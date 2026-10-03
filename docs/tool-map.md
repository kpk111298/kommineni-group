# Tool map: local, AWS, Azure

Every problem is solved locally first. This table shows the managed service each cloud offers for the same job.

| Job | Local (free) | AWS | Azure |
|---|---|---|---|
| File storage, data lake | Local folders, MinIO | S3 | ADLS Gen2, Blob Storage |
| Warehouse | DuckDB, Postgres | Redshift, Athena | Synapse Analytics, Microsoft Fabric |
| Batch processing | Python, DuckDB, Spark local | Glue, EMR | Data Factory data flows, Databricks |
| SQL transforms | dbt | dbt on Redshift or Athena | dbt on Synapse or Fabric |
| Orchestration | Dagster, Airflow | MWAA (managed Airflow), Step Functions | Data Factory pipelines |
| Streaming | Redpanda, Kafka | Kinesis, MSK | Event Hubs |
| Change data capture | Debezium | DMS | Data Factory CDC |
| Data catalog, governance | dbt docs, OpenMetadata | Glue Data Catalog, Lake Formation | Microsoft Purview |
| Secrets | .env files, never committed | Secrets Manager | Key Vault |
| Dashboards | Streamlit | QuickSight | Power BI |
| Scheduling small jobs | GitHub Actions | EventBridge Scheduler, Lambda | Azure Functions timer trigger |

Snowflake and Databricks run on both clouds, so they work the same either way.
