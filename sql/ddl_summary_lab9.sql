DROP TABLE IF EXISTS sales_summary;

CREATE TABLE sales_summary (
    date_id UInt32,
    store_id UInt32,
    amount_sum Decimal(10, 2) 
) ENGINE = MergeTree() 
ORDER BY (date_id, store_id);

TRUNCATE TABLE sales_summary;

INSERT INTO sales_summary (date_id, store_id, amount_sum)
SELECT 
    date_id,
    store_id,
    SUM(amount) AS amount_sum
FROM fact_sales
GROUP BY date_id, store_id;