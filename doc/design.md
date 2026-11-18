# Dashboard Design

## Design Parameters
Users:
- Not-for-profit homelessness agency managers.

Primary Tasks:
- Summarize homelessness data.
- User friendly filtering of results.

Theme:
- Accessible.
- Comfortable.

Color palette:
- Background      #F6F4EE
- Card Background #F6F4EE
- Primary Blue    #4F7CAC
- Accent Blue     #7EA8BE
- Tan             #D6C6A5
- Dark Text       #2F3A40
- Secondary Text  #6B7280

## Coding Agent Initial Prompts
- When assisting with front-end development:
```
You are acting as a dashboard UX designer.
Do not create any data connections, callbacks, database code or business logic.
Your only goal is to generate front-end page layout, visual structure and user interactive elements.
Use dash and dash-bootstrap-components.
Take note of the coding style and design objective documents located in the doc/ directory.
Do not generate any python code yet.
```
- When assisting with back-end development:
```
You are acting as a database and data analysis developer.
You will be creating a series of functions that perform database connection and data analysis.
Use duckdb for the initial parquet file database connection and data pre-processing.
Use pandas and numpy for data analysis of the outputs of the duckdb queries.
When splitting a task between duckdb and pandas/numpy, play to the strengths of each library.
Take note of the coding style and design objective documents located in the doc/ directory.
The data you'll be working with is in the data/ directory.
Do not generate any python code yet.
```

