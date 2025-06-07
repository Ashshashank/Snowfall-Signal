import duckdb

# Connect to your DuckDB file
conn = duckdb.connect("analytics/plaid_fraud.duckdb")

# Print all available tables
print("🔍 Available DuckDB tables:")
print(conn.execute("SHOW TABLES").fetchdf())

conn.close()
