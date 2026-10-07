from __future__ import annotations

from datetime import datetime, date, timedelta
from typing import Iterator


def parse_yyyy_mm_dd(s: str) -> date:
    return datetime.strptime(s, "%Y-%m-%d").date()


def to_iso_dt(d: date, hour: int = 12, minute: int = 0, second: int = 0) -> str:
    return datetime(d.year, d.month, d.day, hour, minute, second).strftime("%Y-%m-%d %H:%M:%S")


def daterange(start: date, end: date) -> Iterator[date]:
    cur = start
    while cur <= end:
        yield cur
        cur = cur + timedelta(days=1)
