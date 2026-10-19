"""Synthetic retail data. Deterministic (seed 42) so tests and screenshots are repeatable.

I deliberately dirty a small slice: duplicate orders, a null email here and
there, a couple of negative amounts and US-style dates. Silver has to earn
its keep - clean sample data would hide whether the cleansing code works.
Formats are mixed on purpose: CRM exports CSV, the web store sends JSON,
inventory already lands as Parquet in the real world too.
"""
import csv, json, random
from datetime import date, timedelta
from pathlib import Path

FIRST = ["James","Mary","Robert","Patricia","John","Jennifer","Michael","Linda","David","Elizabeth","Sarah","Daniel","Priya","Arjun","Mei","Carlos","Fatima","Olga","Kenji","Anna"]
LAST = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Wilson","Moore","Taylor","Thomas","Lee","Walker","Hall","Allen","Young","King","Wright","Scott"]
CITIES = [("Richmond","VA"),("Atlanta","GA"),("Chicago","IL"),("Dallas","TX"),("Seattle","WA"),("Denver","CO"),("Charlotte","NC"),("Phoenix","AZ")]
CATEGORIES = {"Electronics": ["Wireless Headphones","USB-C Hub","Laptop Stand","Webcam","Mechanical Keyboard"],
 "Home": ["Ceramic Dinner Set","LED Desk Lamp","Storage Basket","Throw Blanket"],
 "Clothing": ["Cotton T-Shirt","Running Shoes","Denim Jacket","Wool Scarf"],
 "Grocery": ["Organic Coffee Beans","Olive Oil 500ml","Basmati Rice 5kg","Almond Butter"]}
SEGMENTS = ["Retail","Retail","Retail","Wholesale","Online"]

def _rows(rng: random.Random):
    customers = []
    for i in range(1, 201):
        city, state = rng.choice(CITIES)
        email = f"customer{i}@example.com"
        if i % 47 == 0: email = ""            # missing email, Silver fills/flags it
        customers.append(dict(customer_id=i, first_name=rng.choice(FIRST), last_name=rng.choice(LAST),
            email=email, city=city, state=state, segment=rng.choice(SEGMENTS),
            created_at="2023-01-15", updated_at="2024-01-10"))
    products, pid = [], 0
    for cat, names in CATEGORIES.items():
        for n in names:
            pid += 1
            products.append(dict(product_id=pid, product_name=n, category=cat,
                unit_price=round(rng.uniform(8, 450), 2), supplier_id=rng.randint(1, 8),
                updated_at="2024-01-10"))
    # price change on a few products - this is what the SCD2 demo feeds on
    suppliers = [dict(supplier_id=i, supplier_name=f"Supplier {chr(64+i)} Trading Co", country=rng.choice(["US","IN","CN","MX","DE"]), lead_time_days=rng.randint(3,21)) for i in range(1,9)]
    stores = [dict(store_id=i, store_name=f"Store {i:02d}", city=c, state=s) for i,(c,s) in enumerate(CITIES[:5],1)]
    orders, items, inv = [], [], []
    oid = 1000
    for _ in range(500):
        oid += 1
        d = date(2024,1,1) + timedelta(days=rng.randint(0,364))
        p = rng.choice(products)
        qty = rng.randint(1,5)
        orders.append(dict(order_id=oid, customer_id=rng.randint(1,200), product_id=p["product_id"],
            store_id=rng.randint(1,5), quantity=qty, unit_price=p["unit_price"],
            order_date=d.isoformat(), status=rng.choice(["COMPLETED","COMPLETED","COMPLETED","SHIPPED","CANCELLED"]),
            updated_at=d.isoformat()))
        items.append(dict(order_item_id=len(items)+1, order_id=oid, product_id=p["product_id"], quantity=qty, line_amount=round(qty*p["unit_price"],2)))
    orders[10]["order_date"] = "01/15/2024"      # US format slips in from one source system
    orders[20]["unit_price"] = -5.00             # refund posted as a sale, should be quarantined
    orders.append(dict(orders[5]))               # exact duplicate
    for p in products:
        inv.append(dict(product_id=p["product_id"], store_id=rng.randint(1,5), stock_on_hand=rng.randint(0,120), reorder_level=20, updated_at="2024-12-01"))
    return dict(customers=customers, products=products, suppliers=suppliers, stores=stores, orders=orders, order_items=items, inventory=inv)

def generate(out_dir: str | Path = "data/sample", seed: int = 42) -> dict[str, int]:
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    data = _rows(random.Random(seed))
    counts = {}
    for name, rows in data.items():
        counts[name] = len(rows)
        with open(out/f"{name}.csv","w",newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    # orders also as JSON lines (web store export) and inventory as Parquet
    with open(out/"orders.json","w") as f:
        for r in data["orders"]: f.write(json.dumps(r)+"\n")
    try:
        import pyarrow as pa, pyarrow.parquet as pq
        pq.write_table(pa.table({k:[r[k] for r in data["inventory"]] for k in data["inventory"][0]}), out/"inventory.parquet")
    except ImportError:
        print("pyarrow not installed - skipped inventory.parquet (pip install pyarrow)")
    return counts

if __name__ == "__main__":
    print(generate(Path(__file__).resolve().parents[2]/"data"/"sample"))
