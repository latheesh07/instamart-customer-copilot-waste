# 🛒 Instamart Customer Intelligence & Support Copilot

A Python and Streamlit-based customer intelligence dashboard that demonstrates customer analytics, RFM segmentation, support ticket classification, policy retrieval, refund request tracking, and customer lapse risk analysis.

> ⚠️ Educational capstone project using synthetic data. This is not an official Instamart application.

## 📌 Project Overview

The Instamart Customer Intelligence & Support Copilot demonstrates how data analytics and AI-assisted workflows can support customer service operations.

The application provides a unified interface for exploring customer data, analyzing customer segments, classifying support tickets, retrieving demo policy information, and examining customer lapse risk.

## ✨ Features

### 📊 1. Dashboard
- Overview of the available customer and support data.
- Summary metrics for exploring the dataset.

### 👥 2. Customer Analytics
- Customer data analysis.
- RFM (Recency, Frequency, Monetary) analysis.
- Customer segmentation insights.

### 🗄️ 3. SQL Analytics
- SQL-based data exploration.
- Customer and order analysis using SQLite.

### 🎫 4. Ticket Classifier
- Demonstration of support ticket classification.
- Support ticket triage workflows.

### 📚 5. Policy Assistant
- Retrieves information from a fictional demonstration refund policy.
- Helps users explore policy-related questions.

### 💳 6. Refund Requests
- Demonstrates a refund request tracking workflow.
- Does not initiate real refunds.

### 🔍 7. Lapse Prediction
- Demonstrates rule-based customer lapse risk analysis.
- This prototype should not be interpreted as a validated predictive model.

## 🧰 Technologies Used

- *Python* — Application logic
- *Streamlit* — Interactive web application
- *Pandas* — Data processing and analysis
- *SQLite* — Relational database and SQL analytics
- *Scikit-learn* — Machine learning library included in the project technology stack

The use of a library does not imply that every feature uses a trained machine-learning model.

## 📁 Project Structure

```text
instamart-customer-copilot/
├── app.py
├── README.md
├── requirements.txt
├── schema.sql
├── queries.sql
├── data/
│   ├── customers.csv
│   ├── customer_segments.csv
│   ├── support_tickets.csv
│   ├── refund_policy.txt
│   └── orders.csv
└── src/
    ├── generate_data.py
    ├── analyze_customers.py
    ├── import_data.py
    ├── ticket_classification.py
    ├── policy_rag.py
    └── lapse_prediction.py
