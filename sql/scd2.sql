DROP TABLE IF EXISTS dim_customer_scd2;

CREATE TABLE dim_customer_scd2 (
    customer_id INTEGER,
    customer_name VARCHAR,
    city VARCHAR,
    segment VARCHAR,
    gender VARCHAR,
    valid_from DATE NOT NULL,
    valid_to DATE,
    is_current BOOLEAN DEFAULT TRUE
);


INSERT INTO dim_customer_scd2 (customer_id, customer_name, city, segment, gender, valid_from, valid_to, is_current)
SELECT 
    customer_id, 
    customer_name, 
    city, 
    segment, 
    gender, 
    DATE '2024-01-01' AS valid_from,
    NULL AS valid_to,
    TRUE AS is_current
FROM read_csv_auto('data/raw/dim_customer.csv')
WHERE customer_id <= 100;


UPDATE dim_customer_scd2
SET valid_to = DATE '2024-05-31',
    is_current = FALSE
WHERE customer_id = 1 AND is_current = TRUE;


INSERT INTO dim_customer_scd2 (customer_id, customer_name, city, segment, gender, valid_from, valid_to, is_current)
SELECT 
    customer_id, 
    customer_name, 
    city, 
    'VIP' AS segment, 
    gender, 
    DATE '2024-06-01' AS valid_from,
    NULL AS valid_to,
    TRUE AS is_current
FROM dim_customer_scd2
WHERE customer_id = 1 AND is_current = FALSE AND valid_to = DATE '2024-05-31';