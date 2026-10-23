-- 1. View all customers
SELECT * FROM customers;

-- 2. Total spending by city
SELECT city, COUNT(*) AS customer_count,
       SUM(total_spend) AS total_spending
FROM customers
GROUP BY city
ORDER BY total_spending DESC;

-- 3. Count support tickets by category
SELECT category, COUNT(*) AS ticket_count
FROM support_tickets
GROUP BY category
ORDER BY ticket_count DESC;
