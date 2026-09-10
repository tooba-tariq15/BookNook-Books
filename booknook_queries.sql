-- BookNook Books — queries.sql
-- Reference queries used throughout the assignment.

-- 1. Row-count check (Task 1.2 and Task 1.6) — run any time.
SELECT 'customers' AS table_name, COUNT(*) FROM customers
UNION ALL SELECT 'products', COUNT(*) FROM products
UNION ALL SELECT 'orders', COUNT(*) FROM orders
UNION ALL SELECT 'orderitems', COUNT(*) FROM orderitems;

-- 2. Order totals check (Task 1.6) — run after the pipeline AND load_orderitems.py.
SELECT o.order_id, c.first_name, c.last_name,
       COUNT(oi.order_item_id) AS line_items,
       SUM(oi.quantity * oi.unit_price) AS order_total
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
JOIN orderitems oi ON oi.order_id = o.order_id
GROUP BY o.order_id, c.first_name, c.last_name
ORDER BY o.order_id;

-- 3. Day 2 join query — builds the DataFrame used for every chart.
SELECT o.order_id, o.order_date, o.status,
       p.product_name, p.category,
       oi.quantity, oi.unit_price
FROM orders o
JOIN orderitems oi ON oi.order_id = o.order_id
JOIN products p ON p.product_id = oi.product_id;

-- 4. Day 3 city counts — feeds the Folium map.
SELECT city, COUNT(*) AS n FROM customers GROUP BY city;
