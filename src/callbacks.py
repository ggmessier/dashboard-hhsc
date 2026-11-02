import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd


def register_slider_callback(app,analysisResults):
    
    # Callback to update people summary when sliders change
    @app.callback(
        [Output('TenureSummary', 'children'),
        Output('UtilizationSummary', 'children'),
        Output('ReentrySummary', 'children'),
        Output('ConsecutiveSummary', 'children'),
        Output('ShelterSummary', 'children'),
        Output('HousingSummary', 'children')],
        [Input('TenureSlider', 'value'),
        Input('UtilizationSlider', 'value'),
        Input('ReentrySlider', 'value'),
        Input('ConsecutiveSlider', 'value'),
        Input('ShelterSlider', 'value'),
        Input('HousingSlider', 'value')]
    )
    def update_people_summary(tenureValue, utilizationValue, reentryValue, consecutiveValue, shelterValue, housingValue):
        # This function would normally process the slider values to generate updated summary text
        # For now, we'll just return the original text (in a real app, this would be dynamic)
        return (
            analysisResults['PeopleSummary']['Tenure'],
            analysisResults['PeopleSummary']['Utilization'],
            analysisResults['PeopleSummary']['ReentryRate'],
            analysisResults['PeopleSummary']['ConsecutivePrograms'],
            analysisResults['PeopleSummary']['ShelterDays'],
            analysisResults['PeopleSummary']['HousingDays']
        )
