import pandas as pd
from pathlib import Path

# Project folders
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "customers.csv"
REPORT_DIR = BASE_DIR / "reports"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Load customer data
df = pd.read_csv(DATA_FILE)

print("=" * 50)
print("INSTAMART CUSTOMER DATA ANALYSIS")
print("=" * 50)

# 1. Total customers
print("\n1. Total Customers:", len(df))

# 2. Total orders
print("2. Total Orders:", df["total_orders"].sum())

# 3. Total revenue
print("3. Total Customer Spending: ₹", df["total_spend"].sum())

# 4. Average spending
print(
    "4. Average Spending per Customer: ₹",
    round(df["total_spend"].mean(), 2)
)

# 5. City-wise customer count
print("\n5. Customers by City:")
print(df["city"].value_counts())

# 6. Top 5 customers by spending
print("\n6. Top Customers by Spending:")
top_customers = df.nlargest(5, "total_spend")
print(top_customers[
    ["customer_id", "city", "total_orders", "total_spend"]
])

# Save analysis report
report_file = REPORT_DIR / "customer_analysis.csv"
top_customers.to_csv(report_file, index=False)

print("\nReport saved successfully!")
print("Location:", report_file)