import clickhouse_connect
import pandas as pd

client = clickhouse_connect.get_client(host='localhost', port=8123, username='admin', password='')

print("Создание таблиц в ClickHouse...")
with open('sql/ddl_clickhouse.sql', 'r', encoding='utf-8') as f:
    ddl_queries = f.read().split(';')
    for query in ddl_queries:
        if query.strip():
            client.command(query)

tables = [
    "dim_product", "dim_store", "dim_date", "dim_customer", "dim_employee", "dim_promotion",
    "fact_sales", "fact_returns", "fact_inventory"
]

print("Очистка старых данных...")
for t in tables:
    client.command(f"TRUNCATE TABLE {t}")

print("Загрузка данных из CSV...")
for t in tables:
    df = pd.read_csv(f"data/raw/{t}.csv")
    # Преобразование дат для ClickHouse
    if 'full_date' in df.columns:
        df['full_date'] = pd.to_datetime(df['full_date']).dt.date
        
    client.insert_df(t, df)
    print(f"  {t}: загружено {len(df)} строк")
    
print("Загрузка завершена!")