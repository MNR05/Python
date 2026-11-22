"""Minimal local expense ledger using SQLite and integer cents."""
import argparse
import json
import sqlite3
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

def init_db(db):
    db.execute("""CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        spent_on TEXT NOT NULL,
        category TEXT NOT NULL,
        amount_cents INTEGER NOT NULL CHECK(amount_cents > 0),
        note TEXT NOT NULL DEFAULT '')""")
    db.commit()

def cents(value):
    try:
        amount = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError("Amount must be a number") from exc
    if not amount.is_finite() or amount <= 0 or amount.as_tuple().exponent < -2:
        raise ValueError("Amount must be positive and have at most two decimals")
    total = int(amount * 100)
    if total > 100_000_000_000:
        raise ValueError("Amount too large")
    return total

def add_expense(db, amount, category, spent_on, note=""):
    date.fromisoformat(spent_on)
    category = category.strip()
    if not 1 <= len(category) <= 60:
        raise ValueError("Category must be 1-60 characters")
    with db:
        record = db.execute(
            "INSERT INTO expenses (spent_on, category, amount_cents, note) VALUES (?, ?, ?, ?)",
            (spent_on, category, cents(amount), note.strip()[:200]))
    return record.lastrowid

def summary(db, month):
    if len(month) != 7 or month[4] != "-":
        raise ValueError("Month must use YYYY-MM")
    date.fromisoformat(month + "-01")
    rows = db.execute(
        "SELECT category, SUM(amount_cents) FROM expenses WHERE substr(spent_on, 1, 7) = ? GROUP BY category ORDER BY category",
        (month,)).fetchall()
    return {"month": month, "total_cents": sum(row[1] for row in rows), "by_category_cents": dict(rows)}

def main():
    parser = argparse.ArgumentParser(description="Offline expense tracker")
    parser.add_argument("--db", default="expenses.sqlite3")
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add")
    add.add_argument("--amount", required=True)
    add.add_argument("--category", required=True)
    add.add_argument("--date", default=date.today().isoformat())
    add.add_argument("--note", default="")
    monthly = commands.add_parser("summary")
    monthly.add_argument("--month", default=date.today().strftime("%Y-%m"))
    args = parser.parse_args()
    Path(args.db).parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(args.db) as db:
        init_db(db)
        if args.command == "add":
            print(json.dumps({"id": add_expense(db, args.amount, args.category, args.date, args.note)}))
        else:
            print(json.dumps(summary(db, args.month), indent=2))

if __name__ == "__main__":
    main()
