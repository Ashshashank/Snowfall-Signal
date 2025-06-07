import duckdb
import pandas as pd

# ✅ Correct path to DuckDB file
conn = duckdb.connect("analytics/plaid_fraud.duckdb")

# Preview the aggregated fraud data
df = pd.read_sql_query("SELECT * FROM agg_fraud_by_step", conn)

# Show the first few rows
print("\n--- First 10 rows ---")
print(df.head(10))

# Show summary stats
print("\n--- Summary Statistics ---")
print(df.describe())

conn.close()
