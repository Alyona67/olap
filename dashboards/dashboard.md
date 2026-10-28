# Дашборд Metabase (лаба 10)

Ссылка: http://localhost:3000
Источник данных: ClickHouse OLAP

## Описание дашборда
Дашборд состоит из 4 виджетов, которые отвечают на бизнес-вопросы из паспорта (лаба 2):
1. Выручка по месяцам (Line chart) — динамика продаж.
2. Выручка по магазинам (Bar chart) — сравнение точек.
3. Товары по акции и без (Pie chart) — доля акционных продаж.
4. Топ категорий и брендов (Bar chart) — лидеры ассортимента.

Добавлен фильтр по датам (Date picker), который позволяет выбрать период.

## SQL-запросы виджетов:

### 1. Выручка по месяцам, 2. Выручка по магазинам, 3. Товары по акции и без, 4. Топ категорий и брендов, 5. Главная метрика
```sql
SELECT 
    d.month_name AS month_label,
    d.month AS month_num,
    SUM(f.amount) AS revenue
FROM fact_sales f
JOIN dim_date d ON f.date_id = d.date_id
GROUP BY d.month, d.month_name
ORDER BY d.month


SELECT 
    s.store_name, 
    SUM(f.amount) AS revenue
FROM fact_sales f
JOIN dim_store s ON f.store_id = s.store_id
GROUP BY s.store_name
ORDER BY revenue DESC
LIMIT 10


SELECT 
    CASE 
        WHEN isNull(promotion_id) OR promotion_id = 0 THEN 'Без акции' 
        ELSE 'С акцией' 
    END AS promo_flag,
    SUM(amount) AS revenue
FROM fact_sales
GROUP BY promo_flag


SELECT SUM(amount) AS total_revenue
FROM fact_sales

