# Scenarios

Scenarios are bigger business events you trigger from the Control Room. Each one hits one or more source systems and creates at least one problem for the roadmap.

## Business events

| Scenario | Divisions hit | What breaks or gets hard |
|---|---|---|
| Black Friday, 10x normal traffic | Meel Cart, Meel Move, Meel Pay | Pipeline speed, late shipments, payment retries |
| Chip shortage, inventory nearly empty | Meel Motors | Inventory reports, price swings, waitlists |
| Real recall on a model the dealership sells | Meel Motors | Service job spike, customer lookups by VIN |
| Storm closes the Dallas branch for 3 days | Meel Motors, Meel Move | Missing days that are not errors, delayed targets |
| Competitor price war, daily price changes | Meel Cart | Price history tracking (SCD Type 2) |
| Interest rate jump | Meel Pay, Meel Motors | Fewer approvals, forecasts off |
| Flu season peak | Meel Care | Visit volume, staffing reports, claim backlog |
| Tariff on imported cars | Meel Motors, HQ accounting | Price changes on a set date, margin reports |
| Viral product, sold out in hours | Meel Cart | Overselling, inventory going negative |
| New branch opens | Meel Motors, HQ | New location in every table, no history yet |
| Kommineni Group buys another dealership | Meel Motors, HQ | Their messy data with different IDs merged into yours |
| Old DMS replaced by a new system | Meel Motors | Migration with two systems running side by side |

## Technical events

| Scenario | What breaks or gets hard |
|---|---|
| Supplier changes the file format with no warning | Schema drift |
| App team renames a column in Postgres | Broken pipeline, data contracts |
| Empty file or duplicate file arrives | Wiped or double-counted dashboards |
| Daylight saving time | One hour happens twice in November and vanishes in March |
| Leap day and year-end close | Date math bugs, fiscal year reports |
| Payment retry sends the same charge twice | Dedupe and idempotency |
| A job fails halfway through the night | Safe reruns, backfills |
| Ransomware scare | Prove you can restore yesterday's data |
| Cloud region outage | Failover, freshness alerts |
| Customer asks to be deleted (GDPR, CCPA) | Finding one person across every system |
| Auditor asks who changed a number in March | Lineage and audit history |
| The engineer who built a pipeline leaves | No docs, no tests, you inherit it |
| Finance and marketing report different revenue | One metric definition |

## How a scenario becomes a problem

1. Trigger the scenario in the Control Room for a date range.
2. Let the daily pipeline run and see what breaks.
3. Log it as a GitHub Issue, written like a business request.
4. Fix it, test it, and write it up using `problems/_template.md`.
