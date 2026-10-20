SELECT SUM(amount) AS total_revenue
FROM read_csv_auto('data/raw/fact_sales.csv');