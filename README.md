# Kommineni Group

A simulated company built to practise real data engineering problems, solve them, and write them up.

Kommineni Group runs six businesses and a shared back office. Their systems create the kind of messy data real companies create: late records, duplicate customers, broken files, slow queries, privacy rules. The business reacts to real world data: interest rates, gas prices, weather, recalls and holidays. Every problem gets logged like a work ticket, solved with free tools, tested, and published as a case study on [pkomm.com/blog](https://pkomm.com/blog).

The focus is the problem solving. Each solution runs locally for free, and a short table shows how the same fix would look on AWS and on Azure.

Kommineni Group is not a real company. It is a data engineering showcase built by [Prameel Kommineni](https://pkomm.com). The world data is real, the business is simulated.

## The divisions

| Division | Business | Status | Folder |
|---|---|---|---|
| Meel Motors | Car dealership, 5 branches, sales and service | Live | [divisions/meel-motors](divisions/meel-motors) |
| Meel Cart | Online store selling worldwide | Live | [divisions/meel-cart](divisions/meel-cart) |
| Meel Care | Clinics and a health plan | Planned | |
| Meel Move | Logistics, deliveries and car transfers | Planned | |
| Meel Pay | Car loans, card payments, fraud checks | Planned | |
| Meel Reach | Marketing, campaigns, clicks, ad spend | Planned | |
| HQ | HR, accounting, support, supply chain, IT | Planned | |

All divisions share one customer list, one employee list, one calendar, one set of locations and the same real world data. That makes it one company, not seven side projects.

## How it works

Control Room (pick the day or a scenario) → source systems run the business → pipelines → dashboards and group.pkomm.com → ticket, fix, write-up → next problem.

- [The company](docs/company.md)
- [Source systems](docs/source-systems.md)
- [Real world data](docs/real-world-data.md)
- [Scenarios](docs/scenarios.md)
- [Engineering standards](docs/engineering-standards.md)
- [Tool map: local, AWS, Azure](docs/tool-map.md)

## The problems

| # | Problem | Division | Domain | Level | Status |
|---|---|---|---|---|---|
| 001 | [Yesterday's sales changed overnight](problems/001-history-rewrites-itself) | Meel Motors | Incremental loading | 2 | Open |
| 002 | [The repo that grows every day](problems/002-database-in-git) | Meel Motors | Storage and cost | 1 | Open |
| 003 | [Late payments flip the revenue number](problems/003-late-arriving-updates) | Meel Cart | Incremental loading | 2 | Solved, write-up pending |

The full roadmap, from beginner to top-company level, is in [problems/README.md](problems/README.md).

## Repo layout

```
kommineni-group/
  divisions/     one folder per business, each with its source systems and pipelines
  shared/        company-wide data: customers, employees, locations, calendar, world
  control-room/  private app that sets the day and triggers scenarios
  problems/      one folder per problem: ticket, solution, tests, write-up
  docs/          company story, standards, tool map
```

## Free tools used

Python, Postgres, DuckDB, dbt, Streamlit, GitHub Actions, Docker. Coming: PySpark, Delta Lake or Iceberg, Dagster, Redpanda, Debezium, Terraform with LocalStack and Azurite, Synthea, Ollama.

## History

Meel Motors started as `kpk111298/kommineni-automotive-pipeline` and Meel Cart as `kpk111298/ecommerce-incremental-analytics`. Both were merged here with their full commit history.

## License

All rights reserved. See [LICENSE](LICENSE).
