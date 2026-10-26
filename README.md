# Administrative Data Dashboard

## Data Flow Pipeline
1. `src/data_loader.py`: Loads, validates and pre-processes data queried from parquet files using DuckDB.
2. `src/transforms.py`: Performs calculations on data tables to extract metrics.
3. `src/components.py`: Pure functions returning layout objects and charts.
4. `app.py`: Assembles layout, handles user interaction state.

## Tech Stack
- Data processing: Pandas / DuckDB
- Charts: Plotly Express
- Dashboard framework: Dash
