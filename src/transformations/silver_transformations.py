"""Bronze -> Silver: the unglamorous work - types, trims, dedupe, bad dates."""
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from src.utils.config import load_config, table_path
from src.utils.spark_session import get_spark

def dedupe(df, keys: list[str], order_col: str = "_ingested_at"):
    # keep the latest copy when a file was landed twice
    w = Window.partitionBy(*keys).orderBy(F.col(order_col).desc())
    return df.withColumn("_rn", F.row_number().over(w)).filter("_rn = 1").drop("_rn")

def clean_orders(df):
    df = dedupe(df, ["order_id"])
    # two date formats in the wild: ISO from most systems, MM/dd/yyyy from one store export
    df = df.withColumn("order_date", F.coalesce(F.to_date("order_date", "yyyy-MM-dd"), F.to_date("order_date", "MM/dd/yyyy")))
    return df.filter("unit_price > 0 AND order_date IS NOT NULL")

def clean_customers(df):
    df = dedupe(df, ["customer_id"])
    return (df.withColumn("email", F.lower(F.trim("email")))
              .withColumn("email", F.when(F.col("email") == "", None).otherwise(F.col("email")))
              .withColumn("first_name", F.initcap(F.trim("first_name"))))

def dedupe_only(df, key: str):
    # fallback for tables with no real cleaning rules yet - just dedupe
    return dedupe(df, [key])

CLEANERS = {"orders": clean_orders, "customers": clean_customers}

def main():
    cfg = load_config(); spark = get_spark()
    keys = {"products":"product_id","order_items":"order_item_id","inventory":"product_id"}
    for t in cfg["tables"]["silver"]:
        df = spark.read.format("delta").load(table_path(cfg, "bronze", t))
        out = CLEANERS.get(t, lambda d: dedupe_only(d, keys.get(t, "product_id")))(df)
        out.write.format("delta").mode("overwrite").option("overwriteSchema","true").save(table_path(cfg, "silver", t))

if __name__ == "__main__": main()
