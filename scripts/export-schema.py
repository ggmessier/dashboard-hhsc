"""
Housing and homelessness system synthetic data dashboard schema export script.
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

con = duckdb.connect()
tables = {
    "main": "data/SHHAd-System-Level-2026_11_03.parquet"
}

schema_text = "# Database Schema Reference\n\n"
for table_name, file_path in tables.items():
    schema_text += f"## Table: {table_name}\nFile: `{file_path}`\n```sql\n"
    describe_df = con.sql(f"DESCRIBE SELECT * FROM '{file_path}'").df()
    for _, row in describe_df.iterrows():
        schema_text += f"{row['column_name']} {row['column_type']}\n"
    schema_text += "```\n\n"

with open("data/schema.sql", "w") as f:
    f.write(schema_text)

print("Updated data/schema.sql")
