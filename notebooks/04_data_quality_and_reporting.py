# Databricks notebook source
# MAGIC %md
# MAGIC # 04 - Data quality + reporting
# MAGIC Critical rule failures go to quarantine, they don't quietly disappear.
# COMMAND ----------
from src.data_quality.quality_checks import RULES, run_spark_checks
from src.utils.config import load_config, table_path
cfg = load_config()
orders = spark.read.format("delta").load(table_path(cfg, "bronze", "orders"))
clean, bad = run_spark_checks(spark, orders, "orders", cfg["paths"]["quarantine"])
print("clean:", clean.count(), "quarantined:", bad.count())
# COMMAND ----------
# MAGIC %sql
# MAGIC -- Same query as sql/03_business_reporting_queries.sql, section 1
# MAGIC SELECT * FROM delta.`data/warehouse/gold/sales_by_category_month` ORDER BY sales_month, revenue DESC;
# COMMAND ----------
# MAGIC %md TODO: wire the quarantine count into an alert. For a portfolio project, printing it is enough.
