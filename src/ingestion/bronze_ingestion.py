"""Bronze = land it as-is, add two columns, change nothing else.

Resist the urge to 'fix it a bit' here. Every cleanup in Bronze is a cleanup
Silver can't audit later. Only additions: _ingested_at and _source_file.
"""
from pathlib import Path
from src.utils.config import load_config, table_path
from src.utils.spark_session import get_spark
from src.utils.logging_setup import get_logger

log = get_logger(__name__)
FORMATS = {"customers":"csv","products":"csv","suppliers":"csv","stores":"csv","order_items":"csv","orders":"json","inventory":"parquet"}

def ingest(spark, cfg: dict, table: str) -> int:
    from pyspark.sql import functions as F
    root = Path(cfg["paths"]["data_root"]); fmt = FORMATS[table]
    reader = spark.read.option("header", True).option("inferSchema", True) if fmt == "csv" else spark.read
    df = reader.format(fmt).load(str(root / f"{table}.{fmt}"))
    df = df.withColumn("_ingested_at", F.current_timestamp()).withColumn("_source_file", F.input_file_name())
    # append-only on purpose; re-running a file shows up as duplicates that Silver dedupes visibly
    df.write.format("delta").mode("append").save(table_path(cfg, "bronze", table))
    n = df.count(); log.info("bronze %s: %d rows", table, n); return n

def main():
    cfg = load_config(); spark = get_spark()
    for t in cfg["tables"]["bronze"]: ingest(spark, cfg, t)

if __name__ == "__main__": main()
