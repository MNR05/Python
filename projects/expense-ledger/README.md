# Expense Ledger

**Problem:** Personal finance tools can be unnecessarily complex or require external accounts.

**Solution:** A local SQLite ledger supporting expense insertion and monthly totals by category, storing amounts as **integer cents** to avoid floating-point rounding.

```bash
python main.py --db demo.sqlite3 add --amount 12.50 --category food --date 2026-11-22
python main.py --db demo.sqlite3 summary --month 2026-11
```

The database stays on your machine and is ignored by Git. This is a CLI demonstration, not financial advice.
