# Tool map

Everything here runs on free, open source tools. On a real team the same job usually runs on a managed cloud service, so every write-up says which one my tool stands in for, and what would change.

**In use** marks what the code uses today. The rest come in with the problem that needs them.

## Languages

Python, SQL, PySpark, Bash and YAML.

## The map

| Job | What I use here | In use | AWS | Azure | Snowflake / Databricks |
|---|---|---|---|---|---|
| Warehouse | DuckDB, Postgres | DuckDB | Redshift, Athena | Synapse, Microsoft Fabric | Snowflake |
| File storage, data lake | Local folders, Parquet files | Local folders | S3 | ADLS Gen2 | Snowflake stages, Unity Catalog volumes |
| Lakehouse tables | Delta Lake, Apache Iceberg | | S3 Tables, Glue with Iceberg | Fabric OneLake (Delta) | Databricks Delta, Snowflake Iceberg tables |
| Big batch processing | PySpark | | Glue, EMR | Synapse Spark, Databricks | Databricks, Snowpark |
| SQL transforms and tests | dbt Core | Yes | dbt on Redshift or Athena | dbt on Synapse or Fabric | dbt on Snowflake or Databricks |
| Scheduling and orchestration | GitHub Actions, Dagster | Not yet (runs on demand from the dashboard) | MWAA (managed Airflow), Step Functions | Data Factory pipelines | Snowflake Tasks, Databricks Jobs |
| Streaming | Redpanda (Kafka compatible) | | Kinesis, MSK | Event Hubs | Snowpipe Streaming |
| Change data capture | Debezium | | DMS | Data Factory CDC | Snowflake Streams |
| Data quality | dbt tests, Great Expectations | dbt tests | Glue Data Quality | Purview data quality | Snowflake data metric functions |
| Catalog and lineage | OpenMetadata, OpenLineage | | Glue Data Catalog | Purview | Snowflake Horizon, Unity Catalog |
| Secrets | .env files, GitHub Actions secrets | | Secrets Manager | Key Vault | Snowflake secrets |
| Infrastructure as code | OpenTofu or Terraform | | CloudFormation | Bicep | Terraform providers |
| Dashboards | Streamlit | Yes | QuickSight | Power BI | Snowsight, Streamlit in Snowflake |

## How each write-up says it

Section 6 of every problem uses the same shape, so the cloud angle is never vague:

> On the job this would run on Snowflake. Here I used DuckDB because it's free and runs on my laptop. The fix carries over as is: the same MERGE, keyed on the same column. What changes in the cloud is cost and scale, so I'd also cluster the table by order date.

Name the service, say why the stand-in, say what carries over, say what changes.
