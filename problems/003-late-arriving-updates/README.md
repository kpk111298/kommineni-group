# 003: Late payments flip the revenue number

**Division:** Meel Cart
**Domain:** Incremental loading
**Level:** 2
**Status:** Fixed, needs tests and write-up

## The ticket
Finance: Monday's revenue looked fine on Monday. By Thursday it was lower. Why does the past keep moving?

## What is actually wrong
Orders, payments and shipments change after they first arrive. A payment fails, then succeeds two days later. A naive daily load either misses the update or counts the record twice.

## The fix
Already built in `divisions/meel-cart`. See [incremental-strategy.md](../../divisions/meel-cart/docs/incremental-strategy.md).
- Bronze stays append-only, so nothing is lost.
- Silver upserts by business key and keeps a record only if its `updated_at` is newer.
- `order_items` stays append-only.
- Empty files are handled safely, and `backfill.py` replays a date range.

## Still to do
- Add tests (the `tests/` folder is empty).
- Before and after numbers for the write-up.
- AWS and Azure table.
