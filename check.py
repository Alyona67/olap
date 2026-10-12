import duckdb

print("DuckDB version:", duckdb.sql("SELECT version()").fetchall())
print("Simple check:", duckdb.sql("SELECT 1 AS ok").fetchall())