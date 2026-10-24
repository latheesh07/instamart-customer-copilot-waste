from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"

CUSTOMERS_FILE = DATA_DIR / "customers.csv"
ORDERS_FILE = DATA_DIR / "orders.csv"


def predict_lapse():
    if not CUSTOMERS_FILE.exists():
        raise FileNotFoundError(
            f"Customers dataset not found: {CUSTOMERS_FILE}"
        )

    customers = pd.read_csv(CUSTOMERS_FILE)

    if ORDERS_FILE.exists():
        orders = pd.read_csv(ORDERS_FILE)
    else:
        orders = pd.DataFrame()

    # Check whether usable customer activity data exists.
    if orders.empty:
        print(
            "Lapse prediction cannot run: orders.csv is missing "
            "or contains no order records."
        )
        print(
            "Add synthetic order history with customer IDs and "
            "order dates before training a lapse model."
        )
        return

    required_order_columns = {"customer_id", "order_date"}

    if not required_order_columns.issubset(orders.columns):
        raise ValueError(
            "orders.csv must contain customer_id and order_date columns."
        )

    if "customer_id" not in customers.columns:
        raise ValueError(
            "customers.csv must contain a customer_id column."
        )

    orders["order_date"] = pd.to_datetime(
        orders["order_date"], errors="coerce"
    )
    orders = orders.dropna(subset=["customer_id", "order_date"])

    if orders.empty:
        print("No valid order dates found in orders.csv.")
        return

    reference_date = orders["order_date"].max() + pd.Timedelta(days=1)

    activity = orders.groupby("customer_id").agg(
        last_order_date=("order_date", "max"),
        order_count=("order_date", "count"),
    ).reset_index()

    activity["days_since_last_order"] = (
        reference_date - activity["last_order_date"]
    ).dt.days

    # Demo rule: 30+ days since last order indicates inactivity.
    activity["lapse_label"] = (
        activity["days_since_last_order"] >= 30
    ).astype(int)

    result = customers.merge(activity, on="customer_id", how="left")
    result["days_since_last_order"] = (
        result["days_since_last_order"].fillna(999)
    )
    result["order_count"] = result["order_count"].fillna(0)
    result["lapse_label"] = result["lapse_label"].fillna(1).astype(int)

    result["lapse_risk"] = result["lapse_label"].map(
        {0: "Lower inactivity risk", 1: "Potentially inactive"}
    )

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = REPORT_DIR / "lapse_predictions.csv"
    result.to_csv(output_file, index=False)

    print(f"Demo lapse report saved to: {output_file}")
    print(result[[
        "customer_id",
        "days_since_last_order",
        "order_count",
        "lapse_risk",
    ]].to_string(index=False))


if __name__ == "__main__":
    predict_lapse()
