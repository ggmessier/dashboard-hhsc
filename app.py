#%%
#%load_ext autoreload
#%autoreload 2

import sys

import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from src.layout import generate_sequence_fig, generate_people_tab, colors, integrate_tabs
from src.callbacks import register_slider_callback

from src.database import ParquetDataManager
from src.analysis import init_layout_data, get_provider_table, get_system_access_metrics, get_event_sequences
from src.analysis import update_system_access_metrics_from_events, calc_people_access_summary, calc_people_location_summary


#%%
dBase = ParquetDataManager()
dBase.load_table(parquetFile='data/SHHAd-System-Level-2026_11_03.parquet',tableName='SystemData')

tblProvider = get_provider_table(dBase,'SystemData')
tblAccess = get_system_access_metrics(dBase,'SystemData')
tblAccess['UsagePct'] = 100 * tblAccess['UsageDays'] / tblAccess['Tenure']

events,eventDates = get_event_sequences(dBase,'SystemData',absenceThreshold = 180)

# Make sure no future records are included in the analysis.
today = np.datetime64('2030-01-01','D')
pastRecords = eventDates <= today
events = events[pastRecords]
eventDates = eventDates[pastRecords]

cohort = np.unique(events[:,0])
tblAccess = tblAccess.loc[ tblAccess.PersonId.isin(cohort) ]

update_system_access_metrics_from_events(tblAccess,tblProvider,events)

peopleTimeWin = np.timedelta64(3*30,'D')

providerId2Name = dict( tblProvider[['ProviderId','ProviderName']].values )
analysisResults = init_layout_data(peopleTimeWin,tblAccess,events,eventDates,providerId2Name)


#%%
# Initialize the app with a Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


# Create dashboard layout.
#seqFig = generate_sequence_fig(analysisResults['Sequence'])
peopleTab = generate_people_tab(analysisResults)
integrate_tabs(app,peopleTab)


# Register callbacks.
register_slider_callback(app,peopleTimeWin,analysisResults,tblAccess,events,eventDates,providerId2Name)



if __name__ == '__main__':
    app.run(debug=True)

# %%
