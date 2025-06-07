import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set display options for better output
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

print("=" * 80)
print("PLAID FRAUD DETECTION PIPELINE - DATA CLEANING & EXPLORATION")
print("=" * 80)

# Load the dataset
print("\n1. LOADING DATASET")
print("-" * 40)
try:
    # Assuming the dataset is downloaded as 'PS_20174392719_1491204439457_log.csv'
    # You'll need to update this path to match your downloaded file
    df = pd.read_csv('/Users/shashank/Documents/GitHub/Snowfall-Signal/data/PS_20174392719_1491204439457_log.csv')
    print(f"✅ Dataset loaded successfully!")
    print(f"📊 Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
except FileNotFoundError:
    print("❌ Dataset file not found. Please ensure you've downloaded the PaySim dataset from Kaggle.")
    print("Expected filename: 'PS_20174392719_1491204439457_log.csv'")
    exit()

# Display basic info about the dataset
print(f"\n📋 Dataset Info:")
print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
print(f"Data types:")
for col, dtype in df.dtypes.items():
    print(f"  {col}: {dtype}")

print("\n2. INITIAL DATA EXPLORATION")
print("-" * 40)
print("First 5 rows:")
print(df.head())

print(f"\nColumn names:")
for i, col in enumerate(df.columns, 1):
    print(f"{i:2d}. {col}")

# Check for missing values
print("\n3. DATA QUALITY ASSESSMENT")
print("-" * 40)
missing_values = df.isnull().sum()
print("Missing values per column:")
for col, missing in missing_values.items():
    if missing > 0:
        print(f"  {col}: {missing:,} ({missing/len(df)*100:.2f}%)")
    else:
        print(f"  {col}: 0")

# Clean column names - convert to snake_case and remove special characters
print("\n4. CLEANING COLUMN NAMES")
print("-" * 40)
original_columns = df.columns.tolist()

# Convert column names to snake_case
def clean_column_name(col_name):
    # Remove special characters and convert to lowercase
    import re
    cleaned = re.sub(r'[^a-zA-Z0-9_]', '_', col_name.lower())
    # Remove multiple underscores
    cleaned = re.sub(r'_+', '_', cleaned)
    # Remove leading/trailing underscores
    cleaned = cleaned.strip('_')
    return cleaned

df.columns = [clean_column_name(col) for col in df.columns]

print("Column name changes:")
for orig, new in zip(original_columns, df.columns):
    if orig != new:
        print(f"  {orig} → {new}")
    else:
        print(f"  {orig} (no change)")

# Generate summary statistics
print("\n5. SUMMARY STATISTICS")
print("-" * 40)
print("Numerical columns summary:")
print(df.describe())

print(f"\nCategorical columns summary:")
categorical_cols = df.select_dtypes(include=['object']).columns
for col in categorical_cols:
    print(f"\n{col}:")
    print(df[col].value_counts().head(10))

# Fraud analysis - assuming there's an 'isFraud' column
print("\n6. FRAUD PATTERN ANALYSIS")
print("-" * 40)

# Check if fraud column exists (common names)
fraud_col = None
for col in df.columns:
    if 'fraud' in col.lower() or 'is_fraud' in col.lower():
        fraud_col = col
        break

if fraud_col:
    fraud_stats = df[fraud_col].value_counts()
    fraud_rate = df[fraud_col].mean() * 100
    
    print(f"Fraud Distribution:")
    print(f"  Non-fraud: {fraud_stats[0]:,} ({(fraud_stats[0]/len(df)*100):.2f}%)")
    print(f"  Fraud: {fraud_stats[1]:,} ({(fraud_stats[1]/len(df)*100):.2f}%)")
    print(f"  Overall fraud rate: {fraud_rate:.4f}%")
    
    # Fraud by transaction type
    if 'type' in df.columns:
        print(f"\nFraud by Transaction Type:")
        fraud_by_type = df.groupby('type')[fraud_col].agg(['count', 'sum', 'mean']).round(4)
        fraud_by_type['fraud_rate_%'] = fraud_by_type['mean'] * 100
        fraud_by_type.columns = ['total_transactions', 'fraud_count', 'fraud_rate', 'fraud_rate_%']
        print(fraud_by_type)
else:
    print("❗ Fraud column not found. Please check column names.")

# Transaction amount analysis
print("\n7. TRANSACTION AMOUNT ANALYSIS")
print("-" * 40)
amount_col = None
for col in df.columns:
    if 'amount' in col.lower():
        amount_col = col
        break

if amount_col:
    print(f"Transaction Amount Statistics:")
    print(f"  Mean: ${df[amount_col].mean():,.2f}")
    print(f"  Median: ${df[amount_col].median():,.2f}")
    print(f"  Min: ${df[amount_col].min():,.2f}")
    print(f"  Max: ${df[amount_col].max():,.2f}")
    print(f"  Std Dev: ${df[amount_col].std():,.2f}")
    
    # Amount distribution by fraud status
    if fraud_col:
        print(f"\nAmount Distribution by Fraud Status:")
        amount_by_fraud = df.groupby(fraud_col)[amount_col].agg(['mean', 'median', 'std']).round(2)
        print(amount_by_fraud)

# Time-based analysis (if step column exists representing time)
print("\n8. TEMPORAL PATTERN ANALYSIS")
print("-" * 40)
if 'step' in df.columns:
    print("Time Step Statistics:")
    print(f"  Total time steps: {df['step'].max()}")
    print(f"  Time range: Step {df['step'].min()} to {df['step'].max()}")
    
    # Transactions per time step
    transactions_per_step = df.groupby('step').size()
    print(f"  Avg transactions per step: {transactions_per_step.mean():.2f}")
    print(f"  Peak transactions in single step: {transactions_per_step.max():,}")

# Account balance analysis
print("\n9. ACCOUNT BALANCE ANALYSIS")
print("-" * 40)
balance_cols = [col for col in df.columns if 'balance' in col.lower()]
if balance_cols:
    for col in balance_cols:
        print(f"\n{col} Statistics:")
        print(f"  Mean: ${df[col].mean():,.2f}")
        print(f"  Accounts with zero balance: {(df[col] == 0).sum():,} ({(df[col] == 0).mean()*100:.2f}%)")
        print(f"  Negative balances: {(df[col] < 0).sum():,} ({(df[col] < 0).mean()*100:.2f}%)")

# Data quality checks
print("\n10. DATA QUALITY CHECKS")
print("-" * 40)

# Check for duplicates
duplicate_count = df.duplicated().sum()
print(f"Duplicate rows: {duplicate_count:,}")

# Check for obvious data inconsistencies
if amount_col and fraud_col:
    # Transactions with zero amounts
    zero_amount = (df[amount_col] == 0).sum()
    print(f"Zero amount transactions: {zero_amount:,} ({zero_amount/len(df)*100:.2f}%)")
    
    # Very high amount transactions (potential outliers)
    high_amount_threshold = df[amount_col].quantile(0.999)
    high_amount_count = (df[amount_col] > high_amount_threshold).sum()
    print(f"Very high amount transactions (>99.9th percentile): {high_amount_count:,}")
    print(f"High amount threshold: ${high_amount_threshold:,.2f}")

# Final data preparation
print("\n11. FINAL DATA PREPARATION")
print("-" * 40)

# Handle any missing values (if found)
if df.isnull().sum().sum() > 0:
    print("Handling missing values...")
    # For this dataset, we'll use appropriate strategies
    for col in df.columns:
        if df[col].isnull().sum() > 0:
            if df[col].dtype in ['int64', 'float64']:
                df[col].fillna(df[col].median(), inplace=True)
                print(f"  Filled {col} missing values with median")
            else:
                df[col].fillna(df[col].mode()[0], inplace=True)
                print(f"  Filled {col} missing values with mode")
else:
    print("✅ No missing values found - dataset is clean!")

# Add derived features for better analysis
print("\nAdding derived features...")

# Create transaction hour if step represents time
if 'step' in df.columns:
    df['transaction_hour'] = df['step'] % 24
    print("  Added 'transaction_hour' feature")

# Create amount bands for analysis
if amount_col:
    df['amount_band'] = pd.cut(df[amount_col], 
                              bins=[0, 100, 1000, 10000, 100000, float('inf')],
                              labels=['<$100', '$100-1K', '$1K-10K', '$10K-100K', '>$100K'])
    print("  Added 'amount_band' feature")

# Save the cleaned dataset
print("\n12. SAVING CLEANED DATASET")
print("-" * 40)
try:
    df.to_csv('staging_data.csv', index=False)
    print("✅ Cleaned dataset saved as 'staging_data.csv'")
    print(f"📁 File size: {pd.read_csv('staging_data.csv').memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    print(f"📊 Final shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
except Exception as e:
    print(f"❌ Error saving file: {e}")

print("\n" + "=" * 80)
print("DATA CLEANING & EXPLORATION COMPLETE!")
print("Next steps:")
print("1. Review staging_data.csv")
print("2. Design data pipeline architecture")
print("3. Build feature engineering pipeline")
print("4. Implement fraud detection models")
print("=" * 80)