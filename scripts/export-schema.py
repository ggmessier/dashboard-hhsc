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
