# example_usage_optimized.py
"""
Example usage of the optimized database functions with ParquetDataManager.
"""

import sys
import os

# Add src to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.database import create_duckdb_connection, ParquetDataManager

def main():
    """
    Demonstrate usage of optimized database functions.
    """
    try:
        # Create database connection
        print("Creating DuckDB connection...")
        conn = create_duckdb_connection(":memory:")
        
        # Create parquet data manager
        print("Creating parquet data manager...")
        parquet_path = "data/SHHAd-System-Level-2026_11_03.parquet"
        data_manager = ParquetDataManager(conn, parquet_path)
        
        # Get provider name index (this will load the table once)
        print("Getting provider name index...")
        provider_index = data_manager.get_provider_name_index_optimized()
        print(f"Retrieved {len(provider_index)} provider mappings")
        print("First 5 mappings:")
        print(provider_index.head())
        
        # Get access characteristics (this will reuse the same loaded table)
        print("\nGetting access characteristics...")
        access_chars = data_manager.get_access_characteristics_optimized()
        print(f"Retrieved access characteristics for {len(access_chars)} persons")
        print("First 5 persons:")
        print(access_chars.head())
        
        # Close connection
        conn.close()
        print("\nDatabase connection closed.")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
```Now let me create a simple example