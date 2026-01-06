# Spotify ETL Engine - Databricks Component

This directory contains the **Data Processing Core** of the Spotify Data Engineering project. It is implemented as a **Databricks Asset Bundle (DAB)** and focuses strictly on the **Silver & Gold layers**, utilizing Delta Live Tables for transformations and Spark Structured Streaming for ingestion.

> **Note:** This is the transformation module triggered by Azure Data Factory. For the full end-to-end architecture (including ADF & Bronze ingestion), please refer to the root repository README.

## 🏗 Component Scope & Architecture

This module is responsible for the **Transformation & Serving** stages of the Medallion Architecture:

### 1. Ingestion & Silver Layer (Streaming Logic)
* **Ingestion:** Uses **Auto Loader** (`cloudFiles`) to ingest raw data from the Bronze container (ADLS Gen2).
* **Processing Pattern:** Implements **Incremental Batch Processing**. The code uses Spark Structured Streaming logic but is executed with `.trigger(once=True)` to process micro-batches cost-effectively on Serverless Compute.
* **Key Tasks:** Schema enforcement, deduplication, and data quality checks (handling `_rescued_data`).

### 2. Gold Layer (Delta Live Tables & CDC)
* **Dimensional Modeling:** Builds a Star Schema optimized for analytics (`FactStream`, `DimDate`, `DimTrack`, `DimUser`).
* **SCD Type 2 Implementation:** Leverages `dlt.create_auto_cdc_flow` with `APPLY CHANGES INTO` logic to track historical changes (e.g., preserving user profile history over time).
* **Isolation:** Separates staging tables from final published tables within the Unity Catalog.

### 3. Dynamic SQL & Templating
* **Jinja2 Framework:** Utilizes Jinja templating to generate complex SQL queries dynamically from Python configurations, ensuring DRY (Don't Repeat Yourself) code principles.

---

## 📂 Internal Structure

```bash
spotify_dab/
├── databricks.yml              # Bundle configuration (DABs) & variable definitions
├── resources/                  # IaC: Workflow Jobs and DLT Pipeline definitions
├── src/
│   ├── silver/                 # PySpark Notebooks (Auto Loader logic)
│   └── gold/dlt/               # DLT Python Modules (SCD Type 2 & Dimensions)
├── Jinja/                      # SQL Templates for dynamic view generation
└── requirements.txt            # Python library dependencies
```




## 🚀 Deployment & CI/CD

This project is fully managed via **Databricks Asset Bundles (DABs)**.

### Configuration (databricks.yml)
- Defines distinct targets for **Dev** (personal schema) and **Prod** (production catalog)
- Uses variables to parameterize catalog and schema names dynamically

### Deployment Commands

```bash
# Validate bundle configuration
databricks bundle validate

# Deploy to Development environment
databricks bundle deploy -t dev

# Run the pipeline manually
databricks bundle run -t dev
```

## 🛠 Tech Stack

- **Compute:** Delta Live Tables, Spark Structured Streaming  
- **Storage / Format:** Delta Lake  
- **Orchestration:** Databricks Workflows  
- **Languages:** Python (PySpark), SQL, Jinja2  
- **DevOps & Tooling:** Databricks CLI, Git

