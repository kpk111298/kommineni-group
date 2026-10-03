# Source systems

Real companies don't have a data generator. They run business software, and data is a side effect of doing business. Every Kommineni Group division follows that standard.

## Each division has real-style systems

| Division | System | Industry name | Writes to |
|---|---|---|---|
| Meel Motors | Sales, inventory, service | DMS (dealer management system) | Postgres `meel_motors_dms` |
| Meel Cart | Storefront, orders, payments | E-commerce platform | Postgres `meel_cart_store` + click events |
| Meel Care | Patients, visits, labs, prescriptions | EHR (electronic health record), Synthea based | FHIR JSON + Postgres `meel_care_ehr` |
| Meel Care | Insurance claims | Claims system | Daily claim files |
| Meel Pay | Loans and card payments | Loan origination system, payment processor | Postgres `meel_pay_core` |
| Meel Move | Shipments, trucks, GPS | TMS (transportation management system) | GPS event stream |
| Meel Reach | Campaigns, ad spend, email | Marketing platform | API with paging and rate limits |
| HQ | HR, payroll, ledger, support tickets, IT logs | HRIS, ERP, help desk | Mixed |

Folders follow the same naming: `divisions/meel-motors/sources/dms/`, not `data_generator/`.

## Rules every source system follows

1. It writes events through the day, one sale or visit at a time, not one big file at night.
2. It never rewrites the past. A closed day stays closed. Corrections arrive as new records, the way refunds and adjustments work in real life.
3. It uses a fixed seed per day, so any day can be replayed and gives the same result.
4. It reads the real world feeds in `shared/world/` (see [real-world-data.md](real-world-data.md)).
5. It follows business logic, not plain random numbers.

## Business logic examples

Meel Motors:
- Saturday is the busiest day. Month-end gets a rush as salespeople chase targets.
- Illinois bans car sales on Sundays, so Illinois branches show zero Sunday sales. Other states have their own Sunday rules.
- Spring gets a lift from tax refund season. December gets year-end clearance deals.
- A few top salespeople sell far more than the rest.
- Cars that sit on the lot longer sell at bigger discounts.
- Past buyers come back for service. Service needs follow the car's age and mileage.

Meel Cart:
- Evenings and weekends are busiest. Black Friday and Cyber Monday spike hard.
- Some payments fail and retry. Some orders get returned weeks later.

Meel Care:
- Flu season raises visits in winter. Claims get adjusted weeks after the visit.

## AI generated text

Code makes the rows. AI makes the messy text that code can't fake well: doctor notes, support tickets, product reviews, supplier emails. Text is generated once with a local model (Ollama), saved, and reused, so runs stay repeatable and free.

## Honesty

Inside the company, everything uses business names. Every README and every blog post says clearly: Kommineni Group is a simulated company built by Prameel Kommineni as a data engineering showcase.
