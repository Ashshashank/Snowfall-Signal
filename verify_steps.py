'''import duckdb

conn = duckdb.connect("analytics/plaid_fraud.duckdb")

print("🧪 Unique steps in raw_transactions:")
df = conn.execute("SELECT DISTINCT step FROM main.raw_transactions ORDER BY step").fetchdf()
print(df)

conn.close()
'''

import duckdb

# Connect to the DuckDB file
conn = duckdb.connect("analytics/plaid_fraud.duckdb")

# Run the SQL
query = "SELECT risk_level, COUNT(*) AS count FROM stg_transactions GROUP BY risk_level"
result = conn.execute(query).fetchdf()

print("🧠 Risk Level Counts:")
print(result)

conn.close()
