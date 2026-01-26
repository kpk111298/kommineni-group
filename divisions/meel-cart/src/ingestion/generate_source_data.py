from __future__ import annotations

import os
import random
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from faker import Faker

from src.utils.date_helpers import parse_yyyy_mm_dd, to_iso_dt

fake = Faker()
Faker.seed(42)
random.seed(42)
np.random.seed(42)


@dataclass
class VolumeConfig:
    customers_per_day: Tuple[int, int] = (80, 140)
    products_total: Tuple[int, int] = (80, 140)
    orders_per_day: Tuple[int, int] = (300, 700)
    items_per_order: Tuple[int, int] = (1, 4)


ORDER_CHANNELS = ["WEB", "MOBILE", "MARKETPLACE"]
PAYMENT_METHODS = ["CARD", "PAYPAL", "APPLE_PAY"]
PAYMENT_PROVIDERS = ["STRIPE", "ADYEN", "PAYPAL_SIM"]
CARRIERS = ["UPS", "FEDEX", "USPS"]
CATEGORIES = ["Electronics", "Home", "Fashion", "Beauty", "Sports", "Grocery"]
BRANDS = ["Acme", "Nova", "Zenith", "Pioneer", "Orbit", "Vertex"]


def _safe_email() -> str:
    return fake.user_name() + "@example.com"


def _rand_ts(run_date: date, min_hour: int = 0, max_hour: int = 23) -> str:
    hour = random.randint(min_hour, max_hour)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return to_iso_dt(run_date, hour, minute, second)


def generate_products(run_date: date, cfg: VolumeConfig) -> pd.DataFrame:
    n = random.randint(*cfg.products_total)
    rows = []
    for i in range(1, n + 1):
        created = run_date - timedelta(days=random.randint(5, 60))
        updated = created + timedelta(days=random.randint(0, 10))
        if updated > run_date:
            updated = run_date
        base_price = round(random.uniform(5.0, 500.0), 2)
        rows.append(
            {
                "product_id": f"P{i:05d}",
                "created_at": to_iso_dt(created, 9, 0, 0),
                "updated_at": _rand_ts(updated),
                "product_name": f"{random.choice(BRANDS)} {random.choice(['Pro', 'Max', 'Lite', 'Plus'])} {random.choice(['Kit', 'Bundle', 'Item', 'Pack'])}",
                "category": random.choice(CATEGORIES),
                "brand": random.choice(BRANDS),
                "base_price": base_price,
                "active_flag": "Y",
            }
        )
    return pd.DataFrame(rows)


def generate_customers(run_date: date, cfg: VolumeConfig, start_id: int = 1) -> pd.DataFrame:
    n = random.randint(*cfg.customers_per_day)
    rows = []
    for i in range(start_id, start_id + n):
        created = run_date - timedelta(days=random.randint(0, 30))
        updated = created + timedelta(days=random.randint(0, 5))
        if updated > run_date:
            updated = run_date
        rows.append(
            {
                "customer_id": f"C{i:06d}",
                "created_at": to_iso_dt(created, 10, 0, 0),
                "updated_at": _rand_ts(updated),
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "email": _safe_email(),
                "phone": fake.msisdn()[:10],
                "city": fake.city(),
                "state": fake.state_abbr(),
                "country": "US",
                "customer_segment": random.choice(["New", "Regular", "VIP"]),
            }
        )
    return pd.DataFrame(rows)


def generate_orders_items_payments_shipments(
    run_date: date,
    cfg: VolumeConfig,
    customers: pd.DataFrame,
    products: pd.DataFrame,
    start_order_id: int = 1,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    n_orders = random.randint(*cfg.orders_per_day)

    customer_ids = customers["customer_id"].tolist()
    product_ids = products["product_id"].tolist()
    product_price_map: Dict[str, float] = dict(zip(products["product_id"], products["base_price"]))

    orders_rows: List[dict] = []
    items_rows: List[dict] = []
    payments_rows: List[dict] = []
    shipments_rows: List[dict] = []

    order_item_id = 1
    payment_id = 1
    shipment_id = 1

    for oid in range(start_order_id, start_order_id + n_orders):
        order_id = f"O{oid:07d}"
        cust_id = random.choice(customer_ids)
        created_at = _rand_ts(run_date, 0, 23)
        updated_at = created_at

        status = random.choices(
            population=["PLACED", "CONFIRMED", "SHIPPED", "DELIVERED"],
            weights=[0.35, 0.35, 0.20, 0.10],
            k=1,
        )[0]

        orders_rows.append(
            {
                "order_id": order_id,
                "created_at": created_at,
                "updated_at": updated_at,
                "customer_id": cust_id,
                "order_status": status,
                "order_channel": random.choice(ORDER_CHANNELS),
                "currency": "USD",
                "shipping_city": fake.city(),
                "shipping_state": fake.state_abbr(),
                "shipping_country": "US",
            }
        )

        # Items
        n_items = random.randint(*cfg.items_per_order)
        chosen_products = random.sample(product_ids, k=min(n_items, len(product_ids)))
        for pid in chosen_products:
            qty = random.randint(1, 3)
            unit_price = round(float(product_price_map[pid]) * random.uniform(0.90, 1.05), 2)
            line_amount = round(qty * unit_price, 2)
            items_rows.append(
                {
                    "order_item_id": f"OI{order_item_id:09d}",
                    "order_id": order_id,
                    "product_id": pid,
                    "quantity": qty,
                    "unit_price": unit_price,
                    "line_amount": line_amount,
                    "created_at": created_at,
                }
            )
            order_item_id += 1

        # Payment (one per order for v1)
        order_total = float(sum(r["line_amount"] for r in items_rows if r["order_id"] == order_id))
        pay_status = random.choices(
            population=["CAPTURED", "FAILED", "AUTHORIZED"],
            weights=[0.85, 0.08, 0.07],
            k=1,
        )[0]
        payments_rows.append(
            {
                "payment_id": f"PAY{payment_id:09d}",
                "order_id": order_id,
                "created_at": created_at,
                "updated_at": created_at,
                "payment_status": pay_status,
                "payment_method": random.choice(PAYMENT_METHODS),
                "amount": round(order_total, 2),
                "currency": "USD",
                "provider": random.choice(PAYMENT_PROVIDERS),
            }
        )
        payment_id += 1

        # Shipment (only for SHIPPED/DELIVERED on Day 1)
        if status in ["SHIPPED", "DELIVERED"]:
            shipped_at = created_at
            delivered_at = None
            ship_status = "IN_TRANSIT"
            if status == "DELIVERED":
                delivered_at = _rand_ts(run_date, 12, 23)
                ship_status = "DELIVERED"

            shipments_rows.append(
                {
                    "shipment_id": f"S{shipment_id:09d}",
                    "order_id": order_id,
                    "created_at": created_at,
                    "updated_at": created_at,
                    "carrier": random.choice(CARRIERS),
                    "shipping_status": ship_status,
                    "shipped_at": shipped_at,
                    "delivered_at": delivered_at,
                    "estimated_delivery_date": (run_date + timedelta(days=random.randint(2, 5))).isoformat(),
                }
            )
            shipment_id += 1

    return (
        pd.DataFrame(orders_rows),
        pd.DataFrame(items_rows),
        pd.DataFrame(payments_rows),
        pd.DataFrame(shipments_rows),
    )


def write_day_files(out_dir: Path, tables: Dict[str, pd.DataFrame]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, df in tables.items():
        df.to_csv(out_dir / f"{name}.csv", index=False)


def main() -> None:
    run_date_str = os.getenv("RUN_DATE", "").strip()
    if not run_date_str:
        raise SystemExit("Set RUN_DATE like: RUN_DATE=2026-01-01 python src/ingestion/generate_source_data.py")

    run_date = parse_yyyy_mm_dd(run_date_str)
    cfg = VolumeConfig()

    products = generate_products(run_date, cfg)
    customers = generate_customers(run_date, cfg, start_id=1)

    orders, order_items, payments, shipments = generate_orders_items_payments_shipments(
        run_date=run_date,
        cfg=cfg,
        customers=customers,
        products=products,
        start_order_id=1,
    )

    out_dir = Path("data/source") / f"day={run_date_str}"
    write_day_files(
        out_dir,
        {
            "customers": customers,
            "products": products,
            "orders": orders,
            "order_items": order_items,
            "payments": payments,
            "shipments": shipments,
        },
    )

    print(f"Generated source data for {run_date_str} in {out_dir}")
    for name, df in [
        ("customers", customers),
        ("products", products),
        ("orders", orders),
        ("order_items", order_items),
        ("payments", payments),
        ("shipments", shipments),
    ]:
        print(f"{name}: {len(df):,} rows")


if __name__ == "__main__":
    main()
