SELECT
  risk_level,
  COUNT(*) AS txn_count,
  SUM(isfraud) AS fraud_txns,
  ROUND(100.0 * SUM(isfraud) / COUNT(*), 2) AS fraud_rate_pct
FROM {{ ref('stg_transactions') }}
GROUP BY risk_level
ORDER BY fraud_rate_pct DESC
