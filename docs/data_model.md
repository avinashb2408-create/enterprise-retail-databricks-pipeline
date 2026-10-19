# Data model

| Table | Grain | Notes |
|---|---|---|
| bronze_* | one row per source row | as landed, plus ingest columns |
| silver_orders | one row per order | deduped, `unit_price > 0`, parsed `order_date` |
| silver_customers | one row per customer | email may be null - flagged, not dropped |
| silver_products | one row per product | current catalogue only in Silver |
| gold.dim_customer | one row per customer version | SCD2: `is_current`, `effective_from/to`, `row_hash` |
| gold.dim_product | one row per product version | SCD2 on name/category/price |
| gold.fact_sales | one row per completed/shipped order | partitioned by `order_date`, `line_amount = quantity * unit_price` |
| gold.sales_by_category_month | category x month | revenue, distinct orders |
| gold.inventory_risk | product/store below reorder level | the reorder list, nothing more |
| gold.customer_segments | one row per customer | total spend + Low/Mid/High band |

Keys: `customer_id`, `product_id`, `order_id`, `supplier_id`, `store_id`.
No surrogate keys generated - the source IDs are stable in this dataset,
and inventing them would just add a join.
