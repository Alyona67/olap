import clickhouse_connect

client = clickhouse_connect.get_client(host='localhost', port=8123, username='admin', password='')

detail_sum = client.query("""
    SELECT SUM(amount) 
    FROM fact_sales 
    WHERE date_id >= 20240101 AND date_id <= 20240131
""").result_rows[0][0]

summary_sum = client.query("""
    SELECT SUM(amount_sum) 
    FROM sales_summary 
    WHERE date_id >= 20240101 AND date_id <= 20240131
""").result_rows[0][0]

print("-" * 27)
print("Сверка за январь 2024 года")
print("-" * 27)
print(f"Сумма по детальной таблице: {detail_sum}")
print(f"Сумма по сводной таблице:   {summary_sum}")

if detail_sum == summary_sum:
    print("\n✅ СВЕРКА ПРОЙДЕНА! Суммы совпадают.")
else:
    print("\n❌ ОШИБКА! Суммы не совпадают.")
