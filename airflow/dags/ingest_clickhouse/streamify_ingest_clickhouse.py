from datetime import datetime
from pathlib import Path
from airflow.sdk import dag, task, AssetAll, Asset
from services.pipeline.run_clickhouse_loader import run_pipeline

"""
 Script Purpose:
    This script dynamically generates tasks to ingest raw datasets into ClickHouse by executing `run_pipeline()`.
    It listens to raw data assets and updates ClickHouse dataset assets upon completion.

    DAG ID: streamify_ingest_clickhouse
    Schedule: AssetAll (*raw_assets)
    Outlets: s3://streamify/clickhouse/{dataset}
 
 Workflows :
    init_platform --> streamify_ingest_minio --> streamify_ingest_clickhouse (current) --> ...

 Warnings & Edge Cases:
    - Empty Directory Edge Case: If `/opt/airflow/config/datasets` contains no `.yml` files at parse time,
      `raw_assets` will be empty (`[]`), causing the DAG schedule to fall back to `None` and resulting 
      in an empty DAG without any generated tasks.
    - Top-Level I/O Overhead: Using `DATASET_PATH.glob()` at the top level causes file system scanning 
      on every DAG parsing cycle, which may impact Airflow Scheduler performance as the project scales.
"""

DATASET_PATH = Path("/opt/airflow/config/datasets")
assets = [Asset(f"s3://streamify/raw/{f.stem}") for f in DATASET_PATH.glob('*.yml')]

@task
def load_dataset_task(dataset_name: str, **kwargs):
    run_pipeline(dataset = dataset_name)

@dag(
    dag_id="streamify_ingest_clickhouse",
    start_date=datetime(2024, 1, 1),
    schedule= AssetAll(*assets) if assets else None,
    catchup=False,
)

def load_to_clickhouse():

    for dataset_file in DATASET_PATH.glob("*.yml"):
        dataset = dataset_file.stem

        load_dataset_task.override(
            task_id = f'load_{dataset}',
            outlets = [Asset(f"s3://streamify/clickhouse/{dataset}")]
        )(dataset_name = dataset)

load_to_clickhouse()