<div align="right">
  🌐 <strong><a href="README.md">🇬🇧 English</a></strong> | <strong><a href="README_th.md">🇹🇭 ภาษาไทย</a></strong>
</div>

# Streamify Data Pipeline Project

This project is a Data Pipeline designed for analyzing music streaming behavior from a simulated platform (Streamify). It leverages the **Modern Data Stack**, including `dbt`, `ClickHouse`, and `Airflow`, to handle Data Modeling and Pipeline orchestration.

> **Note:** 
> * The structure of this Project was cloned from a Github Repo I previously created, and then adapted and enhanced from its original version.
> * The data used in this Project is from **[Streamify](https://github.com/ankurchavda/streamify)**, which simulates and extracts mock data for a specific point in time and is stored in `data/`.

## Project Setup

For instructions on how to set up and run this project locally, please refer to the **[Project Setup Guide](setup-project.md)**.

## System Architecture

![System Architecture](images/stack.png)

## Pipeline Workflow

```mermaid
flowchart LR
    Airflow[Airflow DAGs] --> Services[Python Services]
    
    subgraph dbt [dbt Transformation]
        direction LR
        STG[Staging] --> INT[Intermediate]
        INT --> CORE[Fact & Dim]
        CORE --> MARTS[Marts]
    end
    
    Services --> STG

    style Airflow fill:#e8f4f8,stroke:#017cee,stroke-width:2px,color:#000
    style Services fill:#f0f5f9,stroke:#306998,stroke-width:2px,color:#000
    style dbt fill:#fff0ed,stroke:#ff694b,stroke-width:2px,color:#000
```
---

## Project Structure

### 1. `data/` (Raw Data)
Folder for storing raw data files generated from the simulator.
- **Note:** Large data files will not be pushed to Git (configured in `.gitignore`).
- Only the `_sample.csv` files, limited to **200 rows**, are included for basic system testing.

### 2. `services/` (Python Data Ingestion)
Python scripts for importing and processing files before loading them into the Data Warehouse.
- **`extractors/csv_extractor.py`**: Helps in reading CSV files.
- **`converters/parquet_converter.py`**: Converts files from Raw CSV to Parquet Format.
- **`metadata/ddl_generator.py`**: Helper script to extract data structure (Schema) into DDL commands for creating tables in ClickHouse.

### 3. `dbt/streamify/` (Data Transformation)
This layer is divided into 3 main sub-layers:

- **`models/staging/`** *(Cleansing Layer)*
  - **Files:** `stg_streamify__listen_events`, `stg_streamify__auth_events`, `stg_streamify__page_view_events`

- **`models/intermediate/`** *(OBT)*
  - **Files:** `int_streamify__listen_events`

- **`models/core/`** *(Star Schema)*
  - **Role:** Breaks down tables from Intermediate into **Dimensions** to describe data attributes, and **Facts** to store transactional metrics.
  - **Key Files:** 
    - `fct_streamify__listen_events` *(Listening Fact table)*
    - `dim_streamify__users`, `dim_streamify__contents`, `dim_streamify__date` *(Various Dimension tables)*

### 4. `airflow/` (Data Orchestration)
Folder for managing Workflows and Scheduling the Data Pipeline.
- **`dags/`**: Folder for storing DAG (Directed Acyclic Graph) files, which define the execution order of the pipeline steps (e.g., triggering Python scripts for data ingestion, followed by executing `dbt run`).
- **`config/datasets/`**: Stores configuration and metadata files related to datasets, allowing Airflow to systematically reference and manage data.

---

## Business Scenario Simulation

Since this project was created to practice building a Data Pipeline and developing skills as a Data Engineer, I wanted to reflect the reality that Data Engineers must communicate and collaborate with various stakeholders, such as Data Owners, Business Analysts (BAs), Data Scientists, and Executives.

Therefore, to simulate a realistic working environment, I prompted AI to assume different roles involved in a data project:
- **Data Source Owner**
- **Business Analyst (BA)**
- **CEO**

You can view the Business Questions derived from this simulation here: <strong><a href="dbt/streamify/models/bussiness_question.md">Business Questions</a></strong>

___

## Project Summary & Reflection

![Dashboard](images/dashboard.png)
**Dashboard public link:** [Streamify Dashboard](https://datastudio.google.com/reporting/107e96a5-47d7-406b-bc8d-01d3cba74cc9)

### What did you learn from this project?
- Learned how to handle and process data effectively.
- Learned that if we need to create a dimension but the source data lacks a primary key, we can generate a surrogate key using hashing.
- Understood the connections and purposes of different Data Modeling layers and how they align with each other.
- From the project structure I created, I learned the importance of clear separation of concerns. For example, separating the `airflow`, `dbt`, and `services` folders, and utilizing Airflow as a fully-fledged orchestrator.
- Gained foundational knowledge of managing metadata.
- Learned more about storing data in MinIO.
- Gained practical experience with SQL, such as using CTEs, Aggregate functions, and subqueries, beyond just watching tutorials.
- Learned how to write Generic tests and Singular tests in dbt.

### How would you improve it?
- Integrate Kafka for data streaming, similar to what the original **[Streamify](https://github.com/ankurchavda/streamify)** project did.
- Incorporate PySpark as an additional processing layer before loading data into dbt.
- Explore and implement dbt snapshots and incremental tables.

### If you had to do it all over again, what would you do differently?
- Experiment with more diverse datasets, rather than just simulating music streaming data.
- Change the business context to introduce more variety and complexity into the queries.
