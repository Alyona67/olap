INSERT INTO dim_product
SELECT * FROM read_csv_auto('data/raw/dim_product.csv');

INSERT INTO dim_store
SELECT * FROM read_csv_auto('data/raw/dim_store.csv');

INSERT INTO dim_date
SELECT * FROM read_csv_auto('data/raw/dim_date.csv');

INSERT INTO dim_customer
SELECT * FROM read_csv_auto('data/raw/dim_customer.csv');

INSERT INTO dim_employee
SELECT * FROM read_csv_auto('data/raw/dim_employee.csv');

INSERT INTO dim_promotion
SELECT * FROM read_csv_auto('data/raw/dim_promotion.csv');

INSERT INTO fact_sales
SELECT * FROM read_csv_auto('data/raw/fact_sales.csv');

INSERT INTO fact_returns
SELECT * FROM read_csv_auto('data/raw/fact_returns.csv');

INSERT INTO fact_inventory
SELECT * FROM read_csv_auto('data/raw/fact_inventory.csv');