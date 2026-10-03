# Problem roadmap

Levels:
1. Beginner. Every data engineer hits this in year one.
2. Working engineer. Common in interviews and real jobs.
3. Senior. Needs design trade-offs.
4. Top company. Scale, cost and reliability at once.

Copy [_template.md](_template.md) for each new problem.

## Logged

| # | Problem | Division | Domain | Level | Status |
|---|---|---|---|---|---|
| 001 | Yesterday's sales changed overnight | Meel Motors | Incremental loading | 2 | Open |
| 002 | The repo that grows every day | Meel Motors | Storage and cost | 1 | Open |
| 003 | Late payments flip the revenue number | Meel Cart | Incremental loading | 2 | Solved, write-up pending |

## Roadmap

### Ingestion
- A supplier sends CSVs with a new column every month (schema drift). Meel Cart, level 1
- Ad platform API returns 100 rows per page and rate limits after 50 calls. Meel Reach, level 2
- An empty file arrives and wipes out yesterday's dashboard. Meel Cart, level 1
- Copying the whole loans table every night takes 4 hours (change data capture). Meel Pay, level 3

### Data quality
- Same customer, three emails, two divisions (identity resolution). Shared, level 3
- Negative sale prices and cars sold before they were bought. Meel Motors, level 1
- Catch bad data before the CEO sees it, not after (quality gates and alerts). Meel Motors, level 2

### Modeling
- A salesperson moves branches and last year's branch revenue changes (SCD Type 2). Shared, level 2
- One star schema for sales across Meel Motors and Meel Cart. Shared, level 2
- Finance and marketing count customers differently (one metric definition). Meel Reach, level 3

### Streaming
- Track delivery trucks live from GPS pings. Meel Move, level 3
- The same click arrives twice (exactly-once and dedupe in streams). Meel Reach, level 3
- Flag a suspicious card payment within seconds. Meel Pay, level 4

### Orchestration and reliability
- The pipeline fails at step 4 of 6. Rerun without double-loading (idempotency). Meel Cart, level 2
- Rebuild six months of history after a bug fix (backfill). Meel Cart, level 2
- Job B runs before job A finishes (dependencies and retries). Shared, level 2

### Performance and cost
- The daily sales query takes 20 minutes (partitioning and file sizes). Meel Motors, level 3
- Millions of tiny files slow everything down (compaction). Meel Reach, level 3
- Cut the warehouse bill in half without slowing reports. Shared, level 4

### Privacy and governance
- Analysts can see loan applicants' full SSNs (masking and access rules). Meel Pay, level 2
- A customer asks to be deleted from every system. Shared, level 3
- Who changed this number and when (lineage and audit). Shared, level 3

### Serving
- Sales team wants scores inside the CRM, not a dashboard (reverse ETL). Meel Motors, level 3
- Data science needs the same features in training and live (feature tables). Meel Pay, level 4

### Healthcare (Meel Care)
- Flatten nested FHIR patient records into clean tables. Level 2
- Remove the 18 HIPAA identifiers before analysts see the data. Level 2
- Claims adjusted weeks after the visit change last month's totals. Level 3
- One patient registered three times at three clinics. Level 3

### Back office (HQ)
- Every division's revenue must match the general ledger at month-end. Level 3
- Payroll history with raises and transfers over time. Level 2
- Millions of server log lines a day, searchable by error. Level 3

### Real world data
- Pull rates, gas prices, weather and recalls daily without leaking API keys. Level 1
- FRED revises last month's number. Which version did the report use? Level 3
- Orders in 5 currencies and 4 time zones, one finance report. Meel Cart, level 2

### Platform and practices
- Real source systems: move Meel Cart orders into Postgres and pull changes with Debezium. Level 3
- Move a big batch job to PySpark with Delta Lake or Iceberg tables. Level 3
- Dev, test and prod with tests on every pull request. Level 2
- Start the whole company with one docker compose command. Level 2
- Describe the platform in Terraform, test against LocalStack and Azurite. Level 3
- Alert on failed runs and stale data. Lineage with OpenLineage. Level 2
- Make doctor notes and support tickets searchable with embeddings. Level 4

### Scenarios
Every scenario in [docs/scenarios.md](../docs/scenarios.md) can turn into a problem here.
