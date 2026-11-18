"""
Housing and homelessness system synthetic data dashboard database file.
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

import duckdb
import pandas as pd
from typing import Optional, Dict, Any, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# TODO: Figure out how to disable info but allow errors.
#logger.disabled = True


class ParquetDataManager:
    """
    Class to manage DuckDB loading and querying of parquet files.
    """
    
    def __init__(self, databasePath: str = ":memory:"):
        """
        Initialize DuckDB connection.
        
        Args:
        databasePath (str): Path to database file (default is in-memory).
        """
        try:
            self.conn = duckdb.connect(database=databasePath)
            logger.info(f"Successfully connected to DuckDB at {databasePath}")
            self.loadedTables = set()

        except Exception as e:
            logger.error(f"Failed to connect to DuckDB: {e}")
            raise

    def __del__(self):
        """
        Close the DuckDB connection.
        """
        try:
            self.conn.close()
            logger.info("DuckDB connection closed successfully")
            
        except Exception as e:
            logger.error(f"Failed to close DuckDB connection: {e}")
            raise

    
    def load_table(self, parquetFile: str, tableName: str) -> None:
        """
        Load a parquet file into a table.  Ignored if table already loaded.
        
        Args:
            parquetFile (str): Parquet file (full path) containing table.
            tableName (str): Table name for later queries.
        """
        try:
            if tableName not in self.loadedTables:
                query = f"CREATE OR REPLACE TABLE {tableName} AS SELECT * FROM read_parquet('{parquetFile}')"
                self.conn.execute(query)
                self.loadedTables.add(tableName)
                logger.info(f"Successfully loaded {parquetFile} into table {tableName}.")
            else:
                logger.info(f"Load ignored, table {tableName} already loaded.")


        except Exception as e:
            logger.error(f"Failed to load parquet file {parquetFile} as {tableName}: {e}")
            raise



    def execute_query(self, query: str) -> pd.DataFrame:
        """
        Execute a SQL query and return results as a pandas DataFrame.  Query must
        be performed on a table that has already been loaded using self.load_table().
        
        Args:
            query (str): SQL query to execute
            
        Returns:
            pd.DataFrame: Query results as pandas DataFrame
        """
        try:            
            result = self.conn.execute(query).fetchdf()
            logger.info(f"Query executed successfully: {query}")
            return result
        except Exception as e:
            logger.error(f'Failed to execute query: {e}')
            raise


    def get_table_info(self, tableName: str) -> pd.DataFrame:
        """
        Get information about a table's structure.  tableName must already have been 
        loaded with self.load_table().
        
        Args:
            table_name (str): Name of the table
            
        Returns:
            pd.DataFrame: Table schema information
        """
        try:
            query = f"DESCRIBE {tableName}"
            return self.execute_query(query)
        except Exception as e:
            logger.error(f"Failed to get table info for {table_name}: {e}")
            raise



