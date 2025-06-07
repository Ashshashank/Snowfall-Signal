SELECT
  CAST(step AS INTEGER) AS day,
  COUNT(*) AS txn_count,
  SUM(CASE WHEN isfraud = 1 THEN 1 ELSE 0 END) AS fraud_count,
  ROUND(100.0 * SUM(CASE WHEN isfraud = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS fraud_rate_pct
FROM {{ ref('stg_transactions') }}
GROUP BY day
ORDER BY day