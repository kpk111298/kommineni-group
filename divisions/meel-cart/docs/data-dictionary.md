# Data Dictionary (Source Tables)

This project simulates real e-commerce source systems and generates daily drops.

## customers (upsert)
Primary key: customer_id
Incremental rule: update record only when updated_at is newer

Columns:
- customer_id
- created_at
- updated_at
- first_name
- last_name
- email
- phone
- city
- state
- country
- customer_segment

## products (upsert)
Primary key: product_id
Incremental rule: update record only when updated_at is newer

Columns:
- product_id
- created_at
- updated_at
- product_name
- category
- brand
- base_price
- active_flag

## orders (upsert)
Primary key: order_id
Incremental rule: update record only when updated_at is newer

Columns:
- order_id
- created_at
- updated_at
- customer_id
- order_status
- order_channel
- currency
- shipping_city
- shipping_state
- shipping_country

## order_items (append-only)
Primary key: order_item_id
Incremental rule: new rows only (append)

Columns:
- order_item_id
- order_id
- product_id
- quantity
- unit_price
- line_amount
- created_at

## payments (upsert)
Primary key: payment_id
Incremental rule: update record only when updated_at is newer

Columns:
- payment_id
- order_id
- created_at
- updated_at
- payment_status
- payment_method
- amount
- currency
- provider

## shipments (upsert)
Primary key: shipment_id
Incremental rule: update record only when updated_at is newer

Columns:
- shipment_id
- order_id
- created_at
- updated_at
- carrier
- shipping_status
- shipped_at
- delivered_at
- estimated_delivery_date
