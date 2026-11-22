# CSV Insights

**Problem:** Quickly understand a CSV's shape before building a dashboard or data pipeline.

**Approach:** Use `csv.DictReader` to summarize row count, columns, missing values and fully numeric columns. No pandas required.

```bash
python main.py sample.csv
```

**Trade-off:** Designed for small and medium CSV files that fit in memory. For large datasets, use streaming aggregation or a database; this tool intentionally does not infer complex types.
