# Databricks notebook source
# MAGIC %md
# MAGIC # 02 - Silver transformations
# MAGIC Dedupe, fix the two date formats, drop the negative-price rows, tidy emails.
# MAGIC Logic lives in `src/transformations/silver_transformations.py` - this notebook just runs it.
# COMMAND ----------
from src.transformations.silver_transformations import clean_orders, clean_customers, dedupe
# COMMAND ----------
# MAGIC %md Run the full Silver step from the script entry point, then inspect:
# COMMAND ----------
# %run ../src/transformations/silver_transformations
display(spark.read.format("delta").load("data/warehouse/silver/orders").limit(20))
# COMMAND ----------
# MAGIC %md If `order_date` has a lot of nulls after this, a source added a third date format. Check before assuming data loss.
