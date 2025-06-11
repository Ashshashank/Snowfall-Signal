'''import streamlit as st
import pandas as pd
import duckdb 
import plotly.express as px
import matplotlib.pyplot as plt

# Title
st.set_page_config(page_title="Plaid Fraud Detection", layout="wide")
st.title("🚨 Plaid Fraud Detection Dashboard")

# Connect to DuckDB — update the path if needed
conn = duckdb.connect("analytics/plaid_fraud.duckdb")
df = pd.read_sql_query("SELECT * FROM agg_fraud_by_step", conn)

# Load tables
fraud_by_step = pd.read_sql_query("SELECT * FROM agg_fraud_by_step", conn)
risk_summary = pd.read_sql_query("SELECT * FROM agg_risk_band_summary", conn)
all_txns = pd.read_sql_query("SELECT * FROM stg_transactions LIMIT 10000", conn)

st.subheader("📊 Distribution of Fraud Rate")
fig3, ax = plt.subplots(figsize=(4, 2))
ax.hist(fraud_by_step['fraud_rate_pct'].dropna(), bins=50)
st.pyplot(fig3)


# Fraud by Step Table
st.subheader("📋 Fraud by Step (Full Table)")
st.dataframe(fraud_by_step, use_container_width=True)

# Summary Stats
st.write("📊 Summary Stats for fraud_by_step")
st.write(fraud_by_step.describe())


# Trend Over Time
st.subheader("📈 Fraud Trend Over Time")
fig = px.histogram(fraud_by_step, x="fraud_rate_pct", title="Fraud Rate (%) by Step")
fig.update_layout(height=400, width=800)  # <- Add this
st.plotly_chart(fig, use_container_width=False)  # <- Change this


# Risk Band Summary
st.subheader("🧠 Risk Band vs Fraud Rate")
fig2 = px.bar(risk_summary, x="risk_level", y="fraud_rate_pct", color="risk_level", title="Fraud Rate by Risk Band")
st.write("📊 Risk Summary Table Preview", risk_summary)


st.plotly_chart(fig2, use_container_width=True)

# Raw Data Explorer
st.subheader("📋 Explore Sample Transactions")
st.dataframe(all_txns)

# Close connection
conn.close()
'''
import duckdb
import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import os

# Streamlit settings
st.set_page_config(page_title="Plaid Fraud Detection", layout="wide")
st.title("🚨 Plaid Fraud Detection Dashboard")

# Attempt to use the full DB path first (local dev)
LOCAL_DB_PATH = "/Users/shashank/Documents/GitHub/Snowfall-Signal/analytics/plaid_fraud.duckdb"
DEFAULT_DB_PATH = "plaid_fraud.duckdb"  # used in Streamlit Cloud

if os.path.exists(LOCAL_DB_PATH):
    conn = duckdb.connect(LOCAL_DB_PATH)
else:
    # ✅ Streamlit fallback: rebuild from CSV
    conn = duckdb.connect(DEFAULT_DB_PATH)
    if not os.path.exists(DEFAULT_DB_PATH):
        st.warning("Building DuckDB from CSV (first-time setup)...")
        conn.execute("""
            CREATE TABLE raw_transactions_sample AS
            SELECT * FROM read_csv_auto('analytics/seeds/raw_transactions_sample.csv')
        """)
        # Optional: create views to simulate dbt models
        conn.execute("""
            CREATE TABLE stg_transactions AS
            SELECT *,
                CASE WHEN isfraud = 1 THEN 'fraud' ELSE 'non_fraud' END AS fraud_label,
                CASE 
                    WHEN amount > 1000000 THEN 'high'
                    WHEN amount > 100000 THEN 'medium'
                    ELSE 'low'
                END AS risk_level
            FROM raw_transactions_sample
        """)
        conn.execute("""
            CREATE TABLE agg_fraud_by_step AS
            SELECT
                CAST(step AS INTEGER) AS day,
                COUNT(*) AS txn_count,
                SUM(CASE WHEN isfraud = 1 THEN 1 ELSE 0 END) AS fraud_count,
                ROUND(100.0 * SUM(CASE WHEN isfraud = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS fraud_rate_pct
            FROM stg_transactions
            GROUP BY day
            ORDER BY day
        """)
        conn.execute("""
            CREATE TABLE agg_risk_band_summary AS
            SELECT
                risk_level,
                COUNT(*) AS txn_count,
                SUM(isfraud) AS fraud_txns,
                ROUND(100.0 * SUM(isfraud) / COUNT(*), 2) AS fraud_rate_pct
            FROM stg_transactions
            GROUP BY risk_level
            ORDER BY fraud_rate_pct DESC
        """)

# Load tables
fraud_by_step = pd.read_sql_query("SELECT * FROM agg_fraud_by_step", conn)
risk_summary = pd.read_sql_query("SELECT * FROM agg_risk_band_summary", conn)
all_txns = pd.read_sql_query("SELECT * FROM stg_transactions LIMIT 10000", conn)

# Distribution plot
st.subheader("📊 Distribution of Fraud Rate")
fig3, ax = plt.subplots(figsize=(4, 2))
ax.hist(fraud_by_step['fraud_rate_pct'].dropna(), bins=50)
st.pyplot(fig3)

# Show table + summary
st.write("Fraud by Step", fraud_by_step)
st.write("Summary Stats for fraud_by_step")
st.write(fraud_by_step.describe())

# Fraud Trend
st.subheader("📈 Fraud Trend Over Time")
fig = px.histogram(fraud_by_step, x="fraud_rate_pct", title="Fraud Rate (%) by Step")
fig.update_layout(height=400, width=800)
st.plotly_chart(fig, use_container_width=False)

# Risk Band Summary
st.subheader("🧠 Risk Band vs Fraud Rate")
fig2 = px.bar(risk_summary, x="risk_level", y="fraud_rate_pct", color="risk_level", title="Fraud Rate by Risk Band")
st.plotly_chart(fig2, use_container_width=True)

# Sample Explorer
st.subheader("📋 Explore Sample Transactions")
st.dataframe(all_txns)

# Close conn
conn.close()
