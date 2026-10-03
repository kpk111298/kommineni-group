# Kommineni Group: the company

Kommineni Group is a simulated company built by Prameel Kommineni as a data engineering showcase. The world data it reacts to is real. The business is not.

## The story

Kommineni Group is a family-run group based in Illinois. It started with a car dealership and grew into retail, healthcare, logistics, finance and marketing. Like most real companies, it grew fast and its data grew messy. Each division bought its own systems, and nobody planned how they would talk to each other.

The data engineering team (that is me) gets the tickets.

## Divisions

**Meel Motors** sells and services cars at 5 branches, including Dallas and Chicago. Runs on a DMS. Data: vehicles, sales, service jobs, employees, branch targets.

**Meel Cart** is the group's online store, selling in the US, Canada, the UK, Europe and India. Data: customers, products, orders, payments, shipments, clicks. Orders change status, payments fail and retry, shipments arrive late, currencies and time zones differ.

**Meel Care** (planned) runs outpatient clinics and a small health plan. Runs on an EHR and a claims system, with patients from Synthea. Data: patients, visits, labs, prescriptions, claims. Brings FHIR, HIPAA de-identification and claim adjustment problems.

**Meel Move** (planned) delivers Meel Cart orders and moves cars between branches. Data: shipments, trucks, routes, GPS pings. Brings streaming and geo problems.

**Meel Pay** (planned) handles car loans for Meel Motors and card payments for Meel Cart. Data: applications, payments, refunds, chargebacks. Brings fraud, PII and audit problems.

**Meel Reach** (planned) runs marketing for every division. Data: campaigns, ad spend, web and app clicks, email sends. Brings high-volume events, attribution and API ingestion problems.

## Kommineni Group HQ

The back office every division shares:

- **HR and payroll.** Hiring, pay, promotions, transfers, attrition.
- **Accounting.** The general ledger and month-end close, where every division's numbers must add up to one company total.
- **Customer support.** Tickets, call logs, satisfaction scores.
- **Supply chain.** Suppliers, purchase orders, warehouse stock, reorder points.
- **IT and security.** Logins, app errors, server logs.

## Shared data

These live in `shared/` and every division uses them:

- **Customers.** One person can buy a car at Meel Motors, visit a Meel Care clinic and shop on Meel Cart under different emails. Matching them is a real problem (identity resolution).
- **Employees.** One HR list across divisions, with promotions and transfers over time (SCD Type 2).
- **Locations.** Branches, clinics, warehouses, offices.
- **Calendar.** One date table with fiscal months, holidays and weekends.
- **World.** Real public data: rates, prices, weather, recalls, holidays. See [real-world-data.md](real-world-data.md).

## How it runs

1. **The Control Room** (private Streamlit app behind Cloudflare Access) sets each day: normal, or a scenario like Black Friday. See [scenarios.md](scenarios.md).
2. **Source systems** run the business and write data the way real software does. See [source-systems.md](source-systems.md).
3. **Pipelines** load bronze, silver and gold, with tests at every step.
4. **Dashboards and pkomm.com/group** show the business the results.
5. **Tickets** come in as GitHub Issues when something looks wrong. Each one gets fixed, tested and written up on pkomm.com.

Engineering practices are in [engineering-standards.md](engineering-standards.md).

## Rules for every problem

1. Write the ticket first: what the business sees, what broke, why it matters.
2. Solve it with free tools that run on a laptop.
3. Prove it with tests or before and after numbers.
4. Add the AWS and Azure versions in a short table. See [tool-map.md](tool-map.md).
5. Publish the write-up on pkomm.com and link it in the problem folder.
