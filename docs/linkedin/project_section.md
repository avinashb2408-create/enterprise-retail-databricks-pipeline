# LinkedIn - Projects section (draft, not published)

**Project name**
Enterprise Retail Data Engineering Pipeline - Azure Databricks, PySpark, Delta Lake

**Project URL**
[GitHub URL after repo creation]

**Associated with**
Independent / personal project (not an employer project)

**Description**
I built this to work through a retail pipeline end to end the way I would
on a job, using synthetic data I generated myself - no employer data.

Source files arrive in three formats (CSV, JSON lines, Parquet) and move
through a Medallion layout on Delta Lake: Bronze lands data unchanged,
Silver handles deduplication, type casting, nulls, and two different date
formats, and Gold holds the tables reporting actually uses - fact_sales,
sales by category and month, inventory below reorder level, and customer
spend bands.

Orders load incrementally with a Delta MERGE on order_id and an
updated_at watermark. Customers and products use SCD Type 2, so a price
or address change keeps its history. Data quality rules run before Silver;
rows that fail a critical rule go to a quarantine table with the rule name
attached instead of being dropped silently.

The code runs locally on PySpark + Delta and the notebooks run unchanged
on Databricks - only the paths in the config file change. I documented
the trade-offs, including where I decided not to use SCD2 and why
Z-ORDER stayed off, in docs/decisions.md in the repo.

**Technologies**
Azure Databricks, Python, SQL, PySpark, Apache Spark, Delta Lake, ETL/ELT, Data Engineering
