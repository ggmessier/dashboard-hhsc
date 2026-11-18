"""
Test file for database module functionality.
"""

import duckdb
from src.database import create_duckdb_connection, get_person_provider_data

def test_get_person_provider_data():
    """Test the person-program data extraction function."""
    try:
        # Create DuckDB connection
        conn = create_duckdb_connection()
        
        # Get person-program data
        result = get_person_provider_data(conn)
        
        print("Sample of extracted data:")
        for person_id, programs in list(result.items())[:3]:  # Show first 3 persons
            print(f"PersonId: {person_id}")
            print(f"Programs: {programs}")
            print()
        
        print(f"Total number of persons: {len(result)}")
        
        # Close connection
        conn.close()
        
        return result
        
    except Exception as e:
        print(f"Test failed with error: {e}")
        raise

if __name__ == "__main__":
    test_get_person_provider_data()