import duckdb
from pathlib import Path
import sys

DB_PATH = "retail.duckdb"
LOG_FILE = "etl/log.txt"

FILES = {
    "dim_product": "data/raw/dim_product.csv",
    "dim_store": "data/raw/dim_store.csv",
    "dim_date": "data/raw/dim_date.csv",
    "dim_customer": "data/raw/dim_customer.csv",
    "dim_employee": "data/raw/dim_employee.csv",
    "dim_promotion": "data/raw/dim_promotion.csv",
    "fact_sales": "data/raw/fact_sales.csv",
    "fact_returns": "data/raw/fact_returns.csv",
    "fact_inventory": "data/raw/fact_inventory.csv",
}

def log(message, file=LOG_FILE):
    """Записывает сообщение в лог-файл и выводит в консоль."""
    with open(file, "a", encoding="utf-8") as f:
        f.write(message + "\n")
    print(message)

def run_etl():
    open(LOG_FILE, "w", encoding="utf-8").close()
    log("ЗАПУСК ELT-ПРОЦЕССА")

    con = duckdb.connect(DB_PATH)

    log("\n[1/4] Очистка старых таблиц...")
    tables = list(FILES.keys())
    for t in tables:
        con.execute(f"DROP TABLE IF EXISTS {t}")
    log("      Таблицы удалены (если были).")

    log("\n[2/4] Загрузка справочников...")
    con.execute("""
        CREATE TABLE dim_product (product_id INTEGER PRIMARY KEY, product_name VARCHAR, category VARCHAR, brand VARCHAR);
        CREATE TABLE dim_store (store_id INTEGER PRIMARY KEY, store_name VARCHAR, city VARCHAR, region VARCHAR);
        CREATE TABLE dim_date (date_id INTEGER PRIMARY KEY, full_date DATE, year INTEGER, month INTEGER, month_name VARCHAR, day_of_week INTEGER);
        CREATE TABLE dim_customer (customer_id INTEGER PRIMARY KEY, customer_name VARCHAR, city VARCHAR, segment VARCHAR, gender VARCHAR);
        CREATE TABLE dim_employee (employee_id INTEGER PRIMARY KEY, employee_name VARCHAR, position VARCHAR, store_id INTEGER);
        CREATE TABLE dim_promotion (promotion_id INTEGER PRIMARY KEY, promotion_name VARCHAR, promo_type VARCHAR, discount_pct INTEGER);
    """)
    
    for t in ["dim_product", "dim_store", "dim_date", "dim_customer", "dim_employee", "dim_promotion"]:
        con.execute(f"INSERT INTO {t} SELECT * FROM read_csv_auto('{FILES[t]}')")
        count = con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        log(f"      {t}: загружено {count} строк.")

    log("\n[3/4] Загрузка фактов...")
    con.execute("""
        CREATE TABLE fact_sales (sale_id INTEGER, date_id INTEGER, store_id INTEGER, product_id INTEGER, customer_id INTEGER, employee_id INTEGER, promotion_id INTEGER, qty INTEGER, amount DECIMAL(10,2));
        CREATE TABLE fact_returns (return_id INTEGER PRIMARY KEY, sale_id INTEGER, date_id INTEGER, store_id INTEGER, product_id INTEGER, qty INTEGER, amount DECIMAL(10,2), reason VARCHAR);
        CREATE TABLE fact_inventory (inventory_id INTEGER PRIMARY KEY, date_id INTEGER, store_id INTEGER, product_id INTEGER, qty_on_hand INTEGER);
    """)

    for t in ["fact_sales", "fact_returns", "fact_inventory"]:
        con.execute(f"INSERT INTO {t} SELECT * FROM read_csv_auto('{FILES[t]}')")
        count = con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        log(f"      {t}: загружено {count} строк.")

    log("\n[4/4] Проверки качества данных...")
    
    errors = []


    log("      Проверка 1: Пустые ключи (NULL)...")
    null_checks = [
        ("fact_sales.date_id", "SELECT COUNT(*) FROM fact_sales WHERE date_id IS NULL"),
        ("fact_sales.amount", "SELECT COUNT(*) FROM fact_sales WHERE amount IS NULL"),
        ("fact_sales.store_id", "SELECT COUNT(*) FROM fact_sales WHERE store_id IS NULL"),
        ("fact_returns.sale_id", "SELECT COUNT(*) FROM fact_returns WHERE sale_id IS NULL"),
    ]
    for name, query in null_checks:
        bad = con.execute(query).fetchone()[0]
        if bad > 0:
            errors.append(f"Найдены NULL в {name}: {bad} строк")
        else:
            log(f"         OK: {name} без NULL")


    log("      Проверка 2: Странные диапазоны (qty < 0)...")
    bad_qty = con.execute("SELECT COUNT(*) FROM fact_sales WHERE qty < 0").fetchone()[0]
    if bad_qty > 0:
        errors.append(f"Найдено отрицательное количество (qty < 0): {bad_qty} строк")
    else:
        log("         OK: Отрицательных qty нет.")


    log("      Проверка 3: Дубли (sale_id + product_id)...")
    dup = con.execute("""
        SELECT COUNT(*) FROM (
            SELECT sale_id, product_id, COUNT(*) as c
            FROM fact_sales
            GROUP BY sale_id, product_id
            HAVING COUNT(*) > 1
        )
    """).fetchone()[0]
    if dup > 0:
        errors.append(f"Найдены дубли по (sale_id + product_id): {dup}")
    else:
        log("         OK: Дублей не найдено.")


    log("      Проверка 4: Сироты (ссылочная целостность)...")
    orphans = con.execute("""
        SELECT COUNT(*) 
        FROM fact_sales f 
        LEFT JOIN dim_store s ON f.store_id = s.store_id 
        WHERE s.store_id IS NULL
    """).fetchone()[0]
    if orphans > 0:
        errors.append(f"Найдены сироты в fact_sales (store_id): {orphans}")
    else:
        log("         OK: Сирот в fact_sales (store_id) нет.")


    if errors:
        log("\n" + "❌ Загрузка остановлена. Найдены ошибки:")
        for err in errors:
            log(f"  - {err}")
        con.close()
        sys.exit(1) 
    else:
        log("\n" + "✅ Все проверки пройдены успешно.")
        log("Данные готовы к анализу.")
        
        revenue = con.execute("SELECT SUM(amount) FROM fact_sales").fetchone()[0]
        log(f"Главная метрика (Выручка): {revenue}")
    
    con.close()

if __name__ == "__main__":
    run_etl()