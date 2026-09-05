from datetime import datetime
from pathlib import Path
from airflow.sdk import dag, task, AssetAll, Asset


from services.pipeline.run_clickhouse_loader import run_pipeline

DATASET_PATH = Path("/opt/airflow/config/datasets")

assets = []
for dataset_file in DATASET_PATH.glob("*.yml"):
    dataset = dataset_file.stem
    asset = Asset(f"s3://streamify/raw/{dataset}")

    assets.append(asset)

@dag(
    dag_id="streamify_ingest_clickhouse",
    start_date=datetime(2024, 1, 1),
    schedule= AssetAll(*assets),
    catchup=False,
)

def load_to_clickhouse():

    load_tasks = []

    for dataset_file in DATASET_PATH.glob("*.yml"):

        dataset = dataset_file.stem
        asset = Asset(f"s3://streamify/clickhouse/{dataset}")

        @task(task_id = f"load_{dataset}", outlets=[asset])
        def load_datasets(dataset_name: str, ds = None):

            run_pipeline(dataset = dataset_name)

        load_tasks.append(load_datasets(dataset))

    load_tasks

load_to_clickhouse()