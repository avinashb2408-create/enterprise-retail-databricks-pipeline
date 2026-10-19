# Decisions

Short notes, written when I made the call. Not a design doc.

## Synthetic data, generated not downloaded
Kaggle retail sets are either too clean or have licence terms I don't
want to think about for a public repo. A seeded generator (seed 42) means
anyone can recreate the exact dataset, and I could add the dirty cases
I actually wanted to test: duplicates, a negative amount, US-format dates.

## SCD Type 2 only on customers and products
Those are the two where "what was true at the time of the sale?" matters -
a customer's segment and a product's price/category. Orders are events;
corrections arrive as new rows. Inventory changes hourly, history rows
would mostly be noise. SCD2 everywhere is a common portfolio move and a
poor production one.

## MERGE for orders, overwrite for Gold aggregates
Orders get late corrections, so they MERGE. Gold aggregates are cheap
to rebuild from Silver at this scale, so they overwrite - simpler, and
the logic stays easy to audit. At a much larger scale I'd make
`sales_by_category_month` incremental too.

## Partition fact_sales by order_date, no Z-ORDER by default
I tried Z-ORDER on `customer_id`: the customer-segment query got faster,
the load got slower, and at this dataset size neither mattered much.
Partitioning by date matches how the data is actually queried. Left the
note in the Gold module rather than pretending I tuned something I didn't.

## Rules in plain Python, applied in Spark
The rule list (`quality_checks.py`) is testable without spinning up
Spark, which means the tests run in half a second in CI. The Spark side
only translates the same rules into filters.

## Known limitations
- Date parsing covers two formats. A third format produces nulls that
  the checks count, but nothing auto-detects the new format.
- Quarantine is a Delta path, not an alert. Nobody gets paged.
- SCD2 compares a hash of tracked columns only; an untracked column
  change is applied... actually it isn't - untracked changes are ignored
  by design, and that could surprise someone. Worth knowing.
- Local Delta runs need JDK 17; the pure-Python tests don't.
- Bands in `customer_segments` (300 / 1000) were picked from the spend
  distribution of this synthetic data. They are not a business rule.
