SELECT 
    d.year,
    d.month,
    d.month_name,
    SUM(f.amount) AS revenue,
    ROUND(SUM(f.amount) * 100.0 / SUM(SUM(f.amount)) OVER (PARTITION BY d.year), 2) AS share_pct
FROM read_csv_auto('data/raw/fact_sales.csv') f
JOIN read_csv_auto('data/raw/dim_date.csv') d ON f.date_id = d.date_id
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month;


SELECT 
    p.category,
    p.brand,
    SUM(f.amount) AS revenue,
    RANK() OVER (PARTITION BY p.category ORDER BY SUM(f.amount) DESC) AS brand_rank_in_category
FROM read_csv_auto('data/raw/fact_sales.csv') f
JOIN read_csv_auto('data/raw/dim_product.csv') p ON f.product_id = p.product_id
GROUP BY p.category, p.brand
QUALIFY brand_rank_in_category = 1
ORDER BY revenue DESC;


SELECT 
    CASE 
        WHEN f.promotion_id IS NULL THEN 'Без акции' 
        ELSE 'С акцией' 
    END AS promo_flag,
    COUNT(DISTINCT f.sale_id) AS total_checks,
    SUM(f.amount) AS revenue,
    ROUND(SUM(f.amount) / COUNT(DISTINCT f.sale_id), 2) AS avg_check,
    ROUND(COUNT(DISTINCT f.sale_id) * 100.0 / SUM(COUNT(DISTINCT f.sale_id)) OVER (), 2) AS checks_share_pct,
    ROUND(SUM(f.amount) * 100.0 / SUM(SUM(f.amount)) OVER (), 2) AS revenue_share_pct
FROM read_csv_auto('data/raw/fact_sales.csv') f
GROUP BY promo_flag;


SELECT 
    COUNT(*) AS total_rows,
    COUNT(DISTINCT sale_id) AS total_checks
FROM read_csv_auto('data/raw/fact_sales.csv');