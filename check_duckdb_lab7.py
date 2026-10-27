import duckdb

con = duckdb.connect("retail.duckdb", read_only=True)

result = con.execute("SELECT COUNT(*), SUM(amount) FROM fact_sales").fetchone()

count = result[0]
total_amount = result[1]

print("-" * 40)
print("СВЕРКА DuckDB")
print("-" * 40)
print(f"Количество строк: {count}")
print(f"Общая выручка:    {total_amount}")
