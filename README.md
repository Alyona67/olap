# OLAP 

Лабораторная 301. Стенд и сырьё.


- ФИО: Кудревич Алена Юрьевна
- Группа: ПИ-231
- Домен: розница

## Как поднять стенд (ClickHouse + Metabase)

1. Запустить Docker Desktop.

2. Открыть терминал и перейти в папку стенда:
cd C:\Users\User\Downloads_stand_stand

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

Лежит в папке **`data/raw/`**. Учебный sample курса по домену «розница».

| Файл | Поля | Описание |
|------|------|----------|
| `dim_product.csv` | `product_id, product_name, category, brand` | Справочник товаров (8 шт.) |
| `dim_store.csv` | `store_id, store_name, city, region` | Справочник магазинов (5 шт.) |
| `dim_date.csv` | `date_id, full_date, year, month, month_name, day_of_week` | Справочник дат (8 шт.) |
| `fact_sales.csv` | `sale_id, date_id, store_id, product_id, qty, amount` | Продажи (15 шт.) |

**Схема модели:** «звезда». В центре `fact_sales`, вокруг измерения `dim_product`, `dim_store`, `dim_date`.

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
- `python query.py` → читаются 4 CSV из `data/raw/`