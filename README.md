# OLAP 

Лабораторная 301. Стенд и сырьё.


- ФИО: Кудревич Алена Юрьевна
- Группа: ПИ-231
- Домен: розница

## Как поднять стенд (ClickHouse + Metabase)

1. Запустить Docker Desktop.

2. Открыть терминал и перейти в папку стенда:
cd C:\Users\User\Downloads\_stand\_stand

3. Поднять контейнеры в фоне:
docker compose up -d

4. Инициализировать ClickHouse (создать схему и загрузить sample):
wsl bash ./scripts/init_ch.sh

*(или через Git Bash: `bash scripts/init_ch.sh`)*
5. Проверить, что ClickHouse жив:
curl http://localhost:8123/ping

Должно вернуться `Ok.`

## Порты

| Сервис | Порт | URL |
|--------|------|-----|
| ClickHouse (HTTP) | 8123 | http://localhost:8123 |
| ClickHouse (native) | 9000 | — |
| Metabase | 3000 | http://localhost:3000 |

## Сырьё

Лежит в папке **`data/raw/`**. 

### Измерения (справочники)

| Файл | Поля | Строк | Описание |
|------|------|-------|----------|
| `dim_product.csv` | `product_id, product_name, category, brand` | 50 | Товары |
| `dim_store.csv` | `store_id, store_name, city, region` | 15 | Магазины |
| `dim_date.csv` | `date_id, full_date, year, month, month_name, day_of_week` | 365 | Календарь на 2024 |
| `dim_customer.csv` | `customer_id, customer_name, city, segment, gender` | 100 | Клиенты |
| `dim_employee.csv` | `employee_id, employee_name, position, store_id` | 30 | Сотрудники |
| `dim_promotion.csv` | `promotion_id, promotion_name, promo_type, discount_pct` | 10 | Акции |

### Факты (события)

| Файл | Поля | Строк | Описание |
|------|------|-------|----------|
| `fact_sales.csv` | `sale_id, date_id, store_id, product_id, customer_id, employee_id, promotion_id, qty, amount` | 5000 | Продажи |
| `fact_returns.csv` | `return_id, sale_id, date_id, store_id, product_id, qty, amount, reason` | 300 | Возвраты |
| `fact_inventory.csv` | `inventory_id, date_id, store_id, product_id, qty_on_hand` | 532 | Остатки на складе |

**Схема модели:** «звезда». В центре — три таблицы фактов, вокруг — шесть измерений.

**Одна строка `fact_sales`** = одна позиция в чеке (товар × количество × сумма в одной продаже).

## Инструменты

- **ClickHouse** — колоночная СУБД для OLAP (в Docker).
- **Metabase** — BI-инструмент для визуализации (в Docker).
- **DuckDB** — локальная аналитическая база на файлах (через Python, версия 1.5.6).
- **Python 3.14.7** + `.venv` с пакетами `duckdb`, `pandas`.

## Своя метрика (для следующих лаб)

В этом домене буду считать: **выручку по магазинам и категориям товаров за период**.
Ключевые вопросы:
- Какой магазин приносит больше всего выручки?
- Какие категории товаров продаются лучше?
- Как меняется выручка по месяцам?

## Проверка

- `curl http://localhost:8123/ping` → `Ok.`
- `python check.py` → `DuckDB version: [('v1.5.6',)]`
- `python query.py` → читаются 9 CSV из `data/raw/`


## Витрина в DuckDB (лаба 303)

База данных: `retail.duckdb` в корне проекта.

## Как собрать витрину

```powershell
python build_db.py
```

Скрипт выполняет:
1. `sql/ddl_duckdb.sql` — создаёт 9 таблиц (6 измерений + 3 факта).
2. `sql/load_duckdb.sql` — загружает данные из `data/raw/*.csv`.

## Структура `sql/`

| Файл | Что внутри |
|------|-----------|
| `ddl_duckdb.sql` | DDL — создание 9 таблиц |
| `load_duckdb.sql` | Загрузка CSV в таблицы |
| `checks_duckdb.sql` | 5 проверок витрины |

## Повторная загрузка - как не удвоить данные

При каждом запуске `build_db.py` в начале `ddl_duckdb.sql` выполняются команды `DROP TABLE IF EXISTS` для всех 9 таблиц. Это **удаляет старые таблицы и создаёт новые**, поэтому данные **не удваиваются** — каждый запуск даёт чистую витрину.

## Проверки

```powershell
python run_checks.py
```

Вывод сохраняется в `checks_output.txt`. Проверяется:
1. Число строк в таблицах (сверка с CSV).
2. Пустые ключи в `fact_sales` (должно быть 0).
3. Пустые ключи в `fact_returns` (должно быть 0).
4. Главная метрика: выручка, число строк, число чеков, средний чек.
5. Ссылочная целостность: все ли `product_id` из факта есть в `dim_product`.

## Зафиксированные числа (на момент сборки)

| Метрика | Значение |
|---------|----------|
| Выручка (`SUM amount`) | **1 713 407.05** |
| Строк в `fact_sales` | 5 989 |
| Уникальных чеков | 2 000 |
| Средний чек | 856.70 |
| Строк в `fact_returns` | 300 |
| Строк в `fact_inventory` | 528 |

