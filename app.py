import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import src.data_loader as dl  

# Load data
startDate = pd.to_datetime('2025-01-01')
endDate = pd.to_datetime('2027-01-01')

tblWait = dl.calc_housing_wait_time(startDate,endDate)
# Normalize and resample tblWait to match tbl_monthly's index structure
tblWait_normalized = tblWait.set_index(tblWait.index.normalize())
tblWait_monthly = tblWait_normalized.resample('M').sum()

tbl = dl.calc_program_load(['Housing', 'Shelter'], startDate, endDate)
tbl.set_index(tbl.index.normalize(), inplace=True)
tbl_monthly = tbl.resample('M').sum()

tblWait_monthly.index = tbl_monthly.index


# Prepare slider options: one entry per month
month_dates = list(tbl_monthly.index)
month_labels = {i: d.strftime('%Y-%m') for i, d in enumerate(month_dates)}


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Calculate fixed y-axis range based on maximum value in the table
max_value = tbl_monthly.values.max()
y_max = max_value + 150

app.layout = dbc.Container([
    html.H1("Monthly Program Load Dashboard", className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            html.Label("Select Month:"),
            dcc.Slider(
                id='month-slider',
                min=0,
                max=len(month_dates) - 1,
                step=1,
                value=len(month_dates) - 1,
                allow_direct_input=False,
                marks={i: label for i, label in month_labels.items() if i % max(1, len(month_dates) // 10) == 0},
                tooltip={}
            )
        ], width=12)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='bar-chart')
        ])
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            html.H5(id='housed-value', className="mb-2"),
            html.H5(id='diversion-value', className="mb-2"),
            html.H5(id='avg-days-with-div', className="mb-2")
        ])
    ], className="mb-4")
], fluid=True)


@app.callback(
    Output('bar-chart', 'figure'),
    Output('housed-value', 'children'),
    Output('diversion-value', 'children'),
    Output('avg-days-with-div', 'children'),
    Input('month-slider', 'value')
)
def update_chart(selected_idx):
    selected_date = month_dates[selected_idx]
    row = tbl_monthly.loc[selected_date]
    
    # Get the categories from the column names
    categories = tbl_monthly.columns.tolist()
    
    # Convert to long format preserving the actual column names
    df = row.reset_index()
    df.columns = ['Category', 'Value']

    # Get Wait Time values for the selected month
    wait_row = tblWait_monthly.loc[selected_date]
    housed_val = wait_row['Housed']
    diversion_val = wait_row['GotDiversion']
    avgDaysWithDiv_val = wait_row['HousedWithDiversion']
    avgDaysWithoutDiv_val = wait_row['HousedWithoutDiversion']

    fig = px.bar(
        df,
        x='Category',
        y='Value',
        title=selected_date.strftime('%B %Y'),
        text=df['Value'].apply(lambda x: f"{round(x)}").values
    )
    fig.update_layout(
        xaxis_title=None, 
        yaxis_title="Average Daily Program Load", 
        showlegend=False, 
        yaxis=dict(range=(0, y_max))
    )
    fig.update_traces(
        texttemplate='%{text}', 
        textposition='outside', 
        textfont=dict(size=20),
        selector=dict(type='bar')
    )
    fig.update_xaxes(tickfont=dict(size=20))

    return fig, f"Housed this Month: {round(housed_val)}", f"Housed this Month with Diversion: {round(diversion_val)}", f"People housed waited {round(avgDaysWithDiv_val)} days."

if __name__ == '__main__':
    # For development.
    app.run(debug=True)



