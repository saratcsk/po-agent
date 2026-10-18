"""Step 2: create fake suppliers and items. No AI needed, just Python."""
import csv
import random
from pathlib import Path

random.seed(42)  # same data every time you run it
DATA = Path(__file__).resolve().parent.parent / "data"

suppliers = [
    ("S001", "Northwind Metals"), ("S002", "Bluefield Plastics"), ("S003", "Riverstone Electric"),
    ("S004", "Summit Fasteners"), ("S005", "Lakeside Packaging"), ("S006", "Ironbridge Castings"),
    ("S007", "Clearwater Valves"), ("S008", "Pinecrest Motors"), ("S009", "Harbor Coatings"),
    ("S010", "Granite Tooling"),
]

products = [
    "Steel bracket", "Copper wire 10m", "PVC pipe 2in", "Hex bolt M8", "Ball valve 1in",
    "Fan motor 1HP", "Cardboard box large", "Epoxy primer 1gal", "Aluminum sheet", "Rubber gasket",
    "Pressure sensor", "Thermostat control", "Drill bit set", "Cable tie pack", "Hinge heavy duty",
    "Compressor seal", "Coil assembly", "Circuit breaker 20A", "Shrink wrap roll", "Paint thinner 1gal",
    "Brass fitting", "Fan blade 18in", "Mounting plate", "Wire connector pack", "Air filter",
    "Control board", "Pallet wrap", "Lock washer M8", "Duct tape roll", "Relay switch",
]

with open(DATA / "suppliers.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["supplier_id", "supplier_name"])
    w.writerows(suppliers)

with open(DATA / "items.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["item_id", "item_name", "supplier_id", "contract_price", "stock_on_hand"])
    for i, name in enumerate(products, start=1):
        supplier_id = suppliers[(i - 1) % len(suppliers)][0]
        price = round(random.uniform(2, 250), 2)
        stock = random.randint(0, 500)
        w.writerow([f"I{i:03d}", name, supplier_id, price, stock])

print("Created data/suppliers.csv and data/items.csv")
