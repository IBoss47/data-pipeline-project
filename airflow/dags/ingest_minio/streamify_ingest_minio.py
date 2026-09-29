from airflow.sdk import Asset, dag, task
from datetime import datetime
from pathlib import Path
from services.pipeline.run_minio_loader import run_minio_loader

"""
 Script Purpose:
    This script dynamically generates tasks to ingest raw music data into MinIO storage by executing `run_minio_loader()`.
    It is triggered by the platform initialization asset signal (`s3://streamify/init`) and produces raw dataset assets.

    DAG ID: streamify_ingest_minio
    Schedule: [Asset("s3://streamify/init")]
    Outlets: s3://streamify/raw/{dataset}

 Workflows :
    init_platform --> streamify_ingest_minio (current) --> ...

 Warnings & Edge Cases:
    - Empty Directory Edge Case: If `/opt/airflow/config/datasets` contains no `.yml` files at parse time,
      the DAG will render empty without creating any task instances.
    - Top-Level I/O Overhead: Scanning the file system (`DATASET_PATH.glob()`) at the top level occurs on every 
      DAG parsing cycle, which can introduce minor execution overhead in large-scale deployments.
      
"""

DATASET_PATH = Path("/opt/airflow/config/datasets")
asset = Asset(f"s3://streamify/init")

@task
def load_dataset_task(dataset_name: str, ds = None,  **kwargs):
    run_minio_loader(dataset=dataset_name, date=ds)

@dag(
    dag_id = 'streamify_ingest_minio',
    start_date=datetime(2024, 1, 1),
    schedule=[asset],
    catchup=False
)

def load_to_minio():
    
    for dataset_file in DATASET_PATH.glob("*.yml"):
        dataset = dataset_file.stem

        load_dataset_task.override(
            task_id = f'load_raw_{dataset}_to_minio',
            outlets = [Asset(f"s3://streamify/raw/{dataset}")]
        )(dataset_name = dataset)

load_to_minio()


    

