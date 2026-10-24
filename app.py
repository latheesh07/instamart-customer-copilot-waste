from pathlib import Path
import sys
import sqlite3
import pandas as pd
import streamlit as st

# Project paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
REPORT_DIR = BASE_DIR / "reports"
MODEL_DIR = BASE_DIR / "models"
SRC_DIR = BASE_DIR / "src"

sys.path.insert(0, str(SRC_DIR))

st.set_page_config(
    page_title="Instamart Customer Copilot",
    page_icon="ðŸ›’",
    layout="wide",
)

st.title("ðŸ›’ Instamart Customer Intelligence")
st.subheader("Customer Analytics & Support Copilot")

st.info(
    "Student project prototype using synthetic customer data "
    "and a fictional demo policy. Not connected to Instamart."
)

# Sidebar navigation
page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Customer Analytics",
        "Lapse Prediction",
        "SQL Analytics",
        "Ticket Classifier",
        "Policy Assistant",
        "Refund Requests",
    ],
)
# Initialize SQLite database
DB_PATH = DATA_DIR / "instamart.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"
def initialize_database():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        if SCHEMA_PATH.exists():
            schema = SCHEMA_PATH.read_text(encoding="utf-8")

            statements = [
                statement.strip()
                for statement in schema.split(";")
                if statement.strip().upper().startswith("CREATE TABLE")
            ]

            for statement in statements:
                conn.execute(statement)

        customers_file = DATA_DIR / "customers.csv"
        if customers_file.exists():
            customers = pd.read_csv(customers_file)

            customers.to_sql(
                "customers",
                conn,
                if_exists="replace",
                index=False,
            )

        tickets_file = DATA_DIR / "support_tickets.csv"
        if tickets_file.exists():
            tickets = pd.read_csv(tickets_file)

            tickets.to_sql(
                "support_tickets",
                conn,
                if_exists="replace",
                index=False,
            )


initialize_database()


# Dashboard
if page == "Dashboard":
    st.header("Project Overview")

    customers_file = DATA_DIR / "customers.csv"
    tickets_file = DATA_DIR / "support_tickets.csv"
    segments_file = REPORT_DIR / "customer_segments.csv"

    col1, col2, col3 = st.columns(3)

    if customers_file.exists():
        customers = pd.read_csv(customers_file)
        col1.metric("Sample Customers", len(customers))
        col2.metric("Sample Orders", int(customers["total_orders"].sum()))
        col3.metric(
            "Sample Spending",
            f"â‚¹{customers['total_spend'].sum():,.0f}",
        )
    else:
        st.warning("Customer dataset not found.")

    st.markdown("### Available Modules")
    st.write("- Customer data analysis")
    st.write("- Machine learning customer segmentation")
    st.write("- Customer support ticket classification")
    st.write("- Policy-based question answering")
    st.write("- Refund request recording")

    if tickets_file.exists():
        st.caption("Sample support tickets are available.")

    if segments_file.exists():
        st.caption("Customer segmentation results are available.")


# Customer Analytics
elif page == "Customer Analytics":
    st.header("ðŸ“Š Customer Analytics")

    customer_file = DATA_DIR / "customers.csv"
    segment_file = REPORT_DIR / "customer_segments.csv"

    if customer_file.exists():
        df = pd.read_csv(customer_file)

        col1, col2 = st.columns(2)
        col1.metric("Customers", len(df))
        col2.metric("Total Spending", f"â‚¹{df['total_spend'].sum():,.0f}")

        st.subheader("Customer Dataset")
        st.dataframe(df, use_container_width=True)

        st.subheader("City-wise Customer Count")
        st.bar_chart(df["city"].value_counts())

        st.subheader("Customer Spending")
        st.bar_chart(
            df.set_index("customer_id")["total_spend"]
        )
    else:
        st.error("Run generate_data.py first.")

    if segment_file.exists():
        segments = pd.read_csv(segment_file)

        st.subheader("Customer Segments")
        st.dataframe(segments, use_container_width=True)

        if "segment_name" in segments.columns:
            st.bar_chart(segments["segment_name"].value_counts())

# Ticket Classifier
elif page == "Ticket Classifier":
    st.header("🎫 Support Ticket Classifier")

    model_file = MODEL_DIR / "ticket_classifier.joblib"

    ticket_text = st.text_area(
        "Enter a customer complaint",
        placeholder="Example: My order has not arrived.",
    )

    if st.button("Classify Ticket"):
        if not ticket_text.strip():
            st.warning("Please enter a customer complaint.")
        else:
            try:
                # Train the model automatically if it doesn't exist
                if not model_file.exists():
                    from ticket_classification import train_model

                    with st.spinner("Training ticket classifier..."):
                        train_model()

                # Load model and predict
                import joblib

                model = joblib.load(model_file)
                category = model.predict([ticket_text])[0]

                st.success(f"Predicted category: {category}")
                st.caption(
                    "Demo prediction only. Verify the result before using it."
                )

            except Exception as exc:
                st.error(f"Could not classify ticket: {exc}")

# SQL Analytics
elif page == "SQL Analytics":
# Lapse Prediction
elif page == "Lapse Prediction":
    st.header("Customer Lapse Prediction")

    st.caption(
        "Demo inactivity analysis using synthetic order history. "
        "This is a rule-based prototype, not a trained ML model."
    )

    lapse_file = REPORT_DIR / "lapse_predictions.csv"

    if st.button("Generate Lapse Predictions"):
        try:
            from lapse_prediction import predict_lapse

            predict_lapse()

            if lapse_file.exists():
                df_lapse = pd.read_csv(lapse_file)

                st.success("Lapse report generated successfully!")

                st.dataframe(
                    df_lapse,
                    use_container_width=True
                )

                st.download_button(
                    "Download Lapse Predictions CSV",
                    data=df_lapse.to_csv(index=False).encode("utf-8"),
                    file_name="lapse_predictions.csv",
                    mime="text/csv",
                )
            else:
                st.warning(
                    "Report not created. Check orders.csv and customer IDs."
                )

        except Exception as exc:
            st.error(f"Lapse prediction error: {exc}")
    st.header("SQLite Database Analytics")

    DB_PATH = DATA_DIR / "instamart.db"

    if not DB_PATH.exists():
        st.error("Database not found. Please run the data import script.")
    else:
        with sqlite3.connect(DB_PATH) as conn:
            customer_count = conn.execute(
                "SELECT COUNT(*) FROM customers"
            ).fetchone()[0]

            ticket_count = conn.execute(
                "SELECT COUNT(*) FROM support_tickets"
            ).fetchone()[0]

            col1, col2 = st.columns(2)
            col1.metric("Database Customers", customer_count)
            col2.metric("Support Tickets", ticket_count)

            st.subheader("City-wise Customer Spending")

            city_data = pd.read_sql_query(
                """
                SELECT city,
                       COUNT(*) AS customer_count,
                       SUM(total_spend) AS total_spending
                FROM customers
                GROUP BY city
                ORDER BY total_spending DESC
                """,
                conn,
            )

            st.dataframe(city_data, use_container_width=True)

            st.bar_chart(
                city_data.set_index("city")["total_spending"]
            )

            st.subheader("Support Tickets by Category")

            ticket_data = pd.read_sql_query(
                """
                SELECT category, COUNT(*) AS ticket_count
                FROM support_tickets
                GROUP BY category
                ORDER BY ticket_count DESC
                """,
                conn,
            )

            st.dataframe(ticket_data, use_container_width=True)

            st.bar_chart(
                ticket_data.set_index("category")["ticket_count"]
            )
# Policy Assistant
elif page == "Policy Assistant":
    st.header("ðŸ“– Demo Policy Assistant")

    policy_file = DATA_DIR / "refund_policy.txt"

    question = st.text_input(
        "Ask a question",
        placeholder="What should I do if my product is damaged?",
    )

    if st.button("Search Policy"):
        if not question.strip():
            st.warning("Please enter a question.")
        elif not policy_file.exists():
            st.error("refund_policy.txt was not found.")
        else:
            try:
                from policy_rag import (
                    load_policy,
                    split_policy_into_sections,
                    search_policy,
                )

                policy = load_policy()
                sections = split_policy_into_sections(policy)
                result = search_policy(question, sections)

                if result:
                    st.markdown("### Relevant Policy Information")
                    st.write(result)
                else:
                    st.warning(
                        "No sufficiently relevant policy section found. "
                        "Please contact support."
                    )

            except Exception as exc:
                st.error(f"Policy search error: {exc}")

    st.caption("This uses a fictional demo policy, not official Instamart policy.")


# Refund Requests
elif page == "Refund Requests":
    st.header("ðŸ’° Refund Request Workflow")

    refund_file = DATA_DIR / "refund_requests.csv"

    with st.form("refund_form"):
        customer_id = st.text_input("Customer ID")
        order_id = st.text_input("Order ID")

        reason = st.selectbox(
            "Reason",
            [
                "Cancelled Order",
                "Damaged Product",
                "Missing Item",
                "Payment Issue",
                "Other",
            ],
        )

        description = st.text_area("Describe the issue")

        submitted = st.form_submit_button("Submit Request")

    if submitted:
        if not all(
            [customer_id.strip(), order_id.strip(), description.strip()]
        ):
            st.warning("Please complete all required fields.")
        else:
            from datetime import datetime
            import csv

            request_id = datetime.now().strftime("REF%Y%m%d%H%M%S")

            request = {
                "request_id": request_id,
                "customer_id": customer_id.strip(),
                "order_id": order_id.strip(),
                "reason": reason,
                "description": description.strip(),
                "status": "Pending Review",
                "created_at": datetime.now().isoformat(timespec="seconds"),
            }

            exists = refund_file.exists()

            with refund_file.open(
                "a", newline="", encoding="utf-8"
            ) as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=request.keys(),
                )

                if not exists:
                    writer.writeheader()

                writer.writerow(request)

            st.success(f"Request recorded: {request_id}")
            st.info("Status: Pending Review. No automatic refund is issued.")

    if refund_file.exists():
        st.subheader("Recorded Refund Requests")

        requests = pd.read_csv(refund_file)
        st.dataframe(requests, use_container_width=True)



