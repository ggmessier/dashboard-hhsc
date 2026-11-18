"""
Housing and homelessness system synthetic data dashboard layout file.
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

import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd

colors = {
    'Background': '#F6F4EE',  # warm ivory
    'CardBackground': '#F6F4EE',
    'PrimaryBlue': '#4F7CAC',
    'AccentBlue': '#7EA8BE',
    'Tan': '#D6C6A5',
    'DarkText': '#2F3A40',
    'SecondaryText': '#6B7280'
}


def generate_sequence_fig(sequence):

    # Spread nodes apart
    x = [i * 2 for i in range(len(sequence))]
    y = [0] * len(sequence)
    fig = go.Figure()
    # Draw arrows first so they appear behind the nodes
    for i in range(len(sequence) - 1):
        fig.add_annotation(
            x=x[i + 1] - 0.6,
            y=0,
            ax=x[i] + 0.6,
            ay=0,
            xref="x",
            yref="y",
            axref="x",
            ayref="y",
            showarrow=True,
            arrowhead=2,
            arrowsize=2,
            arrowwidth=3,
            arrowcolor="black"
        )
    # Draw program bubbles
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="markers+text",
            text=sequence,
            textposition="middle center",
            hoverinfo="text",
            textfont=dict(
                family="Arial",
                size=20,
                color="black"
            ),
            marker=dict(
                size=90,
                color=colors['AccentBlue'],
                line=dict(
                    color=colors['PrimaryBlue'],
                    width=3
                )
            )
        )
    )
    fig.update_layout(
        height=250,
        showlegend=False,
        plot_bgcolor=colors['Background'],
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(
            visible=False,
            range=[-1, max(x) + 1]
        ),
        yaxis=dict(
            visible=False,
            range=[-1, 1]
        )
    )

    return fig



def generate_people_tab(analysisResults):
    # People Tab Content
    peopleTab = dbc.Container([
        dbc.Row([
            html.H5(analysisResults['PeopleHeader'], style={'justify': 'center'})
            ], justify='center', style={
                'border': '2px solid black',
                'border-radius': '15px',
                'padding': '15px',
                'margin': '10px',
                'background-color': colors['CardBackground']
            }),
        dbc.Row([
            # Right Half
            dbc.Col([
                html.H5("Use the sliders to select the people you are interested in:", style={'font-size': '20px', 'margin': '5px 0px'}),
                html.Div([html.Label("Days between first system entry and final exit.", style={'display': 'inline-block', 'width': '500px', 'color': colors['DarkText']}), 
                        dcc.RangeSlider(
                            min=analysisResults['PeopleSlider']['Tenure']['Min'], 
                            max=analysisResults['PeopleSlider']['Tenure']['Max'], 
                            step=1, 
                            value=[analysisResults['PeopleSlider']['Tenure']['Initial'][0], analysisResults['PeopleSlider']['Tenure']['Initial'][1]], 
                            marks=analysisResults['PeopleSlider']['Tenure']['Marks'], 
                            id='TenureSlider')]),
                html.Div([html.Label("Percentage of days utilizing programs and supports.", style={'display': 'inline-block', 'width': '500px', 'color': colors['DarkText']}), 
                        dcc.RangeSlider(
                            min=analysisResults['PeopleSlider']['Utilization']['Min'], 
                            max=analysisResults['PeopleSlider']['Utilization']['Max'], 
                            step=1, 
                            value=[analysisResults['PeopleSlider']['Utilization']['Initial'][0], analysisResults['PeopleSlider']['Utilization']['Initial'][1]], 
                            marks=analysisResults['PeopleSlider']['Utilization']['Marks'], 
                            id='UtilizationSlider')]),
                html.Div([html.Label("Number of times homelessness is exited and re-entered.", style={'display': 'inline-block', 'width': '500px', 'color': colors['DarkText']}), 
                        dcc.RangeSlider(
                            min=analysisResults['PeopleSlider']['Reentries']['Min'], 
                            max=analysisResults['PeopleSlider']['Reentries']['Max'], 
                            step=1, 
                            value=[analysisResults['PeopleSlider']['Reentries']['Initial'][0], analysisResults['PeopleSlider']['Reentries']['Initial'][1]], 
                            marks=analysisResults['PeopleSlider']['Reentries']['Marks'], 
                            id='ReentrySlider')]),
                html.Div([html.Label("Number of transitions between agencies or programs.", style={'display': 'inline-block', 'width': '500px', 'color': colors['DarkText']}), 
                        dcc.RangeSlider(
                            min=analysisResults['PeopleSlider']['ConsecutivePrograms']['Min'], 
                            max=analysisResults['PeopleSlider']['ConsecutivePrograms']['Max'], 
                            step=1, 
                            value=[analysisResults['PeopleSlider']['ConsecutivePrograms']['Initial'][0], analysisResults['PeopleSlider']['ConsecutivePrograms']['Initial'][1]], 
                            marks=analysisResults['PeopleSlider']['ConsecutivePrograms']['Marks'], 
                            id='ConsecutiveSlider')]),
                html.Div([html.Label("Total days spent in shelter.", style={'display': 'inline-block', 'width': '500px', 'color': colors['DarkText']}), 
                        dcc.RangeSlider(
                            min=analysisResults['PeopleSlider']['ShelterDays']['Min'], 
                            max=analysisResults['PeopleSlider']['ShelterDays']['Max'], 
                            step=1, 
                            value=[analysisResults['PeopleSlider']['ShelterDays']['Initial'][0], analysisResults['PeopleSlider']['ShelterDays']['Initial'][1]], 
                            marks=analysisResults['PeopleSlider']['ShelterDays']['Marks'], 
                            id='ShelterSlider')]),
                html.Div([html.Label("Total days spent in housing.", style={'display': 'inline-block', 'width': '500px', 'color': colors['DarkText']}), 
                        dcc.RangeSlider(
                            min=analysisResults['PeopleSlider']['HousingDays']['Min'], 
                            max=analysisResults['PeopleSlider']['HousingDays']['Max'], 
                            step=1, 
                            value=[analysisResults['PeopleSlider']['HousingDays']['Initial'][0], analysisResults['PeopleSlider']['HousingDays']['Initial'][1]], 
                            marks=analysisResults['PeopleSlider']['HousingDays']['Marks'], 
                            id='HousingSlider')]),
            ],width=4, style={
                'border': '2px solid black',
                'border-radius': '15px',
                'padding': '15px',
                'margin': '10px',
                'background-color': colors['CardBackground']
            }),
            # Left Half
            dbc.Col([
                html.H5(id='AccessSummHeader', children=analysisResults['PeopleWho']['Header'], style={'font-size': '20px', 'margin': '5px 0px'}),
                html.P(id="AccessSummTenure", children=analysisResults['PeopleWho']['Tenure'], style={'font-size': '20px', 'margin': '5px 15px'}),
                html.P(id="AccessSummUtilization", children=analysisResults['PeopleWho']['Utilization'], style={'font-size': '20px', 'margin': '5px 15px'}),
                html.P(id="AccessSummReentries", children=analysisResults['PeopleWho']['Reentries'], style={'font-size': '20px', 'margin': '5px 15px'}),
                html.P(id="AccessSummConsecPrgs", children=analysisResults['PeopleWho']['ConsecutivePrograms'], style={'font-size': '20px', 'margin': '5px 15px'}),
                html.P(id="AccessSummShelterDays", children=analysisResults['PeopleWho']['ShelterDays'], style={'font-size': '20px', 'margin': '5px 15px'}),
                html.P(id="AccessSummHousingDays", children=analysisResults['PeopleWho']['HousingDays'], style={'font-size': '20px', 'margin': '5px 15px'})
            ], width=6, style={
                'border': '2px solid black',
                'border-radius': '15px',
                'padding': '15px',
                'margin': '10px',
                'background-color': colors['CardBackground']
            }),

        ], justify="center"),

        dbc.Row([
            # Add a pull down menu for "most likely", "2nd most likely", "3rd most likely"
            dbc.Col([
                html.H5(id='LocSummHeader',children=analysisResults['PeopleWhere']['Header'],  style={'font-size': '20px', 'margin': '5px 0px'}),
                html.P(id="LocSummEntry", children=analysisResults['PeopleWhere']['FirstEntry'], style={'font-size': '20px', 'margin': '5px 15px'}),
                html.P(id="LocSummWhereIn", children=analysisResults['PeopleWhere']['InSystem'], style={'font-size': '20px', 'margin': '5px 15px'}),
                html.P(id="LocSummNumReentries", children=analysisResults['PeopleWhere']['NumReentries'], style={'font-size': '20px', 'margin': '5px 15px'}),
                html.P(id="LocSummWhereReentry", children=analysisResults['PeopleWhere']['ReenterSystem'], style={'font-size': '20px', 'margin': '5px 30px'}),
                html.P(id="LocSummWhereAbsence", children=analysisResults['PeopleWhere']['SystemAbsence'], style={'font-size': '20px', 'margin': '5px 30px'}),
            ])
            ], justify='center', style={
                'border': '2px solid black',
                'border-radius': '15px',
                'padding': '15px',
                'margin': '10px',
                'background-color': colors['CardBackground']
            }),


    ], fluid=True)

    return peopleTab


def integrate_tabs(app,peopleTab):
    # Integrate tabs.
    app.layout = dbc.Container([
        dbc.Tabs([
#            dbc.Tab(label="Pathways", children=pathwaysTab, tab_id="TabPathways"),
            dbc.Tab(label="People", children=peopleTab, tab_id="TabPeople")
        ], id="Tabs", active_tab="TabPeople", style={'backgroundColor': colors['Background']})
    ], fluid=True)
