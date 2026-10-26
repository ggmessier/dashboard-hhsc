import duckdb
import pandas as pd
import numpy as np

def load_table(serviceType,startDate,endDate):

    con = duckdb.connect(database=':memory:')
    startDateStr = startDate.strftime("%Y-%m-%d")
    endDateStr = endDate.strftime("%Y-%m-%d")
    

    query = f"""
    SELECT *
    FROM "data/MasterTable-2026_09_02.parquet"
    WHERE ServiceType = '{serviceType}' AND (
       ( StartDate >= '{startDateStr}'::TIMESTAMP_NS AND EndDate <= '{endDateStr}'::TIMESTAMP_NS ) 
       OR ( EndDate >= '{startDateStr}'::TIMESTAMP_NS AND EndDate <= '{endDateStr}'::TIMESTAMP_NS )
       OR ( StartDate >= '{startDateStr}'::TIMESTAMP_NS AND StartDate <= '{endDateStr}'::TIMESTAMP_NS )
    );
    """

    tbl = con.execute(query).fetch_df()
    tbl.set_index('__index_level_0__', inplace=True)

    con.close()

    return tbl


def load_full_table(serviceType):

    con = duckdb.connect(database=':memory:')

    query = f"""
    SELECT *
    FROM "data/MasterTable-2026_09_02.parquet"
    WHERE ServiceType = '{serviceType}';
    """

    tbl = con.execute(query).fetch_df()
    tbl.set_index('__index_level_0__', inplace=True)

    con.close()

    return tbl

def calc_housing_wait_time(startDate,endDate):

    # Determine first date of entry.
    tblShlt = load_full_table('Shelter')
    firstDay = tblShlt.groupby('PersonId').StartDate.min()

    # Determine diversion day.
    tblDiv = load_full_table('Diversion')
    divDay = tblDiv.groupby('PersonId').StartDate.min()
    divIds = divDay.index.to_numpy()

    # Determine housing entry day.
    tblHousing = load_full_table('Housing')
    hsngDay = tblHousing.groupby('PersonId').StartDate.min()

    # Determine wait time.
    dateIndex = pd.date_range(startDate, endDate+pd.Timedelta('31D'), freq='M').normalize()
    dateIndex += pd.offsets.MonthEnd(0)

    tblWait = {
        'Housed': np.zeros(len(dateIndex)),
        'GotDiversion': np.zeros(len(dateIndex)),
        'HousedWithDiversion': np.zeros(len(dateIndex)),
        'HousedWithoutDiversion': np.zeros(len(dateIndex))
    }

    for i,day in enumerate(dateIndex):
        housedIds = hsngDay[ (hsngDay >= day-pd.Timedelta('30D')) & (hsngDay < day) ].index.to_numpy()
        timeToHsng = (hsngDay[housedIds] - firstDay[housedIds]).dt.days
        housedWithDiv = timeToHsng.index.isin(divIds)

        tblWait['Housed'][i] = len(housedIds)
        tblWait['GotDiversion'][i] = np.sum( np.isin(housedIds,divIds) ) 
        tblWait['HousedWithDiversion'][i] = timeToHsng[housedWithDiv].mean()
        tblWait['HousedWithoutDiversion'][i] = timeToHsng[~housedWithDiv].mean()

    return pd.DataFrame(tblWait,index=dateIndex)



def calc_program_load(serviceTypes,startDate,endDate):

    tblDict = {}
    for serviceType in serviceTypes:

        tbl = load_table(serviceType,startDate,endDate)

        nDays = (tbl.EndDate.max() - tbl.StartDate.min()).days + 2
        load = np.zeros(nDays, dtype=np.int32)

        startDays = (tbl.StartDate - tbl.StartDate.min()).dt.days.to_numpy()
        endDays = (tbl.EndDate - tbl.StartDate.min()).dt.days.to_numpy()+1
        
        np.add.at( load, startDays, 1 )
        np.add.at( load, endDays, -1 )
        load = np.cumsum(load)

        leftBuffer = ( startDate - tbl.StartDate.min() ).days 
        rightBuffer = ( tbl.EndDate.max() - endDate ).days + 1

        tblDict[serviceType] = load[leftBuffer:-rightBuffer]

    dateIndex = pd.date_range(startDate, endDate, freq='D').normalize()
    dateIndex += pd.offsets.MonthEnd(0)
    tbl = pd.DataFrame(tblDict,index=dateIndex)

    return tbl.groupby(level=0).mean()



