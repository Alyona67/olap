DROP TABLE IF EXISTS fact_inventory;
DROP TABLE IF EXISTS fact_returns;
DROP TABLE IF EXISTS fact_sales;
DROP TABLE IF EXISTS dim_promotion;
DROP TABLE IF EXISTS dim_employee;
DROP TABLE IF EXISTS dim_customer;
DROP TABLE IF EXISTS dim_date;
DROP TABLE IF EXISTS dim_store;
DROP TABLE IF EXISTS dim_product;


CREATE TABLE dim_product (
    product_id    INTEGER PRIMARY KEY,
    product_name  VARCHAR NOT NULL,
    category      VARCHAR,
    brand         VARCHAR
);


CREATE TABLE dim_store (
    store_id    INTEGER PRIMARY KEY,
    store_name  VARCHAR NOT NULL,
    city        VARCHAR,
    region      VARCHAR
);


CREATE TABLE dim_date (
    date_id      INTEGER PRIMARY KEY,
    full_date    DATE NOT NULL,
    year         INTEGER,
    month        INTEGER,
    month_name   VARCHAR,
    day_of_week  INTEGER
);


CREATE TABLE dim_customer (
    customer_id    INTEGER PRIMARY KEY,
    customer_name  VARCHAR NOT NULL,
    city           VARCHAR,
    segment        VARCHAR,
    gender         VARCHAR
);


CREATE TABLE dim_employee (
    employee_id    INTEGER PRIMARY KEY,
    employee_name  VARCHAR NOT NULL,
    position       VARCHAR,
    store_id       INTEGER
);


CREATE TABLE dim_promotion (
    promotion_id    INTEGER PRIMARY KEY,
    promotion_name  VARCHAR NOT NULL,
    promo_type      VARCHAR,
    discount_pct    INTEGER
);


CREATE TABLE fact_sales (
    sale_id        INTEGER NOT NULL,
    date_id        INTEGER NOT NULL,
    store_id       INTEGER NOT NULL,
    product_id     INTEGER NOT NULL,
    customer_id    INTEGER,
    employee_id    INTEGER,
    promotion_id   INTEGER,
    qty            INTEGER NOT NULL,
    amount         DECIMAL(10, 2) NOT NULL
);


CREATE TABLE fact_returns (
    return_id     INTEGER PRIMARY KEY,
    sale_id       INTEGER NOT NULL,
    date_id       INTEGER NOT NULL,
    store_id      INTEGER NOT NULL,
    product_id    INTEGER NOT NULL,
    qty           INTEGER NOT NULL,
    amount        DECIMAL(10, 2) NOT NULL,
    reason        VARCHAR
);


CREATE TABLE fact_inventory (
    inventory_id  INTEGER PRIMARY KEY,
    date_id       INTEGER NOT NULL,
    store_id      INTEGER NOT NULL,
    product_id    INTEGER NOT NULL,
    qty_on_hand   INTEGER NOT NULL
);