# Databricks notebook source
# MAGIC %md
# MAGIC # 01 - Bronze ingestion
# MAGIC Land each source file as-is into Delta, add `_ingested_at` / `_source_file`.
# MAGIC No cleansing here - see `src/ingestion/bronze_ingestion.py` for the reasoning.
# COMMAND ----------
# MAGIC %md ### Setup (works locally and on Databricks - session is injected here)
# COMMAND ----------
import sys
sys.path.append("../")  # repo root; on Databricks use %pip / workspace files path instead
from src.ingestion.bronze_ingestion import ingest
from src.utils.config import load_config
cfg = load_config()
# COMMAND ----------
for table in cfg["tables"]["bronze"]:
    print(table, ingest(spark, cfg, table))
# COMMAND ----------
# MAGIC %md Spot check: row counts in Bronze should match the files. Duplicates are expected and handled in Silver.
