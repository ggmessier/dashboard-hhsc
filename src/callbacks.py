"""
Housing and homelessness system synthetic data dashboard callbacks file.
Copyright (C) 2026 Geoffrey Messier

This program is free software: you can redistribute it and/or modify it under the terms 
of the GNU General Public License as published by the Free Software Foundation, either 
version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. 
If not, see <https://www.gnu.org/licenses/>. 
"""


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
