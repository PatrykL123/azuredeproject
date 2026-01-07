# 🏭 Azure Data Factory - Metadata-Driven Ingestion Framework

This module implements a dynamic, **metadata-driven ingestion engine** responsible for extracting data from the transactional system (Azure SQL Database) and loading it into the Lakehouse (Bronze Layer).

It is designed to be scalable and operationally robust, featuring **automated incremental loading** and **manual backfilling capabilities**.

## 🚀 Key Features

* **Metadata-Driven Execution**: The pipeline reads a JSON configuration file (`loop_input`) to dynamically determine which tables to process.
* **Incremental Loading (CDC-like)**: Implements a "High Watermark" strategy using `LastModifiedDate` or Timestamp columns (`cdc_col`) to fetch only new records.
* **On-Demand Backfilling**: Uses the `from_date` parameter to manually override the incremental logic, allowing for historical data reloading without resetting database watermarks.
* **Batch Orchestration**: Triggers the downstream Databricks processing job only after all tables have been successfully ingested.

## ⚙️ Architecture & Logic

### 1. Configuration (`loop_input`)
The process is controlled by a JSON array defining the extraction scope.

**Example Config:**
```json
[
  {
    "schema": "dbo",
    "table": "FactStream",
    "cdc_col": "stream_timestamp",
    "from_date": "2024-01-01" 
  },
  {
    "schema": "dbo",
    "table": "DimUser",
    "cdc_col": "updated_at",
    "from_date": ""
  }
]
```

## Configuration Parameters

- **cdc_col**: The column used for tracking changes (Watermark).

### from_date (Backfill Feature)

- **Empty (`""`)**  
  The pipeline runs in **Incremental Mode** (fetches data newer than the last successful load).

- **Set (e.g., `"2024-01-01"`)**  
  The pipeline runs in **Backfill Mode**, forcing extraction starting from the specified date and **ignoring the stored watermark**.

---

## Main Pipeline (`incremental_loop`)

The workflow follows these steps:

1. **Get Metadata**  
   Reads the list of tables from the configuration file.

2. **Iterate (ForEach Loop)**  
   Processes each table in parallel or sequentially.

3. **Determine Range**  
   - If `from_date` is provided, a query is built starting from that date.  
   - If `from_date` is not provided, the pipeline retrieves the last watermark from the control json file.

4. **Copy Data**  
   Queries Azure SQL and saves raw data to **ADLS Gen2** in **Parquet** format.

5. **Update Watermark**  
   Updates the control table with the new maximum timestamp  
   *(only when running in standard incremental mode)*.

6. **Trigger Transformation**  
   After the loop completes, the `Trigger_Silver_Gold` activity invokes the **Databricks Asset Bundle** job.

---


