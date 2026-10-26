# Database Schema Reference

## Table: main
File: `data/MasterTable-2026_09_02.parquet`
```sql
PersonId BIGINT         -- Primary ID for unique individuals
ServiceType VARCHAR     -- Category or type of administrative service
ServiceID BIGINT        -- Unique identifier for the specific service instance/program
StartDate TIMESTAMP_NS  -- Service entry/enrollment timestamp
EndDate TIMESTAMP_NS    -- Service exit/discharge timestamp
FirstName VARCHAR
LastName VARCHAR
DOB TIMESTAMP_NS
ProviderId BIGINT       -- Identifier for service provider
ProviderName VARCHAR
__index_level_0__ BIGINT  -- Internal index column (ignore in SQL queries)```

