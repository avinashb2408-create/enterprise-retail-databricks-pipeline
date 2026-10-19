-- Questions these were written for, in the order I actually got asked them.

-- 1. What sold, by category and month?
SELECT * FROM gold_sales_by_category_month ORDER BY sales_month, revenue DESC;

-- 2. Top 10 products by revenue
SELECT p.product_name, p.category, ROUND(SUM(f.quantity * f.unit_price),2) AS revenue
FROM silver_orders f JOIN silver_products p USING (product_id)
WHERE f.status IN ('COMPLETED','SHIPPED')
GROUP BY p.product_name, p.category ORDER BY revenue DESC LIMIT 10;

-- 3. Inventory that needs reordering now
SELECT product_id, product_name, stock_on_hand, reorder_level
FROM gold_inventory_risk ORDER BY stock_on_hand ASC;

-- 4. Customer bands by spend (bands picked by eye from the distribution, not a model)
SELECT segment_band, COUNT(*) AS customers, ROUND(AVG(total_spend),2) AS avg_spend
FROM gold_customer_segments GROUP BY segment_band ORDER BY avg_spend DESC;
