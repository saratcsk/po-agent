# PO Agent

An AI agent that reads purchase order emails, extracts the order details, checks them against supplier contracts and stock, sends exceptions to a person for approval, and creates a draft order.

All data in this repo is synthetic.

## Status

- [x] Week 1: master data, synthetic PO emails with known correct answers, first Claude API call
- [ ] Week 2: structured extraction with validation
- [ ] Week 3: RAG over supplier contracts
- [ ] Week 4: agent with tools and human approval
- [ ] Week 5: evaluation (accuracy, hallucination, cost, latency)
- [ ] Week 6: Streamlit UI, Docker, demo

## Run it

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # then paste your Anthropic API key into .env
python src/first_call.py
python src/make_master_data.py
python src/generate_emails.py
```
