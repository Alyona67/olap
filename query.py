import duckdb

print("=== dim_product (товары) ===")
print(duckdb.sql("SELECT * FROM 'data/raw/dim_product.csv'").df())

print("\n=== fact_sales (продажи) ===")
print(duckdb.sql("SELECT * FROM 'data/raw/fact_sales.csv'").df())

print("\n=== dim_store (магазины) ===")
print(duckdb.sql("SELECT * FROM 'data/raw/dim_store.csv'").df())

print("\n=== dim_date (даты) ===")
print(duckdb.sql("SELECT * FROM 'data/raw/dim_date.csv'").df())