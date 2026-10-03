# Incremental Strategy

## Problem we are solving
In real e-commerce systems, records change after the first event:
- Orders move through statuses (PLACED → SHIPPED → DELIVERED)
- Payments can fail first and succeed later
- Shipments update as packages move

Reprocessing all history every day is slow and costly. So we load incrementally.

## Rules
### Upsert tables (customers, products, orders, payments, shipments)
- Insert if primary key is new
- Update if primary key exists AND incoming updated_at is newer
- Ignore if primary key exists AND incoming updated_at is older/equal

### Append-only table (order_items)
- Insert new rows only (no updates)

## Layer responsibility
- Bronze: store raw data as received (append-only, immutable)
- Silver: enforce schema + dedupe + apply incremental upsert logic
- Gold: build analytics models (facts/dims) and KPIs for reporting
