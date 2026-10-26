import duckdb

con = duckdb.connect("retail.duckdb")
print(con.execute("SELECT customer_id, segment, valid_from, valid_to, is_current FROM dim_customer_scd2 WHERE customer_id = 1").df())