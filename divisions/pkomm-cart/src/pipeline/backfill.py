from __future__ import annotations

import os
from datetime import timedelta

from src.utils.date_helpers import parse_yyyy_mm_dd, daterange


def _run(cmd: str) -> None:
    rc = os.system(cmd)
    if rc != 0:
        raise SystemExit(f"Command failed: {cmd}")


def main() -> None:
    start = os.getenv("START_DATE", "").strip()
    end = os.getenv("END_DATE", "").strip()
    if not start or not end:
        raise SystemExit("Use: START_DATE=2026-01-01 END_DATE=2026-01-25 python -m src.pipeline.backfill")

    start_d = parse_yyyy_mm_dd(start)
    end_d = parse_yyyy_mm_dd(end)

    # Ensure Day 1 exists as a fresh day (no prev required)
    # Our generator automatically uses "fresh day" behavior if prev day folder is missing.

    for d in daterange(start_d, end_d):
        ds = d.isoformat()
        prev = (d - timedelta(days=1)).isoformat()
        _run(f"RUN_DATE={ds} PREV_DATE={prev} python -m src.pipeline.run_daily")

    print(f"Backfill complete: {start} -> {end}")


if __name__ == "__main__":
    main()
