from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import duckdb
import pandas as pd


TABLES: List[str] = ["customers", "products", "orders", "order_items", "payments", "shipments"]


def _now_ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def load_day_to_bronze(run_date: str, db_path: str = "warehouse/ecomm.duckdb") -> Dict[str, int]:
    """
    Append source CSVs for a given day into bronze_* tables.
    Bronze is append-only and keeps raw-ish data + ingestion metadata.
    """
    day_dir = Path("data/source") / f"day={run_date}"
    if not day_dir.exists():
        raise SystemExit(f"Source folder not found: {day_dir}")

    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(db_path)
    con.execute("PRAGMA threads=4;")

    ingested_at = _now_ts()
    results: Dict[str, int] = {}

    for t in TABLES:
        csv_path = day_dir / f"{t}.csv"
        if not csv_path.exists():
            raise SystemExit(f"Missing source file: {csv_path}")

        df = pd.read_csv(csv_path)

        # Add ingestion metadata
        df["batch_date"] = run_date
        df["ingested_at"] = ingested_at
        df["source_file"] = str(csv_path)

        table_name = f"bronze_{t}"

        # Create table if not exists (schema inferred from df)
        con.register("df_tmp", df)
        con.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM df_tmp WHERE 1=0;")

        # Append rows
        con.execute(f"INSERT INTO {table_name} SELECT * FROM df_tmp;")

        results[t] = len(df)

    con.close()
    return results


def main() -> None:
    run_date = os.getenv("RUN_DATE", "").strip()
    if not run_date:
        raise SystemExit("Set RUN_DATE like: RUN_DATE=2026-01-01 python -m src.ingestion.load_bronze")

    out = load_day_to_bronze(run_date)
    print(f"Loaded Bronze for day={run_date} into warehouse/ecomm.duckdb")
    for k, v in out.items():
        print(f"{k}: {v:,} rows appended")


if __name__ == "__main__":
    main()
