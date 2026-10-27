import clickhouse_connect
from pathlib import Path

client = clickhouse_connect.get_client(host='localhost', port=8123, username='admin', password='')

print("Создание сводной таблицы...")
sql = Path("sql/ddl_summary_lab9.sql").read_text(encoding="utf-8")

queries = [q.strip() for q in sql.split(";") if q.strip()]

for q in queries:
    client.command(q)

print("Готово! Проверяем количество строк в сводке:")
count = client.query("SELECT COUNT(*) FROM sales_summary").result_rows[0][0]
print(f"Строк в сводке: {count}")

print("\nСверка с детальной таблицей:")
total_sum = client.query("SELECT SUM(amount_sum) FROM sales_summary").result_rows[0][0]
print(f"Общая выручка в сводке: {total_sum}")