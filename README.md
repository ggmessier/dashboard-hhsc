# Housing and Homelessness Data Dashboard

## Data Flow Pipeline
1. `app.py`: Dash dashboard entry point.
1. `src/database.py`: Loads and pre-processes data queried from parquet files using DuckDB.
2. `src/analysis.py`: Performs pandas and numpy analysis on the database data.
2. `src/ui.py`: Support functions for the dash user interface.
1. `doc/`: Docs that provide information on the coding standards, design conventions and style conventions to use for this project.

## Tech Stack
- Data processing: DuckDB / Pandas / Numpy
- Dashboard framework: Dash

## Intial Prompt for AI Agent Software Development
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


        SELECT 
            PersonId,
            ProviderId,
            StartDate,
            EndDate,
            -- Calculate days since first start date for each person
            DATEDIFF(StartDate, MIN(StartDate) OVER (PARTITION BY PersonId)) AS StartDay,
            -- Calculate duration in days
            DATEDIFF(EndDate, StartDate) AS Duration,
            -- Calculate gap between consecutive periods
            /*
                * COALESCE takes the first non-null value.  The first DATEDIFF will be null for the
                * last entry which has a gap value of 0.  LEAD pulls the value of the next row
                * of the column defined by the OVER statement.
                */
            COALESCE(
                DATEDIFF(
                    LEAD(StartDate) OVER (PARTITION BY PersonId ORDER BY StartDate),
                    EndDate
                ),
                0
            )
            /*
                DATEDIFF(
                    MAX(EndDate) OVER (PARTITION BY PersonId),
                    EndDate
                )
            */
            ) AS Gap
        FROM {tableName}
        WHERE StartDate IS NOT NULL
        ORDER BY PersonId, StartDate, EndDate


