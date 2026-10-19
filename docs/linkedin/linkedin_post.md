# LinkedIn post (draft, not published - needs Avinash's approval)

I spent the last stretch of weekends building a retail data pipeline from
scratch - not following a tutorial, just working through the problems that
actually show up in this kind of data.

The setup: orders, customers, products, and inventory arriving as CSV,
JSON, and Parquet, processed in Databricks-style notebooks with PySpark,
stored in Delta Lake as Bronze, Silver, and Gold.

Bronze changed nothing. Silver did the real work. Gold answered specific
questions.

A few decisions worth mentioning:

- Orders load with a Delta MERGE on order_id, filtered by an updated_at
  watermark. Retail orders get corrected after the fact; appending blindly
  would double-count them.
- Customers and products are SCD Type 2 - a price change keeps its
  history. Orders and inventory are not. History you never query is just
  storage and confusion.
- I generated the data myself, with the dirt left in on purpose: duplicate
  orders, a negative-priced row, two different date formats. The pipeline
  quarantines bad rows with the rule they failed, rather than dropping them.

The honest lesson: my first version cleansed a few things in Bronze
because it was convenient. I moved all of it to Silver. When a Gold number
looked off, I wanted Bronze to tell me exactly what had arrived - and at
that point it couldn't.

Code, notebooks, SQL, tests, and the reasoning behind the trade-offs
are here: https://github.com/avinashb2408-create/enterprise-retail-databricks-pipeline

I run it locally on PySpark + Delta; the same notebooks and modules run
on Azure Databricks with only the config paths changed. Happy to hear
how others handle SCD scope or incremental Gold tables.

- Avinash B, Senior Data Engineer (Databricks / PySpark / Azure), Richmond, VA

Hashtags: #DataEngineering #Databricks #PySpark #DeltaLake #Azure #ApacheSpark #ETL
