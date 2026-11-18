# Housing and Homelessness Data Dashboard

The code in this repository is provided for the public good and is released under the GNU General Public License Version 3 or, at your option, any later version.  For more information, see the [additional information](https://gnu.org/licenses) provided by the Free Software Foundation.


## Data Flow Pipeline
1. `app.py`: Dash dashboard entry point.
1. `src/database.py`: DuckDB parquet file database interface functions.
2. `src/analysis.py`: Performs pandas and numpy analysis on the database data.
2. `src/layout.py`: Dash user interface layout file.
2. `src/callbacks.py`: Dash user interface callback functions.
1. `doc/`: Docs that provide information on the coding standards, design conventions and style conventions to use for this project.

## Tech Stack
- Data processing: DuckDB / Pandas / Numpy
- Dashboard framework: Dash



