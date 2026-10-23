import pandas as pd
from pathlib import Path

# Locate the project data folder
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def generate_customers():
    customers = {
        "customer_id": [f"CUST{i:04d}" for i in range(1, 11)],
        "city": [
            "Chennai",
            "Coimbatore",
            "Madurai",
            "Trichy",
            "Salem",
            "Chennai",
            "Erode",
            "Madurai",
            "Trichy",
            "Salem",
        ],
        "total_orders": [12, 5, 20, 8, 3, 15, 7, 10, 4, 18],
        "total_spend": [
            6500, 2200, 12000, 4000, 900,
            7800, 3100, 5200, 1500, 9500,
        ],
    }

    df = pd.DataFrame(customers)
    output_file = DATA_DIR / "customers.csv"
    df.to_csv(output_file, index=False)

    print("Customer dataset created successfully!")
    print(f"File location: {output_file}")
    print(f"Total customers: {len(df)}")
    print("\nFirst five rows:")
    print(df.head())

if __name__ == "__main__":
    generate_customers()

