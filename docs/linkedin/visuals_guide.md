# Visuals for the LinkedIn post

Attach the Medallion diagram first - it is the one people will actually read.

1. `docs/diagrams/medallion_architecture.html` - open in a browser, screenshot
   the diagram. Source is the `.mmd` file beside it, edit that and re-open.
2. `docs/diagrams/pipeline_flowchart.html` - same process, shows the run order
   and where quarantine branches off.
3. Tech stack, as text (no graphic needed): Python, PySpark / Apache Spark,
   SQL, Delta Lake, Databricks notebooks, YAML config, pytest.
4. Notebook screenshots: only use real ones, taken after running notebooks
   01-04 in Databricks Community Edition or a workspace. There are no
   execution screenshots in this repo yet because the Spark pipeline has
   not been run in this environment - see docs/execution_report.md.
   Do not screenshot the local sample CSVs and present them as notebook output.
