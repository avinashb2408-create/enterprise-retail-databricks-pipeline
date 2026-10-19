#!/usr/bin/env bash
set -e
python src/data_generation/generate_retail_data.py
pytest tests/ -q
# Spark steps - need JDK 17 + requirements installed
python src/ingestion/bronze_ingestion.py
python src/transformations/silver_transformations.py
python src/transformations/gold_transformations.py
