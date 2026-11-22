"""Summarize a CSV file using Python's standard library."""
import argparse
import csv
import json
from pathlib import Path
from statistics import mean


def profile_csv(path: str | Path) -> dict:
    with Path(path).open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError("CSV must contain a header row")
        fields = list(reader.fieldnames)
        rows = list(reader)
    missing = {name: 0 for name in fields}
    numeric = {name: [] for name in fields}
    for row in rows:
        for name in fields:
            value = (row.get(name) or "").strip()
            if not value:
                missing[name] += 1
                continue
            try:
                numeric[name].append(float(value))
            except ValueError:
                pass
    return {
        "rows": len(rows),
        "columns": fields,
        "missing": missing,
        "numeric_columns": {
            name: {"count": len(values), "min": min(values), "max": max(values), "mean": round(mean(values), 4)}
            for name, values in numeric.items()
            if values and len(values) == len(rows) - missing[name]
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Profile a CSV dataset.")
    parser.add_argument("file", help="Path to a UTF-8 CSV file")
    args = parser.parse_args()
    print(json.dumps(profile_csv(args.file), indent=2))


if __name__ == "__main__":
    main()
