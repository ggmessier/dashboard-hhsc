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


def generate_pathways_tab(seqFig,analysisResults):
    # Pathways Tab Content
    pathwaysTab = dbc.Container([
        dbc.Row([
            dbc.Col(html.H4("The most common pathway through the system:"), width=12)
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=seqFig), width=12)
        ]),
        dbc.Row([
            # Left Half with border and rounded corners - now using divs for editable content
            dbc.Col([
                html.H5("Number of times a person changes programs along their pathway:"),
                html.P(id="AvgProgramsText", children=analysisResults['AvgPrograms'], style={'font-size': '20px', 'margin': '5px 15px'}),
                html.P(id="Top10PercentText", children=analysisResults['Top10Percent'], style={'font-size': '20px', 'margin': '5px 15px'}),
                html.P(id="Bottom10PercentText", children=analysisResults['Bottom10Percent'], style={'font-size': '20px', 'margin': '5px 15px'})
            ], width=4, style={
                'border': '2px solid black',
                'border-radius': '15px',
                'padding': '15px',
                'margin': '10px',
                'background-color': colors['CardBackground']
            }),
            # Right Half with border and rounded corners
            dbc.Col([
                html.H5("The most common place to..."),
                html.P(analysisResults['EnterSystem'], style={'font-size': '20px', 'margin': '5px 15px'}),
                html.P(analysisResults['ExitSystem'], style={'font-size': '20px', 'margin': '5px 15px'}),
                html.P(analysisResults['ReenterSystem'], style={'font-size': '20px', 'margin': '5px 15px'}),
                html.P(analysisResults['ExitBeforeReentry'], style={'font-size': '20px', 'margin': '5px 15px'})
            ], width=6, style={
                'border': '2px solid black',
                'border-radius': '15px',
                'padding': '15px',
                'margin': '10px',
                'background-color': colors['CardBackground']
            })
        ], justify="center")  # Ensure columns are aligned side by side
    ], fluid=True)

    return pathwaysTab

def generate_people_tab(analysisResults):
    # People Tab Content
    peopleTab = dbc.Container([
        dbc.Row([
            # Left Half
            dbc.Col([
                html.H5("2,134 people in my community experienced homelessness in the past 3 months."),
                html.P("Here is the experience of the 2,134/2,134 people you have selected with your sliders:", style={'font-size': '20px', 'margin': '5px 0px'}),
                html.P(id="TenureSummary", children=analysisResults['PeopleSummary']['Tenure'], style={'font-size': '20px', 'margin': '5px 15px'}),
                html.P(id="UtilizationSummary", children=analysisResults['PeopleSummary']['Utilization'], style={'font-size': '20px', 'margin': '5px 15px'}),
                html.P(id="ReentrySummary", children=analysisResults['PeopleSummary']['ReentryRate'], style={'font-size': '20px', 'margin': '5px 15px'}),
                html.P(id="ConsecutiveSummary", children=analysisResults['PeopleSummary']['ConsecutivePrograms'], style={'font-size': '20px', 'margin': '5px 15px'}),
                html.P(id="ShelterSummary", children=analysisResults['PeopleSummary']['ShelterDays'], style={'font-size': '20px', 'margin': '5px 15px'}),
                html.P(id="HousingSummary", children=analysisResults['PeopleSummary']['HousingDays'], style={'font-size': '20px', 'margin': '5px 15px'})
            ], width=6, style={
                'border': '2px solid black',
                'border-radius': '15px',
                'padding': '15px',
                'margin': '10px',
                'background-color': colors['CardBackground']
            }),
            # Right Half
            dbc.Col([
    #            html.H5("Sliders for System Analysis"),
                html.Div([html.Label("Days between first system entry and final exit.", style={'display': 'inline-block', 'width': '500px', 'color': colors['DarkText']}), 
                        dcc.Slider(analysisResults['PeopleData']['Tenure']['Min'], 
                                    analysisResults['PeopleData']['Tenure']['Max'], 
                                    1, 
                                    value=analysisResults['PeopleData']['Tenure']['Initial'], 
                                    marks=analysisResults['PeopleData']['Tenure']['Marks'], 
                                    id='TenureSlider')]),
                html.Div([html.Label("Percentage of days utilizing the system.", style={'display': 'inline-block', 'width': '500px', 'color': colors['DarkText']}), 
                        dcc.Slider(analysisResults['PeopleData']['Utilization']['Min'], 
                                    analysisResults['PeopleData']['Utilization']['Max'], 
                                    1, 
                                    value=analysisResults['PeopleData']['Utilization']['Initial'], 
                                    marks=analysisResults['PeopleData']['Utilization']['Marks'], 
                                    id='UtilizationSlider')]),
                html.Div([html.Label("Homelessness re-entry rate.", style={'display': 'inline-block', 'width': '500px', 'color': colors['DarkText']}), 
                        dcc.Slider(analysisResults['PeopleData']['ReentryRate']['Min'], 
                                    analysisResults['PeopleData']['ReentryRate']['Max'], 
                                    1, 
                                    value=analysisResults['PeopleData']['ReentryRate']['Initial'], 
                                    marks=analysisResults['PeopleData']['ReentryRate']['Marks'], 
                                    id='ReentrySlider')]),
                html.Div([html.Label("Number of program transitions.", style={'display': 'inline-block', 'width': '500px', 'color': colors['DarkText']}), 
                        dcc.Slider(analysisResults['PeopleData']['ConsecutivePrograms']['Min'], 
                                    analysisResults['PeopleData']['ConsecutivePrograms']['Max'], 
                                    1, 
                                    value=analysisResults['PeopleData']['ConsecutivePrograms']['Initial'], 
                                    marks=analysisResults['PeopleData']['ConsecutivePrograms']['Marks'], 
                                    id='ConsecutiveSlider')]),
                html.Div([html.Label("Total days spent in shelter.", style={'display': 'inline-block', 'width': '500px', 'color': colors['DarkText']}), 
                        dcc.Slider(analysisResults['PeopleData']['ShelterDays']['Min'], 
                                    analysisResults['PeopleData']['ShelterDays']['Max'], 
                                    1, 
                                    value=analysisResults['PeopleData']['ShelterDays']['Initial'], 
                                    marks=analysisResults['PeopleData']['ShelterDays']['Marks'], 
                                    id='ShelterSlider')]),
                html.Div([html.Label("Total days spent in housing.", style={'display': 'inline-block', 'width': '500px', 'color': colors['DarkText']}), 
                        dcc.Slider(analysisResults['PeopleData']['HousingDays']['Min'], 
                                    analysisResults['PeopleData']['HousingDays']['Max'], 
                                    1, 
                                    value=analysisResults['PeopleData']['HousingDays']['Initial'], 
                                    marks=analysisResults['PeopleData']['HousingDays']['Marks'], 
                                    id='HousingSlider')]),
            ],width=4, style={
                'border': '2px solid black',
                'border-radius': '15px',
                'padding': '15px',
                'margin': '10px',
                'background-color': colors['CardBackground']
            })
        ], justify="center")
    ], fluid=True)

    return peopleTab


def integrate_tabs(app,pathwaysTab,peopleTab):
    # Integrate tabs.
    app.layout = dbc.Container([
        dbc.Tabs([
            dbc.Tab(label="Pathways", children=pathwaysTab, tab_id="TabPathways"),
            dbc.Tab(label="People", children=peopleTab, tab_id="TabPeople")
        ], id="Tabs", active_tab="TabPathways", style={'backgroundColor': colors['Background']})
    ], fluid=True)

