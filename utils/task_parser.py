def classify_task(task: str) -> str:
    task = task.lower()

    if "wikipedia.org" in task:
        return "scrape"

    elif "duckdb" in task or "parquet" in task or "s3://" in task:
        return "duckdb_query"

    elif "plot" in task or "scatterplot" in task or "regression line" in task:
        return "visualize"

    else:
        return "unknown"