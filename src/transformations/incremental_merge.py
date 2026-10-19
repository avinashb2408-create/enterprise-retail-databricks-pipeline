"""Incremental upsert for orders. I chose Delta MERGE here because late and
corrected orders are normal in retail - a plain append would double-count them,
and a full overwrite gets slower every month for no reason.
Watermark: only rows with updated_at after the stored max are even read.
"""
from delta.tables import DeltaTable
from src.utils.config import load_config, table_path

def watermark(spark, path: str, col: str = "updated_at"):
    try: return spark.read.format("delta").load(path).agg({col:"max"}).collect()[0][0]
    except Exception: return None  # first run, table doesn't exist yet

def merge_orders(spark, cfg: dict, source_df):
    target_path = table_path(cfg, "silver", "orders")
    if not DeltaTable.isDeltaTable(spark, target_path):
        source_df.write.format("delta").save(target_path); return
    t = DeltaTable.forPath(spark, target_path)
    (t.alias("t").merge(source_df.alias("s"), "t.order_id = s.order_id")
       .whenMatchedUpdateAll().whenNotMatchedInsertAll().execute())
