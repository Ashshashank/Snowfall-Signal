SELECT
  *,
  CASE WHEN isfraud = 1 THEN 'fraud' ELSE 'non_fraud' END AS fraud_label,
  CASE 
    WHEN amount > 1000000 THEN 'high'
    WHEN amount > 100000 THEN 'medium'
    ELSE 'low'
  END AS risk_level
FROM main."raw_transactions"