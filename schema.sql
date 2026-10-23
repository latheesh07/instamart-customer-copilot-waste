-- Instamart Customer Intelligence & Support Copilot

CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    city TEXT,
    total_orders INTEGER DEFAULT 0,
    total_spend REAL DEFAULT 0,
    last_order_date TEXT
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date TEXT,
    order_amount REAL,
    order_status TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS support_tickets (
    ticket_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    ticket_text TEXT,
    category TEXT,
    status TEXT DEFAULT 'Open',
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Query 1: View all customers
SELECT * FROM customers;

-- Query 2: Total spending by customer
SELECT customer_id, SUM(order_amount) AS total_spend
FROM orders
GROUP BY customer_id;

-- Query 3: Count tickets by category
SELECT category, COUNT(*) AS ticket_count
FROM support_tickets
GROUP BY category;
