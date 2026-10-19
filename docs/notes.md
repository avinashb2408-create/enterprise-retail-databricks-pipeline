# Working notes

My scratchpad for this repo. Not a roadmap - just what I'd pick up next
and what's still rough.

## Still to do

- Finish the full Spark run locally. The generator and the non-Spark
  tests pass, but I haven't run Bronze -> Silver -> Gold end to end yet
  (this machine has no JDK). Until that output is in
  `docs/execution_report.md`, I don't count the pipeline as verified.
- Run the notebooks in Databricks Community Edition as-is and fix
  whatever path assumptions break. The config is supposed to be the only
  thing that changes; I want to prove that.
- Late-arriving dimensions: right now fact_sales joins the current
  product row. If a price changes between order and load, Gold should
  really join the SCD2 version effective on order_date. That's the
  correct behaviour and it's not in yet.
- Try packaging the pipeline as a Databricks job (job clusters, one
  task per notebook) instead of running notebooks by hand.
- A products feed that actually changes day to day, so the SCD2 code
  gets exercised by data, not just by my test rows.
- Quarantine counts as a small table I can trend. At work I'd alert on
  it; here a daily count and a quick look is enough.
- Gold: customer_segments bands were picked from this dataset. On a
  second dataset they'd need re-picking - noted so I don't pretend
  they're universal.

## Known rough edges

- Two date formats handled in Silver. A third will show up eventually;
  the coalesce chain in clean_orders is where it goes.
- Gold aggregates overwrite. Fine at this size, wrong at real volume -
  incremental Gold is still on the list (see CHANGELOG).
