.PHONY: data test run-local lint
data:
	python src/data_generation/generate_retail_data.py
test:
	pytest tests/ -q
run-local:
	python src/ingestion/bronze_ingestion.py
	python src/transformations/silver_transformations.py
	python src/transformations/gold_transformations.py
# No linter config worth fighting with yet - see docs/decisions.md
lint:
	python -m compileall src tests
