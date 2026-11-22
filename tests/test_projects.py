"""Standard-library tests: python -m unittest discover -s tests -v"""
import importlib.util
import sqlite3
import tempfile
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def load(name, location):
    spec = importlib.util.spec_from_file_location(name, ROOT / location)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

csv_tool = load("csv_tool", "projects/csv-insights/main.py")
duplicates = load("duplicates", "projects/duplicate-finder/main.py")
expenses = load("expenses", "projects/expense-ledger/main.py")

class CsvTests(unittest.TestCase):
    def test_profile(self):
        p = csv_tool.profile_csv(ROOT / "projects/csv-insights/sample.csv")
        self.assertEqual(p["rows"], 4)
        self.assertEqual(p["missing"]["revenue"], 1)
        self.assertEqual(p["numeric_columns"]["orders"]["count"], 4)

    def test_empty_header(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "empty.csv"
            path.write_text("", encoding="utf-8")
            with self.assertRaises(ValueError):
                csv_tool.profile_csv(path)

class DuplicateTests(unittest.TestCase):
    def test_groups(self):
        self.assertEqual(
            duplicates.find_duplicates(ROOT / "projects/duplicate-finder/fixtures"),
            [["a.txt", "b.txt"]])

class ExpenseTests(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(":memory:")
        expenses.init_db(self.db)

    def tearDown(self):
        self.db.close()

    def test_totals(self):
        expenses.add_expense(self.db, "12.50", "food", "2026-11-22")
        expenses.add_expense(self.db, "3.20", "travel", "2026-11-23")
        self.assertEqual(expenses.summary(self.db, "2026-11")["total_cents"], 1570)

    def test_invalid_money(self):
        for amount in ("-1", "0", "NaN", "1.234"):
            with self.subTest(amount=amount), self.assertRaises(ValueError):
                expenses.cents(amount)
