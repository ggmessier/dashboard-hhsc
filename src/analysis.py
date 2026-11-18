import pandas as pd
import numpy as np
from src.database import ParquetDataManager

import logging
logger = logging.getLogger(__name__)    

def calc_people_access_summary(tblAccess,inCoh,nPop):

    nPeople = inCoh.sum()

    summ = { 'Header': f'You have selected {nPeople:,} / {nPop:,} people with your sliders.  Here is their experience:' }

    def populate_stats(col,fmt,nPeople):
        if nPeople == 0:
            return 'N/A (avg), N/A (top 10%)'
        else:
            outStr = f'{fmt.format(x=col.mean())} (avg), '
            outStr += f'{fmt.format(x=col.quantile(0.9))} (top 10%)'
            return outStr

    summ['Tenure'] = 'Days between first system entry and final system exit: '
    summ['Tenure'] += populate_stats(tblAccess.loc[inCoh,'Tenure'],'{x:,.0f}',nPeople)

    summ['Utilization'] = 'Percentage of time they used the system: '
    summ['Utilization'] += populate_stats(tblAccess.loc[inCoh,'UsagePct'],'{x:.1f}%',nPeople)

    summ['Reentries'] = 'Number of times they re-entered homelessness: '
    summ['Reentries'] += populate_stats(tblAccess.loc[inCoh,'NReentries'],'{x:,.0f}',nPeople)

    summ['ConsecutivePrograms'] = 'Number of transitions between agencies/programs: '
    summ['ConsecutivePrograms'] += populate_stats(tblAccess.loc[inCoh,'ConsecPrograms'],'{x:,.0f}',nPeople)

    summ['ShelterDays'] = 'Total number of days spent in shelter: '
    summ['ShelterDays'] += populate_stats(tblAccess.loc[inCoh,'NShelterDays'],'{x:,.0f}',nPeople)

    summ['HousingDays'] = 'Total number of days spent in housing: '
    summ['HousingDays'] += populate_stats(tblAccess.loc[inCoh,'NHousingDays'],'{x:,.0f}',nPeople)

    return summ

def calc_people_location_summary(events,cohort,providerId2Name):

    grpStart = np.r_[0,np.flatnonzero(np.diff(events[:,0]))+1]
    grpEnd = np.r_[ grpStart[1:], len(grpStart) ]

    inCoh = np.isin(events[grpStart,0],cohort)
    nPeople = inCoh.sum()

    if nPeople == 0:
        summ = {}
        summ['Header'] = f'No people selected.'
        summ['FirstEntry'] = ''
        summ['InSystem'] = ''
        summ['NumReentries'] = ''
        summ['ReenterSystem'] = ''
        summ['SystemAbsence'] = ''
        return summ


    sysEntry = np.zeros(nPeople,dtype='int')
    timeSpent = np.zeros(nPeople,dtype='int')
    sysExit = np.zeros(nPeople,dtype='int')

    def find_highest_weight(idx,weights):
        uniqueIdx, inverse = np.unique(idx, return_inverse=True)
        totals = np.bincount(inverse,weights=weights)
        maxPos = totals.argmax()
        return uniqueIdx[maxPos],totals[maxPos]

    # Per person analysis.
    for iV,iSt,iEd in zip(range(nPeople),grpStart,grpEnd):

        prsnEvents = events[iSt:iEd]

        sysEntry[iV] = prsnEvents[:,2][0]
        sysExit[iV] = prsnEvents[:,1][-1]

        notAbsence = prsnEvents[:,2] != 2
        timeSpent[iV],_ = find_highest_weight(prsnEvents[notAbsence,2],prsnEvents[notAbsence,3])



    def most_common(x):
        if len(x) == 0:
            return 0,0
        else:
            vals, cnts = np.unique(x,return_counts=True)
            biggest = np.argmax(cnts)
            return vals[biggest],cnts[biggest]

    entryPrg, entryPrgCnt = most_common(sysEntry[sysEntry > 2])
    mostTime, mostTimeCnt = most_common(timeSpent)

    # Overall analysis.
    inCoh = np.isin(events[:,0],cohort)
    nAbs = (events[inCoh,2] == 2).sum()

    # Find most common departure point for absences.
    absExits = events[inCoh & (events[:,2] == 2),1]
    mostAbsExits, mostAbsExitsCnt = most_common(absExits)

    # Find most common entry point for absences.
    absEntries = events[inCoh & (events[:,1] == 2),2]
    mostAbsEntries, mostAbsEntriesCnt = most_common(absEntries)

    def pct_str(x,y):
        return f'{x:,} / {y:,} ({100*x/y:.1f}%)'

    summ = {}

    summ['Header'] = f'Where are the most likely places to find these {nPeople:,} people:'
    summ['FirstEntry'] = f'{providerId2Name[entryPrg]} was the first system contact point for {pct_str(entryPrgCnt,nPeople)} people.'
    summ['InSystem'] = f'{providerId2Name[mostTime]} is where {pct_str(mostTimeCnt,nPeople)} people spend most of their time.'
    summ['NumReentries'] = f'The {nPeople:,} people temporarily exit and then re-enter homelessness {nAbs:,} times:'
    summ['ReenterSystem'] = f'{providerId2Name[mostAbsEntries]} is where {pct_str(mostAbsEntriesCnt,nAbs)} re-entries occur.'
    summ['SystemAbsence'] = f'{providerId2Name[mostAbsExits]} is where {pct_str(mostAbsExitsCnt,nAbs)} temporary exits occur.'

    return summ

# Function to perform data analysis
def init_layout_data(peopleTimeWin, tblAccess, events, eventDates, providerId2Name):
    """
    Init the data structure used for the dash layout.

    Args:
        tblAccess (pd.DataFrame):  Per person system metric table returned by get_system_access_metrics

    Returns:
        Nothing.
    """

    def calc_tics(min,max,nTic):
        if max-min < nTic:
            nTic = max-min
        incVal = int((max-min)/(nTic-1))
        return { int(x): f'{int(x)}' for x in np.arange(min,max+incVal,incVal,dtype='int') }


    def init_slider_dict(min,max,nTic):
        return { 
            'Min': min, 'Max': max, 'Initial': [ min, max ],
            'Marks': calc_tics(min,max,nTic)
            }
   
    initDict = {}

    # Select the cohort based on who used the system within the time window.
    today = eventDates.max()
    cohortDateMask = eventDates > today-peopleTimeWin 
    cohort = np.unique(events[cohortDateMask,0])


    nPop = len(cohort)

    initDict['PeopleHeader'] = f'{nPop:,} people in my community experienced homelessness in the last {int(peopleTimeWin/np.timedelta64(30,'D'))} months.'

    inCoh = tblAccess.PersonId.isin(cohort)


    # Initialize slider values with max and min values present in the data.
    initDict['PeopleSlider'] = {
        'Tenure': init_slider_dict(0, np.ceil(tblAccess.loc[inCoh].Tenure.max()), nTic=5),
        'Utilization': init_slider_dict(int(tblAccess.loc[inCoh].UsagePct.min()), int(tblAccess.loc[inCoh].UsagePct.max()), nTic=5),
        'Reentries': init_slider_dict(tblAccess.loc[inCoh].NReentries.min(), tblAccess.loc[inCoh].NReentries.max(), nTic=5),
        'ConsecutivePrograms': init_slider_dict(tblAccess.loc[inCoh].ConsecPrograms.min(), tblAccess.loc[inCoh].ConsecPrograms.max(), nTic=5),
        'ShelterDays': init_slider_dict(tblAccess.loc[inCoh].NShelterDays.min(), tblAccess.loc[inCoh].NShelterDays.max(), nTic=5),
        'HousingDays': init_slider_dict(tblAccess.loc[inCoh].NHousingDays.min(), tblAccess.loc[inCoh].NHousingDays.max(), nTic=5),
    }

    # Initialize people experience summary using the full cohort.
    initDict['PeopleWho'] = calc_people_access_summary(tblAccess,inCoh,nPop)
    initDict['PeopleWhere'] = calc_people_location_summary(events,cohort,providerId2Name)

    return initDict


def update_system_access_metrics_from_events(tblAccess: pd.DataFrame, tblProvider: pd.DataFrame, events: np.ndarray):
    """
    Uses the event sequence array to calculate more person specific
    system metrics.  Metrics are added to the person access metric table.

    Args:
        tblAccess (pd.DataFrame):  Per person system metric table returned by get_system_access_metrics
        tblProvider (pd.DataFrame):  Provider identity table returned by get_provider_table()
        events (np.ndarray): Event sequence array returned by get_event_sequences()

    Returns:
        Nothing.
    """

    shelterIds = tblProvider.loc[tblProvider.ServiceType == 'Shelter']['ProviderId'].to_numpy()
    housingIds = tblProvider.loc[tblProvider.ServiceType == 'Housing']['ProviderId'].to_numpy()

    grpStart = np.r_[0,np.flatnonzero(np.diff(events[:,0]))+1]
    grpEnd = np.r_[ grpStart[1:], len(grpStart) ]
    nPeople = len(grpStart)

    nReentry = np.zeros(nPeople,dtype='int')
    nPrg = np.zeros(nPeople,dtype='int')
    nShelterDays = np.zeros(nPeople,dtype='int')
    nHousingDays = np.zeros(nPeople,dtype='int')

    for iV,iSt,iEd in zip(range(nPeople),grpStart,grpEnd):

        prsnEvents = events[iSt:iEd]

        # System re-entries follow absences with destination ID number 2.
        nReentry[iV] = ( prsnEvents[:,2] == 2 ).sum()

        # Ignore absences and count program use events with nonzero duration.
        nPrg[iV] = ( (prsnEvents[:,3] != 0) & (prsnEvents[:,2] != 2) ).sum()

        # Filter out shelters and sum program use duration.
        nShelterDays[iV] = prsnEvents[ np.isin(prsnEvents[:,2],shelterIds), 3].sum()

        # Filter out shelters and sum program use duration.
        nHousingDays[iV] = prsnEvents[ np.isin(prsnEvents[:,2],housingIds), 3].sum()


    tblAccess['NReentries'] = nReentry
    tblAccess['ConsecPrograms'] = nPrg
    tblAccess['NShelterDays'] = nShelterDays
    tblAccess['NHousingDays'] = nHousingDays






def get_event_sequences(dBase: ParquetDataManager, tableName: str = "SystemData",
                        absenceThreshold: int = 180) -> (np.ndarray,np.ndarray):
    """
    Query a synthetic system level admin data file and construct a numpy array that contains
    all the program transitions for each person in that file.  The program transitions are
    returned in a numpy array with columns:
    0: PersonId number.
    1: ProviderId of the source program where the transition originates.
    2: ProviderId of the transitions destination program.
    3: The number of days the person remains in the destination program (duration).

    An initial system entry will have a source ProviderId of 0.  A final system exit will have a 
    destination ProviderId of 1 and a duration of 0.  All intake events also have a duration of
    0.

    An absence from the system is defined as a gap between program access that exceeds
    accessThreshold.  Absences are inserted into the numpy program transition array and
    is identified by ProviderId 2.  The duration of the absence is the number of days
    between program accesses.  Any absences of less than accessThreshold do not appear in the
    array.
    
    
    Args:
        dBase (ParquetDataManager): DuckDB database object.
        tablName (str): System level data table name that has been pre-loaded.
        accessThreshold (int): Threshold for number of days to define an absence from the system.
        
    Returns:
        NDArray[np.int_]: 4 column numpy array with 
        Dict[str, List[tuple]]: Dictionary with PersonId keys and chronological (ProviderId, StartDate) lists
    """
    try:
        
        query = f"""
        SELECT 
            PersonId,
            ProviderId,
            StartDate,
            EndDate,
            -- Calculate days since first start date for each person
            DATEDIFF('day', MIN(StartDate) OVER (PARTITION BY PersonId), StartDate) AS StartDay,
            -- Calculate duration in days
            DATEDIFF('day', StartDate, EndDate) AS Duration,
            -- Calculate gap between consecutive periods
            /*
                * COALESCE takes the first non-null value.  The first DATEDIFF will be null for the
                * last entry which has a gap value of 0.  LEAD pulls the value of the next row
                * of the column defined by the OVER statement.
                */
            COALESCE(
                DATEDIFF('day',
                    EndDate,
                    LEAD(StartDate) OVER (PARTITION BY PersonId ORDER BY StartDate, EndDate)
                ),
                0
            ) AS Gap
        FROM {tableName}
        WHERE StartDate IS NOT NULL
        ORDER BY PersonId, StartDate, EndDate
        """
        
        tbl = dBase.execute_query(query)

        tbl['Src'] = tbl.groupby('PersonId')['ProviderId'].shift(1,fill_value=0)
        net = tbl[[ 'PersonId', 'Src', 'ProviderId', 'Duration', 'Gap' ]].to_numpy()
        dates = tbl['StartDate'].to_numpy(dtype='datetime64[D]')

        # Indices where a system exit entry needs to be inserted.
        idxExit = np.where(net[:-1,0] != net[1:,0])[0] + 1
        idxExit = np.r_[idxExit,len(net)]

        # Create system exit entries.
        exitEntries = np.empty((len(idxExit),4),dtype='int')
        exitEntries[:,0] = net[idxExit-1,0]  # Copy PersonId.
        exitEntries[:,1] = net[idxExit-1,2]  # Src node is final dst ProviderId.
        exitEntries[:,2] = 1 # Dst is 1 for all exits.
        exitEntries[:,3] = 0 # Duration is zero for all exits.

        exitDates = dates[idxExit-1] + net[idxExit-1,3].astype('timedelta64[D]')

        # Indices where a system absence needs to be inserted.
        idxAbs = np.where(net[:,4] > absenceThreshold)[0] + 1  # Test gap entries.
        net[idxAbs,1] = 2  # Src is 2 for all entries that follow absences.

        # Create absence entries.
        absEntries = np.empty((len(idxAbs),4),dtype='int')
        absEntries[:,0] = net[idxAbs,0]  # Copy PersonId.
        absEntries[:,2] = 2  # Dst is 2 for all absence entries.
        absEntries[:,1] = net[idxAbs-1,2]  # Absence src is previous dst.
        absEntries[:,3] = net[idxAbs-1,4]  # Duration is the gap time.

        absDates = dates[idxAbs]  

        insRowPos = np.sort(np.r_[idxAbs,idxExit])  # Merge all row insertion indices.
        ogRowPos = np.arange(len(net),dtype='int')  # Original row indices.
        # For each value in ogRowPos, searchsorted() determines how many inserted rows have been passed.
        # This allows us to calculate the indices of the original rows in the new post-insert array.
        ogRowInsPos = ogRowPos + np.searchsorted(insRowPos,ogRowPos,side='right')

        netAll = np.empty((len(net)+len(insRowPos),4),dtype='int')  # Array for all rows.
        netAll[ogRowInsPos] = net[:,:4]  # Insert original rows.

        absMask = np.isin(insRowPos,idxAbs)  # Mask for the absence entry insertions.
        insRowPos += np.arange(len(insRowPos),dtype='int')  # New row n has had n rows inserted before it.
        netAll[ insRowPos[absMask] ] = absEntries
        netAll[ insRowPos[~absMask] ] = exitEntries

        datesAll = np.empty(len(net)+len(insRowPos),dtype='datetime64[D]')
        datesAll[ ogRowInsPos ] = dates + net[:,3].astype('timedelta64[D]')
        datesAll[ insRowPos[absMask] ] = absDates
        datesAll[ insRowPos[~absMask] ] = exitDates

        logger.info(f"Successfully created the program transition table for {tableName}.")
        return netAll,datesAll
        
    except Exception as e:
        logger.error(f"Failed to create program transition table for {tableName}: {e}")
        raise


def get_provider_table(dBase: ParquetDataManager, tableName: str = "SystemData") -> pd.DataFrame:
    """
    Fetch an index of provider IDs, types and names from the system level
    data table.

    Args:
        dBase (ParquetDataManager): DuckDB database object.
        tableName (str): Name of the table to query
        
    Returns:
        pd.DataFrame: DataFrame with ProviderId and ProviderName columns
    """
    
    # Query to get unique ProviderId to ProviderName mapping
    query = f"""
    SELECT DISTINCT 
        ProviderId,
        ProviderName,
        ServiceType
    FROM {tableName}
    WHERE ProviderId IS NOT NULL AND ProviderName IS NOT NULL AND ServiceType IS NOT NULL
    ORDER BY ProviderId
    """
    
    df = dBase.execute_query(query)
    logger.info(f"Successfully created provider name index with {len(df)} mappings")
    return df

def get_system_access_metrics(dBase: ParquetDataManager, tableName: str = "SystemData") -> pd.DataFrame:
    """
    Calculates tenure (days between first system entry and final exit) and total days spent interacting
    with the system for each person in the system level data.  
    
    Args:
        dBase (ParquetDataManager): DuckDB database object.
        tableName (str): Name of the table to query
        
    Returns:
        pd.DataFrame: DataFrame with PersonId, Tenure, and UsageDays columns
    """
    
    # Query to calculate tenure and usage days for each person
    query = f"""
    SELECT 
        PersonId,
        CAST(MAX(EndDate) AS DATE) - CAST(MIN(StartDate) AS DATE) AS Tenure,
        SUM(CAST(EndDate AS DATE) - CAST(StartDate AS DATE)) AS UsageDays
    FROM {tableName}
    WHERE StartDate IS NOT NULL 
        AND (EndDate IS NOT NULL OR EndDate IS NULL)
    GROUP BY PersonId
    ORDER BY PersonId
    """
    
    df = dBase.execute_query(query)
    logger.info(f"Successfully created access characteristics table with {len(df)} persons")
    return df
