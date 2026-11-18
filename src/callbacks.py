from dash import Input, Output, callback
import dash_bootstrap_components as dbc
from functools import reduce
import numpy as np
from src.analysis import calc_people_access_summary, calc_people_location_summary

def register_slider_callback(app, peopleTimeWin, analysisResults, tblAccess, events, eventDates, providerId2Name):
    """
    Register callbacks for slider interactions
    """
    
    # Callback for all sliders - this would normally filter data based on slider values
    @app.callback(
        [Output('AccessSummHeader', 'children'),
         Output('AccessSummTenure', 'children'),
         Output('AccessSummUtilization', 'children'),
         Output('AccessSummReentries', 'children'),
         Output('AccessSummConsecPrgs', 'children'),
         Output('AccessSummShelterDays', 'children'),
         Output('AccessSummHousingDays', 'children'),
         Output('LocSummHeader', 'children'),
         Output('LocSummEntry', 'children'),
         Output('LocSummWhereIn', 'children'),
         Output('LocSummNumReentries', 'children'),
         Output('LocSummWhereReentry', 'children'),
         Output('LocSummWhereAbsence', 'children')
         ],
        [Input('TenureSlider', 'value'),
         Input('UtilizationSlider', 'value'),
         Input('ReentrySlider', 'value'),
         Input('ConsecutiveSlider', 'value'),
         Input('ShelterSlider', 'value'),
         Input('HousingSlider', 'value')]
    )
    def update_dashboard(tenureValue, usagePctValue, nReentriesValue, consecProgramsValue, nShelterDaysValue, nHousingDaysValue):

        def calc_cohort(tbl,col,vals):
            idx = ( tbl[col] >= vals[0] ) & ( tbl[col] <= vals[1] )
            return tbl.loc[idx,'PersonId'].unique()

        # Select the cohort based on who used the system within the time window.
        today = eventDates.max()
        cohortDateMask = eventDates > today-peopleTimeWin 
        cohortWin = np.unique(events[cohortDateMask,0])
        nPop = len(cohortWin)

        cohorts = [ cohortWin ]
        cohorts += [ calc_cohort(tblAccess,'Tenure',tenureValue) ]        
        cohorts += [ calc_cohort(tblAccess,'UsagePct',usagePctValue) ]        
        cohorts += [ calc_cohort(tblAccess,'NReentries',nReentriesValue) ]        
        cohorts += [ calc_cohort(tblAccess,'ConsecPrograms',consecProgramsValue) ]        
        cohorts += [ calc_cohort(tblAccess,'NShelterDays',nShelterDaysValue) ]        
        cohorts += [ calc_cohort(tblAccess,'NHousingDays',nHousingDaysValue) ]        

        cohort = reduce(np.intersect1d, cohorts)

        nPeople = len(cohort)

        inCoh = tblAccess.PersonId.isin(cohort)
        analysisResults['PeopleWho'] = calc_people_access_summary(tblAccess,inCoh,nPop)
        analysisResults['PeopleWhere'] = calc_people_location_summary(events,cohort,providerId2Name)

        return tuple(analysisResults['PeopleWho'].values()) + tuple(analysisResults['PeopleWhere'].values())
