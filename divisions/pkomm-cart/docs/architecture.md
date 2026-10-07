# Architecture

## Goal
Build an end-to-end e-commerce analytics system that supports incremental loads (only new/changed data), produces trusted analytics tables, and powers a KPI dashboard.

## Layers
1. Source (daily drops): data/source/day=YYYY-MM-DD/
2. Ingestion: reads source drops and lands raw data
3. Bronze (raw, immutable): append-only
4. Silver (clean + incremental merge): upserts based on primary key + updated_at
5. Gold (analytics): star schema facts/dimensions + KPI tables
6. Serving: DuckDB + Streamlit dashboard
7. Quality + Monitoring: checks run on every pipeline execution
8. Orchestration: single pipeline runner controls stage order

## Key design principles
- Bronze is immutable to support audit and replay
- Silver is the “truth layer” with standardized schema and incremental merge logic
- Gold is shaped for analytics (facts/dims) and KPI reporting

## Backfill Range (Local)
For this portfolio project, the local backfill used for dashboard realism starts from **2026-01-05** through the latest generated date.
This avoids partial replays during development while keeping the pipeline behavior realistic (daily incremental loads + late updates).
