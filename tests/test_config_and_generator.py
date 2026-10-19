import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
# .yaml config loader needs pyyaml; skip cleanly on a bare checkout
import pytest
yaml = pytest.importorskip("yaml")
from src.utils.config import load_config
from src.data_generation.generate_retail_data import generate, _rows
import random

def test_config_loads():
    cfg = load_config()
    assert cfg["pipeline"]["name"] == "retail-medallion"
    assert "dim_customer" in cfg["tables"]["gold"]
    assert cfg["paths"]["bronze"].endswith("bronze")

def test_generator_is_deterministic():
    a, b = _rows(random.Random(42)), _rows(random.Random(42))
    assert a["orders"][0] == b["orders"][0] and len(a["customers"]) == 200

def test_generator_counts_and_dirty_data_present(tmp_path):
    counts = generate(tmp_path, seed=42)
    assert counts == {"customers":200,"products":17,"suppliers":8,"stores":5,"orders":501,"order_items":500,"inventory":17}
    # the dirt is part of the test - Silver tests depend on it existing
    assert any(o["unit_price"] < 0 for o in _rows(random.Random(42))["orders"])

def test_generated_files_exist(tmp_path):
    generate(tmp_path, seed=42)
    for f in ["customers.csv","products.csv","orders.csv","orders.json"]:
        assert (tmp_path/f).exists()
