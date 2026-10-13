import duckdb

total_checks = duckdb.sql("SELECT COUNT(DISTINCT sale_id) FROM 'data/raw/fact_sales.csv'").fetchone()[0]

multi = duckdb.sql("""
    SELECT COUNT(*) FROM (
        SELECT sale_id FROM 'data/raw/fact_sales.csv'
        GROUP BY sale_id HAVING COUNT(*) > 1
    )
""").fetchone()[0]

avg = duckdb.sql("""
    SELECT ROUND(SUM(amount) / COUNT(DISTINCT sale_id), 2)
    FROM 'data/raw/fact_sales.csv'
""").fetchone()[0]

print(f"Всего чеков: {total_checks}")
print(f"Чеков с >1 товаром: {multi}")
print(f"Средний чек: {avg} руб.")
print("\nПример чека с 3+ товарами:")
example = duckdb.sql("""
    SELECT sale_id, product_id, qty, amount
    FROM 'data/raw/fact_sales.csv'
    WHERE sale_id = (
        SELECT sale_id FROM 'data/raw/fact_sales.csv'
        GROUP BY sale_id HAVING COUNT(*) >= 3 LIMIT 1
    )
""").df()
print(example)