CREATE TABLE IF NOT EXISTS dim_product (
    product_id UInt32, product_name String, category String, brand String
) ENGINE = MergeTree() ORDER BY product_id;

CREATE TABLE IF NOT EXISTS dim_store (
    store_id UInt32, store_name String, city String, region String
) ENGINE = MergeTree() ORDER BY store_id;

CREATE TABLE IF NOT EXISTS dim_date (
    date_id UInt32, full_date Date, year UInt16, month UInt8, month_name String, day_of_week UInt8
) ENGINE = MergeTree() ORDER BY date_id;

CREATE TABLE IF NOT EXISTS dim_customer (
    customer_id UInt32, customer_name String, city String, segment String, gender String
) ENGINE = MergeTree() ORDER BY customer_id;

CREATE TABLE IF NOT EXISTS dim_employee (
    employee_id UInt32, employee_name String, position String, store_id UInt32
) ENGINE = MergeTree() ORDER BY employee_id;

CREATE TABLE IF NOT EXISTS dim_promotion (
    promotion_id UInt32, promotion_name String, promo_type String, discount_pct UInt8
) ENGINE = MergeTree() ORDER BY promotion_id;

CREATE TABLE IF NOT EXISTS fact_sales (
    sale_id UInt32,
    date_id UInt32,
    store_id UInt32,
    product_id UInt32,
    customer_id UInt32,
    employee_id UInt32,
    promotion_id Nullable(UInt32),
    qty UInt16,
    amount Decimal(10, 2)
) ENGINE = MergeTree() ORDER BY (date_id, store_id, sale_id);

CREATE TABLE IF NOT EXISTS fact_returns (
    return_id UInt32, sale_id UInt32, date_id UInt32, store_id UInt32, 
    product_id UInt32, qty UInt16, amount Decimal(10, 2), reason String
) ENGINE = MergeTree() ORDER BY (date_id, store_id);

CREATE TABLE IF NOT EXISTS fact_inventory (
    inventory_id UInt32, date_id UInt32, store_id UInt32, product_id UInt32, qty_on_hand Int32
) ENGINE = MergeTree() ORDER BY (date_id, store_id, product_id);