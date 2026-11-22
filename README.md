# Python Engineering Labs

Practical, dependency-free Python projects showcasing data processing, automation and reliable CLI tools. Each mini-project solves a small problem end to end, with tests and examples.

> **Provenance:** These are new portfolio examples prepared in 2026. The existence of this repository since 2024 is not evidence that the code below was written then.

## Projects

| Project | Problem | What it demonstrates |
| --- | --- | --- |
| [CSV Insights](./projects/csv-insights/) | Inspect unfamiliar datasets quickly | CSV parsing, missing values, basic statistics and a CLI |
| [Duplicate Finder](./projects/duplicate-finder/) | Identify redundant files safely | SHA-256 streaming, filesystem traversal and non-destructive output |
| [Expense Ledger](./projects/expense-ledger/) | Track expenses without a cloud account | SQLite transactions, input validation and monthly aggregation |

## Run

Requires **Python 3.10+**. No third-party libraries or credentials required.

```bash
python projects/csv-insights/main.py projects/csv-insights/sample.csv
python projects/duplicate-finder/main.py projects/duplicate-finder/fixtures
python projects/expense-ledger/main.py --db /tmp/ledger.db add --amount 12.50 --category food --date 2026-11-22
python -m unittest discover -s tests -v
```

All sample data is fictional. No actual customer information or proprietary code is used. This is not a claim of a historical 2018 codebase or production deployment.
