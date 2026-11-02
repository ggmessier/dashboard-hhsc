import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
from src.layout import generate_sequence_fig, generate_pathways_tab, generate_people_tab, colors, integrate_tabs
from src.callbacks import register_slider_callback

# Initialize the app with a Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


# Function to perform data analysis
def analyze_data():
    # This is where you would put your actual data analysis logic
    # For now, we'll return the same values as in your original code
    sequence = [
        "Shelter",
        "Diversion",
        "Housing", 
        "Exit",
    ]
    
    # You can modify the sequence here based on your analysis
    # For example, you might want to reorder or filter programs
    # sequence = ["Housing", "Shelter", "Diversion", "Absence"]  # Example of reordering
    

    return {
        'Sequence': sequence,
        'AvgPrograms': 'Average: 3.2',
        'Top10Percent': 'Top 10%: 5',
        'Bottom10Percent': 'Bottom 10%: 1',
        'EnterSystem': 'Enter the system for the first time is Program1 (45/120 entries, 37.5%).',
        'ExitSystem': 'Exit the system for good is Program2 (32/80 exits, 40%).',
        'ReenterSystem': 'Re-enter the system is Program3 (18/60 entries, 30%).',
        'ExitBeforeReentry': 'Exit the system before a re-entry is Program4 (25/70 exits, 35.7%).',
        'PeopleData': {
            'Tenure': {
                'Min': 0,
                'Max': 100,
                'Initial': 50,
                'Marks': {0: '0', 25: '25', 50: '50', 75: '75', 100: '100'}
            },
            'Utilization': {
                'Min': 0,
                'Max': 100,
                'Initial': 50,
                'Marks': {0: '0', 25: '25', 50: '50', 75: '75', 100: '100'}
            },
            'ReentryRate': {
                'Min': 0,
                'Max': 100,
                'Initial': 50,
                'Marks': {0: '0', 25: '25', 50: '50', 75: '75', 100: '100'}
            },
            'ConsecutivePrograms': {
                'Min': 0,
                'Max': 100,
                'Initial': 50,
                'Marks': {0: '0', 25: '25', 50: '50', 75: '75', 100: '100'}
            },
            'ShelterDays': {
                'Min': 0,
                'Max': 100,
                'Initial': 50,
                'Marks': {0: '0', 25: '25', 50: '50', 75: '75', 100: '100'}
            },
            'HousingDays': {
                'Min': 0,
                'Max': 100,
                'Initial': 50,
                'Marks': {0: '0', 25: '25', 50: '50', 75: '75', 100: '100'}
            }
        },
        'PeopleSummary': {
            'Tenure': 'Days between first system entry and final system exit: 180 (average), 365 (top 10%)',
            'Utilization': 'Percentage of those days they used the system: 75% (average), 95% (top 10%)',
            'ReentryRate': 'Their re-entry rate into homelessness: 20% (average), 40% (top 10%)',
            'ConsecutivePrograms': 'Number of program changes: 3 (average), 5 (top 10%)',
            'ShelterDays': 'Total number of days spent in shelter: 180 (average), 365 (top 10%)',
            'HousingDays': 'Total number of days spent in housing: 90 (average), 180 (top 10%)'
        }
    }


# Perform front end analysis.
analysisResults = analyze_data()

# Create dashboard layout.
seqFig = generate_sequence_fig(analysisResults['Sequence'])
pathwaysTab = generate_pathways_tab(seqFig,analysisResults)
peopleTab = generate_people_tab(analysisResults)
integrate_tabs(app,pathwaysTab,peopleTab)


# Register callbacks.
register_slider_callback(app,analysisResults)



if __name__ == '__main__':
    app.run(debug=True)
