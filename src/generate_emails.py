"""Step 3: create 50 fake PO emails where we already know the right answer.

Python picks each order (so the truth is known), then Claude writes it up as a
realistic email. The known answers go to data/gold_orders.csv, which becomes
the test set for measuring accuracy in Week 5.
"""
import csv
import os
import random
from datetime import date, timedelta
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
random.seed(7)

DATA = Path(__file__).resolve().parent.parent / "data"
EMAILS = DATA / "emails"
EMAILS.mkdir(exist_ok=True)

suppliers = {r["supplier_id"]: r["supplier_name"] for r in csv.DictReader(open(DATA / "suppliers.csv"))}
items = list(csv.DictReader(open(DATA / "items.csv")))

STYLES = ["short and formal", "casual and friendly", "long with extra small talk",
          "a forwarded email thread", "bullet points", "rushed with a typo or two"]

# Some orders contain a deliberate problem, so the agent has something to catch later.
PROBLEMS = ["none"] * 6 + ["price_above_contract", "quantity_above_stock", "unknown_item"]

gold_rows = []
for n in range(1, 51):
    item = random.choice(items)
    problem = random.choice(PROBLEMS)
    quantity = random.randint(5, 200)
    price = float(item["contract_price"])
    item_name = item["item_name"]

    if problem == "price_above_contract":
        price = round(price * random.uniform(1.10, 1.40), 2)
    elif problem == "quantity_above_stock":
        quantity = int(item["stock_on_hand"]) + random.randint(20, 100)
    elif problem == "unknown_item":
        item_name = "Titanium flange 4in"

    need_by = date(2026, 11, 1) + timedelta(days=random.randint(0, 60))
    supplier = suppliers[item["supplier_id"]]

    prompt = (
        f"Write a purchase order email from a buyer at Acme Manufacturing to {supplier}. "
        f"Order {quantity} units of '{item_name}' at ${price:.2f} each, needed by {need_by:%B %d, %Y}. "
        f"Style: {random.choice(STYLES)}. Include a subject line. Use only these facts. "
        f"Return only the email text."
    )
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=600,
        messages=[{"role": "user", "content": prompt}],
    )
    email_id = f"po_{n:03d}"
    (EMAILS / f"{email_id}.txt").write_text(response.content[0].text)

    gold_rows.append({
        "email_id": email_id, "supplier": supplier, "item": item_name, "quantity": quantity,
        "unit_price": price, "need_by": need_by.isoformat(), "problem": problem,
    })
    print(f"{email_id} done ({problem})")

with open(DATA / "gold_orders.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=gold_rows[0].keys())
    w.writeheader()
    w.writerows(gold_rows)

print("Created 50 emails in data/emails and the answer key in data/gold_orders.csv")
