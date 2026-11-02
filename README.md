# Housing and Homelessness Data Dashboard

## Data Flow Pipeline
1. `app.py`: Dash dashboard entry point.
1. `src/database.py`: Loads and pre-processes data queried from parquet files using DuckDB.
2. `src/analysis.py`: Performs pandas and numpy analysis on the database data.
2. `src/ui.py`: Support functions for the dash user interface.

## Tech Stack
- Data processing: DuckDB / Pandas / Numpy
- Dashboard framework: Dash
