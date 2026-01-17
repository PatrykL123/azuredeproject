# Spotify End-to-End Data Engineering Project
[![Azure](https://img.shields.io/badge/Azure-Microsoft-blue?logo=azure)](https://azure.microsoft.com/) [![Databricks](https://img.shields.io/badge/Databricks-Workflows-orange?logo=databricks)](https://databricks.com/) [![Spark](https://img.shields.io/badge/Spark-Apache-orange?logo=apache-spark)](https://spark.apache.org/)

This repository contains an end-to-end data engineering solution that extracts transactional data from an Azure SQL source, ingests it via an ADF-driven, metadata-configurable engine into ADLS Gen2 (bronze), and implements transformation and serving layers on Databricks (silver → gold) using Databricks Asset Bundles and Delta Live Tables.

## Architecture (high-level)
```mermaid
graph LR
  A["Azure SQL Database"] --> B["Azure Data Factory<br/>(metadata loop & cdc.json state)"]
  B --> C["ADLS Gen2 (Bronze)"]
  C --> D["Databricks — Silver processing<br/>(Auto Loader / Structured Streaming)"]
  D --> E["Databricks — Gold (DLT & SCD Type 2)"]
```

## Navigation
A short map to the main modules in this repository:

| Module | Purpose |
|---|---|
| ADF Ingestion Engine | [./adf/README.md](./adf/README.md) |
| Databricks Processing Core | [./spotify_dab/README.md](./spotify_dab/README.md) |

(Each module README contains implementation and operational details.)

## Key features
- Metadata-Driven Ingestion — ingestion behavior is controlled by metadata/config rather than hard-coded pipelines, enabling scalable table-by-table processing.
- File-Based State Management (Serverless) — pipeline watermarking and checkpoints are managed in lightweight JSON state files (cdc.json), suitable for serverless and repeatable runs.
- Databricks Asset Bundles & Delta Live Tables — transformations and SCD logic are packaged and deployed as Databricks Asset Bundles; Gold layer leverages DLT for continuous CDC and SCD Type 2 patterns.

## Tech stack (summary)

| Layer | Technology |
|---|---|
| Source | Azure SQL Database |
| Orchestration / Ingestion | Azure Data Factory (metadata loops) |
| Storage | Azure Data Lake Storage Gen2 (Bronze / Silver / Gold via Delta) |
| Compute / Transform | Databricks — Apache Spark, Delta Lake, Delta Live Tables (DLT) |
| Packaging / Deployment | Databricks Asset Bundles (DAB) |
| State / Watermarking | File-based (cdc.json) stored in ADLS |

