import clickhouse_connect
from decimal import Decimal

client = clickhouse_connect.get_client(host='localhost', port=8123, username='admin', password='')

result = client.query('SELECT COUNT(*), SUM(amount) FROM fact_sales').result_rows

count = result[0][0]
total_amount = result[0][1]

print("-" * 40)
print("Сверка ClickHouse И DuckDB")
print("-" * 40)
print(f"Количество строк: {count}")
print(f"Общая выручка:    {total_amount}")
