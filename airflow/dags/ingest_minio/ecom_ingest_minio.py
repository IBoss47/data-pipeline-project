from airflow.sdk import Asset, dag, task
from airflow import DAG
from datetime import datetime
from pathlib import Path
from services.pipeline.run_minio_loader import run_minio_loader

DATASET_PATH = Path("/opt/airflow/config/datasets")

@dag(
    dag_id = 'ecom_ingest_minio',
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False
)

def load_to_minio():

    load_tasks = []
    
    for dataset_file in DATASET_PATH.glob("*.yml"):
        dataset = dataset_file.stem
        asset = Asset(f"s3://ecom/raw/{dataset}")

        @task(task_id = f"load_{dataset}", outlets = [asset])
        def load_datasets(dataset_name: str, ds = None):
            run_minio_loader(dataset = dataset_name, date = ds)

        load_tasks.append(load_datasets(dataset))
    
    load_tasks

load_to_minio()


    

