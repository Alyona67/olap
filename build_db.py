import duckdb
from pathlib import Path

# Путь к файлу базы данных
DB_PATH = "retail.duckdb"

# Пути к SQL-файлам
DDL_FILE = "sql/ddl_duckdb.sql"
LOAD_FILE = "sql/load_duckdb.sql"

print("Создание витрины 'Розница' в DuckDB")

# Подключаемся к базе (создастся, если нет)
con = duckdb.connect(DB_PATH)
print(f"\n✓ База данных: {DB_PATH}")

# 1. Выполняем DDL (создание таблиц)
print(f"\n[1/2] Выполняю {DDL_FILE}...")
ddl_sql = Path(DDL_FILE).read_text(encoding="utf-8")
con.execute(ddl_sql)
print("   Таблицы созданы")

# 2. Выполняем загрузку
print(f"\n[2/2] Выполняю {LOAD_FILE}...")
load_sql = Path(LOAD_FILE).read_text(encoding="utf-8")
con.execute(load_sql)
print("   Данные загружены")

# 3. Проверяем число строк в каждой таблице
print("Проверка: число строк в таблицах")


tables = [
    "dim_product", "dim_store", "dim_date",
    "dim_customer", "dim_employee", "dim_promotion",
    "fact_sales", "fact_returns", "fact_inventory"
]

print(f"\n{'Таблица':<20} {'Строк':>8}")
for t in tables:
    n = con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    print(f"{t:<20} {n:>8}")

# 4. Главная метрика
total_revenue = con.execute("SELECT SUM(amount) FROM fact_sales").fetchone()[0]
print(f"\n{'Главная метрика':<20}")
print("-" * 30)
print(f"Выручка (SUM amount): {total_revenue}")

con.close()
print("Готово! База retail.duckdb создана.")
