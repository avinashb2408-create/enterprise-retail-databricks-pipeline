# Databricks notebook source
# MAGIC %md
# MAGIC # 03 - Gold tables + SCD Type 2
# MAGIC Gold answers specific questions (category/month revenue, reorder risk, customer bands).
# MAGIC SCD2 only for `dim_customer` / `dim_product` - full reasoning in `docs/decisions.md`.
# COMMAND ----------
from src.transformations.gold_transformations import build_gold
from src.transformations.scd_type2 import apply_scd2
from src.utils.config import load_config, table_path
cfg = load_config()
print(build_gold(spark, cfg))
# COMMAND ----------
customers = spark.read.format("delta").load(table_path(cfg, "silver", "customers"))
apply_scd2(spark, table_path(cfg, "gold", "dim_customer"), "dim_customer", customers)
# COMMAND ----------
# MAGIC %md Check history worked: change one customer's city in Silver, re-run, and you should
# MAGIC %md see the old row closed (`is_current=false`) and a new current row.
