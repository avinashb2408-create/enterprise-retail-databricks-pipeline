# Execution report

Written from actual runs in the build environment, 2026-10-19.
Anything not listed as run here was not run.

## Environment
- Python 3.12.3 (system), tests run in a virtualenv with pytest 9.1.1,
  PyYAML, and pyarrow 26.0.0
- Java: not installed in this environment
- PySpark: not installed / not run here

## Ran: data generator
Command: `python src/data_generation/generate_retail_data.py`

Output:
```
{'customers': 200, 'products': 17, 'suppliers': 8, 'stores': 5, 'orders': 501, 'order_items': 500, 'inventory': 17}
```
Orders count is 501, not 500: the generator appends one exact duplicate
on purpose to exercise Silver deduplication.

Files written to `data/sample/`: customers.csv, products.csv,
suppliers.csv, stores.csv, orders.csv, order_items.csv, inventory.csv,
orders.json (JSON lines), inventory.parquet.

## Ran: pytest (non-Spark)
Command: `pytest tests/ -q`

Result: **8 passed, 1 skipped**.
The skipped test is `tests/test_spark_smoke.py`, marked skipped because
it needs Spark + a JDK. The 8 passing tests cover config loading,
generator determinism and counts, the intentionally dirty rows being
present, generated files existing, and the data quality rule functions.

## Not run
- The Spark/Delta pipeline (Bronze -> Silver -> Gold, MERGE, SCD2).
  No Java in this environment, so no Delta tables were created and no
  Gold output exists yet. The SQL timings / row counts for Gold are
  therefore not shown anywhere in this repo.
- Anything on Azure Databricks or Databricks Community Edition.

## Published
- GitHub: repository created and public since 2026-10-19 —
  https://github.com/avinashb2408-create/enterprise-retail-databricks-pipeline
- LinkedIn: project added to profile and launch post published 2026-10-19.

## To reproduce the Spark run
Install JDK 17, `pip install -r requirements.txt`, then follow
"Run it locally" in the README, and replace this section with the
actual output.
