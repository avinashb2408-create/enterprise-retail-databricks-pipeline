-- Gold: sales_by_category_month
CREATE OR REPLACE TABLE gold_sales_by_category_month AS
SELECT p.category,
       DATE_FORMAT(f.order_date, 'yyyy-MM') AS sales_month,
       ROUND(SUM(f.quantity * f.unit_price), 2) AS revenue,
       COUNT(DISTINCT f.order_id) AS orders
FROM silver_orders f
JOIN silver_products p ON p.product_id = f.product_id
WHERE f.status IN ('COMPLETED', 'SHIPPED')
GROUP BY p.category, DATE_FORMAT(f.order_date, 'yyyy-MM')
ORDER BY sales_month, revenue DESC;
