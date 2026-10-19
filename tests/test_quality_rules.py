import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.data_quality.quality_checks import check_row, RULES

def test_good_order_passes():
    row = {"order_id":1,"customer_id":2,"unit_price":10.0,"status":"COMPLETED"}
    assert check_row("orders", row) == []

def test_negative_price_fails():
    row = {"order_id":1,"customer_id":2,"unit_price":-5.0,"status":"COMPLETED"}
    assert "price_not_negative" in check_row("orders", row)

def test_missing_email_is_not_critical_path():
    assert "email_present" in check_row("customers", {"customer_id":1,"email":""})

def test_rules_cover_orders():
    assert {r.name for r in RULES["orders"]} >= {"order_id_present","price_not_negative"}
