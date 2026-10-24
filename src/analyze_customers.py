import pandas as pd
from pathlib import Path

# Project folders
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CUSTOMERS_FILE = DATA_DIR / "customers.csv"
ORDERS_FILE = DATA_DIR / "orders.csv"
REPORT_DIR = BASE_DIR / "reports"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Load customer data
df = pd.read_csv(CUSTOMERS_FILE)

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
print(
    top_customers[
        ["customer_id", "city", "total_orders", "total_spend"]
    ]
)

top_customers.to_csv(
    REPORT_DIR / "customer_analysis.csv",
    index=False
)

# 7. RFM analysis using orders.csv
print("\n7. RFM Customer Analysis:")

if not ORDERS_FILE.exists():
    print("orders.csv not found. RFM analysis skipped.")
else:
    orders = pd.read_csv(ORDERS_FILE)

    required_columns = {
        "customer_id",
        "order_date",
        "order_amount",
    }

    if not required_columns.issubset(orders.columns):
        print("RFM skipped: orders.csv has missing required columns.")
    else:
        orders["order_date"] = pd.to_datetime(
            orders["order_date"], errors="coerce"
        )
        orders["order_amount"] = pd.to_numeric(
            orders["order_amount"], errors="coerce"
        )

        orders = orders.dropna(
            subset=["customer_id", "order_date", "order_amount"]
        )

        if orders.empty:
            print("RFM skipped: no valid order records.")
        else:
            reference_date = (
                orders["order_date"].max() + pd.Timedelta(days=1)
            )

            rfm = orders.groupby("customer_id").agg(
                last_order_date=("order_date", "max"),
                frequency=("order_date", "count"),
                monetary=("order_amount", "sum"),
            ).reset_index()

            rfm["recency"] = (
                reference_date - rfm["last_order_date"]
            ).dt.days

            # Merge with all customers
            rfm = df[["customer_id"]].merge(
                rfm, on="customer_id", how="left"
            )

            rfm["recency"] = rfm["recency"].fillna(999).astype(int)
            rfm["frequency"] = rfm["frequency"].fillna(0).astype(int)
            rfm["monetary"] = rfm["monetary"].fillna(0)

            def segment_customer(row):
                if row["frequency"] == 0:
                    return "No Recorded Orders"
                elif row["recency"] <= 30 and row["frequency"] >= 3:
                    return "Active Loyal Customer"
                elif row["recency"] <= 30:
                    return "Recent Customer"
                elif row["recency"] > 60:
                    return "Potentially Inactive"
                else:
                    return "Needs Engagement"

            rfm["customer_segment"] = rfm.apply(
                segment_customer, axis=1
            )

            rfm = rfm.drop(columns=["last_order_date"])

            rfm.to_csv(
                REPORT_DIR / "rfm_customer_analysis.csv",

                if __name__ == "__main__":
    print("Customer analysis script completed.")
