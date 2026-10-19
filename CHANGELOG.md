# Changelog

## Cleanup - 2026-10-19
- Naming pass, the way I'd name things at work: logging_setup.py is
  now src/utils/log.py, clean_generic is dedupe_only, watermark() is
  get_watermark()
- Author details filled in properly (README byline, config owner)
- Added docs/notes.md with my working notes and what's still rough
- Fixed a line in the LinkedIn draft that claimed a local Spark run
  I haven't actually finished yet

## v0.2 - 2026-10-19
- SCD Type 2 for dim_customer / dim_product (two-step MERGE)
- Data quality rules split out into plain Python + Spark application,
  quarantine output added
- Notebooks 01-04 added in Databricks source format
- Execution report: generator + pytest verified locally; Spark run
  still pending a JDK (see docs/execution_report.md)

## v0.1 - 2026-10-19
- Seeded synthetic generator with intentionally dirty slice
- Bronze ingestion for CSV / JSON / Parquet
- Silver cleansing + dedupe, Gold aggregates
- Config in YAML, first pytest suite

<!-- TODO: v0.3 - incremental Gold, and an alert stub for quarantine counts -->
