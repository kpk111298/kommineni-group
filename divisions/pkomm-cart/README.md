<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../brand/pkomm-cart/lockup-dark.svg">
  <img src="../../brand/pkomm-cart/lockup-light.svg" alt="Pkomm Cart" height="72">
</picture>

# Pkomm Cart – E-commerce Incremental Analytics

This project simulates a real-world **e-commerce analytics platform** built for a fictional company called **Pkomm Cart**.

The goal is to demonstrate how daily transactional data is processed **incrementally**, while handling late updates and changing business states, and then surfaced through a KPI dashboard.

---

## Business Problem

E-commerce teams need reliable answers to questions like:
- How many orders did we process today?
- What is today’s revenue and average order value?
- Are payments failing more than usual?
- Are shipments being delivered on time?

Raw event data alone cannot answer these questions because:
- orders change status over time
- payments can fail and retry
- shipments are delivered days later

This project models that reality.

---

## Architecture Overview

**Source → Bronze → Silver → Gold → Dashboard**

### Source (Daily Data)
- Daily drops of customers, orders, order_items, payments, and shipments
- Includes late-arriving updates and status changes
- Simulates real ingestion behavior

### Bronze Layer (Raw History)
- Append-only storage
- No transformations or deduplication
- Preserves full data history for audit and replay

### Silver Layer (Clean & Incremental)
- Deduplicates records using business keys
- Uses timestamps to keep the latest version of each record
- Handles late updates and empty files safely

### Gold Layer (Analytics Ready)
- Order-level fact table
- Daily KPI table with:
  - Orders
  - Revenue
  - Average Order Value (AOV)
  - Payment failure rate
  - Delivery rate

---

## Dashboard

A Streamlit dashboard built on the Gold layer shows:
- KPI tiles
- Daily trends
- Filters by date and channel
- Order drill-down table
- “Data through” date
- “Last pipeline run” status

---

## How to Run

### Run daily pipeline (end-to-end)
```bash
RUN_DATE=2026-01-26 PREV_DATE=2026-01-25 python -m src.pipeline.run_daily

