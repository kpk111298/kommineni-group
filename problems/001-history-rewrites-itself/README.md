# 001: Yesterday's sales changed overnight

**Division:** Meel Motors
**Domain:** Incremental loading
**Level:** 2
**Status:** Open

## The ticket
The Chicago branch manager: Last Tuesday showed 6 cars sold on Wednesday morning. Today the same Tuesday shows 3. Which number do I report?

## What is actually wrong
`divisions/meel-motors/data_generator/generate_data.py` uses `random.seed(None)` and rebuilds the last 30 days of sales every run. The daily GitHub Action runs it, then reloads bronze from scratch. So every morning the whole past month is replaced with new random history. Nothing that happened yesterday stays true.

## Why it matters
Managers lose trust in the dashboard. Monthly targets and commissions depend on the past staying fixed.

## Constraints
Free tools only. The live dashboard must keep working.

## The fix (plan)
1. Replace `data_generator/` with the Meel Motors DMS in `sources/dms/`. It writes sales one at a time into Postgres, uses a fixed seed per day, and never rewrites a closed day.
2. Add real business patterns: busy Saturdays, month-end rush, no Sunday sales in Illinois, tax refund season, top sellers, lot-age discounts, repeat service customers.
3. Make bronze append-only with `_ingested_at` and `_source_file`, never a full replace.
4. Make dbt silver and gold models incremental.
5. Add a test: a closed day's totals never change after it closes.

## Proof
To do.

## On AWS and Azure
To do.

## Write-up
To do.
