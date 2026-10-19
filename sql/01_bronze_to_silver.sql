-- Bronze -> Silver for orders, the SQL twin of silver_transformations.py.
-- I keep both: PySpark for the pipeline, SQL here because an analyst asked
-- "show me exactly what changed" and SQL is easier to review in a PR.
CREATE OR REPLACE TABLE silver_orders AS
SELECT DISTINCT
  CAST(order_id AS BIGINT) AS order_id,
  CAST(customer_id AS BIGINT) AS customer_id,
  CAST(product_id AS BIGINT) AS product_id,
  COALESCE(TRY_TO_DATE(order_date, 'yyyy-MM-dd'), TRY_TO_DATE(order_date, 'MM/dd/yyyy')) AS order_date,
  quantity, unit_price, status
FROM bronze_orders
WHERE unit_price > 0;
-- TODO: DISTINCT here hides the duplicate-file problem; the PySpark path
-- dedupes with row_number() and logs the count, prefer that one.
