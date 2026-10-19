"""Spark session that does the right thing in both places I run this:
locally (build a session with Delta) and on Databricks (one already exists).
"""
try:
    from pyspark.sql import SparkSession
except ImportError:  # tests run without Spark
    SparkSession = None  # type: ignore

def get_spark(app_name: str = "retail-medallion"):
    if SparkSession is None:
        raise RuntimeError("pyspark is not installed - see requirements.txt")
    # Databricks injects a session; getOrCreate returns it untouched.
    spark = (
        SparkSession.builder.appName(app_name)
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")
    return spark
