# Architecture

Three layers, Delta Lake at each one. Nothing fancy - this is the setup
I've used on retail-style data before and it holds up because each layer
has one job.

**Sources** - CSV from CRM-type exports, JSON lines from the web store,
Parquet for inventory. Mixed formats are deliberate; real feeds never agree.

**Bronze** - files landed as-is into Delta, plus `_ingested_at` and
`_source_file`. No cleansing. If Silver produces a strange number, I can
always go back and see exactly what arrived.

**Silver** - types cast, duplicate orders removed (latest ingest wins),
two date formats reconciled, negative-price rows sent to quarantine,
emails trimmed/lowered. This is where data becomes trustworthy.

**Gold** - tables built for questions: `fact_sales`,
`sales_by_category_month`, `top_products`, `inventory_risk`,
`customer_segments`, plus SCD Type 2 dimensions for customers and products.

**Incremental** - orders merge into Silver with Delta MERGE keyed on
`order_id`, filtered by an `updated_at` watermark. Full reloads are in
the code for first runs and backfills, not as the daily path.

**Quality** - rules live in `src/data_quality/quality_checks.py`.
Critical failures are written to a quarantine Delta path with the rule
names attached. They are counted and printed, not swallowed.

On Databricks this maps directly: notebooks 01-04 run the same `src/`
modules, DBFS/Unity Catalog volume replaces the local `data/warehouse/`
paths in `config/pipeline_config.yaml`. No code changes.
