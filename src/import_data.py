import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DB_PATH = DATA_DIR / "instamart.db"


def import_customers(conn):
    file_path = DATA_DIR / "customers.csv"

    with file_path.open("r", newline="", encoding="utf-8-sig") as file:
        rows = list(csv.DictReader(file))

    conn.executemany(
        """
        INSERT OR REPLACE INTO customers
        (customer_id, city, total_orders, total_spend)
        VALUES (?, ?, ?, ?)
        """,
        [
            (
                row["customer_id"],
                row["city"],
                int(row["total_orders"]),
                float(row["total_spend"]),
            )
            for row in rows
        ],
    )
    print(f"Customers imported: {len(rows)}")


def import_support_tickets(conn):
    file_path = DATA_DIR / "support_tickets.csv"

    with file_path.open("r", newline="", encoding="utf-8-sig") as file:
        rows = list(csv.DictReader(file))

    # Avoid duplicates by replacing the existing demo ticket rows.
    conn.execute("DELETE FROM support_tickets")

    conn.executemany(
        """
        INSERT INTO support_tickets (ticket_text, category)
        VALUES (?, ?)
        """,
        [
            (row["ticket_text"], row["category"])
            for row in rows
        ],
    )
    print(f"Support tickets imported: {len(rows)}")


def main():
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DB_PATH}. Create it first."
        )

    with sqlite3.connect(DB_PATH) as conn:
        import_customers(conn)
        import_support_tickets(conn)

    print("CSV import completed successfully!")


if __name__ == "__main__":
    main()

