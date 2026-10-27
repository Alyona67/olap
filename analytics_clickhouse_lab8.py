import clickhouse_connect

client = clickhouse_connect.get_client(host='localhost', port=8123, username='admin', password='')

print("-" * 60)
print("ЗАПРОС 1: Выручка по месяцам")
print("-" * 60)
query1 = """
SELECT 
    d.year,
    d.month,
    d.month_name,
    SUM(f.amount) AS revenue,
    ROUND(SUM(f.amount) * 100.0 / SUM(SUM(f.amount)) OVER (PARTITION BY d.year), 2) AS share_pct
FROM fact_sales f
JOIN dim_date d ON f.date_id = d.date_id
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month
"""
df1 = client.query_df(query1)
print(df1.to_string(index=False))


print("\n" + "-" * 60)
print("ЗАПРОС 2: Лидеры брендов в категориях")
print("-" * 60)
query2 = """
SELECT 
    p.category,
    p.brand,
    SUM(f.amount) AS revenue,
    RANK() OVER (PARTITION BY p.category ORDER BY SUM(f.amount) DESC) AS brand_rank_in_category
FROM fact_sales f
JOIN dim_product p ON f.product_id = p.product_id
GROUP BY p.category, p.brand
QUALIFY brand_rank_in_category = 1
ORDER BY revenue DESC
"""
df2 = client.query_df(query2)
print(df2.to_string(index=False))


print("\n" + "-" * 60)
print("ЗАПРОС 3: Доля акционных товаров (в % и деньгах)")
print("-" * 60)
query3 = """
SELECT 
    CASE 
        WHEN f.promotion_id = 0 OR isNull(f.promotion_id) THEN 'Без акции' 
        ELSE 'С акцией' 
    END AS promo_flag,
    COUNT(*) AS total_items,
    SUM(f.amount) AS revenue,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS items_share_pct,
    ROUND(SUM(f.amount) * 100.0 / SUM(SUM(f.amount)) OVER (), 2) AS revenue_share_pct
FROM fact_sales f
GROUP BY promo_flag
"""
df3 = client.query_df(query3)
print(df3.to_string(index=False))