import duckdb

tables = ["dim_product", "dim_store", "dim_date", "dim_customer",
          "dim_employee", "dim_promotion",
          "fact_sales", "fact_returns", "fact_inventory"]

print(f"{'Таблица':<20} {'Строк':>8}")
print("-" * 30)
for t in tables:
    n = duckdb.sql(f"SELECT count(*) FROM 'data/raw/{t}.csv'").fetchone()[0]
    print(f"{t:<20} {n:>8}")