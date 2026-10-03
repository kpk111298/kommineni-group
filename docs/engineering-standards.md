# Engineering standards

How the Kommineni Group data team works. Everything here is free.

## Environments
- `dev`, `test` and `prod` are separate databases and separate schedules.
- Nothing changes prod directly. Every change goes through a pull request.

## CI
- GitHub Actions runs Python tests and `dbt build` on every pull request.
- A pull request can't merge if tests fail.

## Local setup
- One `docker compose up` starts Postgres, the source systems, the pipelines and the dashboards.

## Infrastructure as code
- Terraform describes the platform.
- LocalStack (community edition) stands in for AWS services and Azurite for Azure Storage, so cloud-style setups run on a laptop with no bill.

## Big data and lakehouse
- PySpark for large batch jobs.
- Delta Lake or Apache Iceberg tables for the lakehouse layer.

## Data quality and contracts
- dbt tests on every model. Freshness checks on every source.
- Each source system publishes a data contract: column names, types and rules. A breaking change needs a version bump.

## Monitoring
- Failed runs and stale data post an alert to a Discord or Slack channel.
- Lineage with OpenLineage and Marquez.

## Work tracking
- Business requests come in as GitHub Issues, written the way a manager would write them.
- A GitHub Projects board acts as the team's Jira. Work runs in two-week sprints.

## Incidents
- Every serious break gets a runbook entry and a short blameless postmortem in `docs/incidents/`.

## Secrets
- API keys live in `.env` locally and GitHub Actions secrets in CI. Never committed.

## AI data
- Embeddings for doctor notes and support tickets with a local model (Ollama) and pgvector, so the text becomes searchable.
