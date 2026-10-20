-- Число строк в таблицах (сверить с CSV)
SELECT 'dim_product' AS table_name, COUNT(*) AS rows_count FROM dim_product
UNION ALL SELECT 'dim_store', COUNT(*) FROM dim_store
UNION ALL SELECT 'dim_date', COUNT(*) FROM dim_date
UNION ALL SELECT 'dim_customer', COUNT(*) FROM dim_customer
UNION ALL SELECT 'dim_employee', COUNT(*) FROM dim_employee
UNION ALL SELECT 'dim_promotion', COUNT(*) FROM dim_promotion
UNION ALL SELECT 'fact_sales', COUNT(*) FROM fact_sales
UNION ALL SELECT 'fact_returns', COUNT(*) FROM fact_returns
UNION ALL SELECT 'fact_inventory', COUNT(*) FROM fact_inventory;

-- Пустые ключи в fact_sales 
SELECT 'NULL date_id'    AS check_name, COUNT(*) AS bad_rows FROM fact_sales WHERE date_id IS NULL
UNION ALL SELECT 'NULL store_id',   COUNT(*) FROM fact_sales WHERE store_id IS NULL
UNION ALL SELECT 'NULL product_id', COUNT(*) FROM fact_sales WHERE product_id IS NULL
UNION ALL SELECT 'NULL qty',        COUNT(*) FROM fact_sales WHERE qty IS NULL
UNION ALL SELECT 'NULL amount',     COUNT(*) FROM fact_sales WHERE amount IS NULL;

-- Пустые ключи в fact_returns
SELECT 'NULL sale_id'    AS check_name, COUNT(*) AS bad_rows FROM fact_returns WHERE sale_id IS NULL
UNION ALL SELECT 'NULL date_id',    COUNT(*) FROM fact_returns WHERE date_id IS NULL
UNION ALL SELECT 'NULL store_id',   COUNT(*) FROM fact_returns WHERE store_id IS NULL
UNION ALL SELECT 'NULL product_id', COUNT(*) FROM fact_returns WHERE product_id IS NULL;

-- Главная метрика 
SELECT 
    SUM(amount) AS total_revenue,
    COUNT(*) AS total_rows,
    COUNT(DISTINCT sale_id) AS total_checks,
    ROUND(SUM(amount) / COUNT(DISTINCT sale_id), 2) AS avg_check
FROM fact_sales;
