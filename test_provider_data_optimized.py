"""
Test script for optimized provider data extraction with duration filtering.
"""

import duckdb
from src.database import create_duckdb_connection, get_person_provider_data

def test_optimized_provider_data():
    """Test the optimized person-provider data extraction function."""
    try:
        # Create DuckDB connection
        conn = create_duckdb_connection()
        
        print("=== Testing optimized implementation with min_duration=0 ===")
        # Test with no duration filtering
        result_all = get_person_provider_data(conn, min_duration=0)
        
        print(f"Total persons found: {len(result_all)}")
        
        if result_all:
            # Show sample data
            sample_persons = list(result_all.keys())[:3]
            for person_id in sample_persons:
                providers = result_all[person_id]
                print(f"\nPersonId: {person_id}")
                print(f"Number of providers: {len(providers)}")
                print("Provider history (ProviderId, StartDate):")
                for provider_id, start_date in providers[:3]:  # Show first 3 providers
                    print(f"  - ProviderId: {provider_id}, StartDate: {start_date}")
                if len(providers) > 3:
                    print(f"  ... and {len(providers) - 3} more")
        
        print("\n=== Testing optimized implementation with min_duration=30 ===")
        # Test with duration filtering
        result_filtered = get_person_provider_data(conn, min_duration=30)
        
        print(f"Total persons found: {len(result_filtered)}")
        
        if result_filtered:
            # Show sample data
            sample_persons = list(result_filtered.keys())[:3]
            for person_id in sample_persons:
                providers = result_filtered[person_id]
                print(f"\nPersonId: {person_id}")
                print(f"Number of providers (duration > 30 days): {len(providers)}")
                print("Provider history (ProviderId, StartDate):")
                for provider_id, start_date in providers[:3]:  # Show first 3 providers
                    print(f"  - ProviderId: {provider_id}, StartDate: {start_date}")
                if len(providers) > 3:
                    print(f"  ... and {len(providers) - 3} more")
        
        # Close connection
        conn.close()
        
        print("\n=== Test Completed Successfully ===")
        return result_all, result_filtered
        
    except Exception as e:
        print(f"Test failed with error: {e}")
        raise

if __name__ == "__main__":
    test_optimized_provider_data()