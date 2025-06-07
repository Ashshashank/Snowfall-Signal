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

# Streamlit settings
st.set_page_config(page_title="Plaid Fraud Detection", layout="wide")
st.title("🚨 Plaid Fraud Detection Dashboard")

# ✅ NEW: Connect to DuckDB from project root
conn = duckdb.connect("/Users/shashank/Documents/GitHub/Snowfall-Signal/analytics/plaid_fraud.duckdb")

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
