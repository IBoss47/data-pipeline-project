from datetime import datetime
from pathlib import Path
from pprint import pprint

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import dag, task, AssetAll, Asset


from services.pipeline.run_pipeline import run_pipeline

DATASET_PATH = Path("/opt/airflow/config/datasets")

assets = []
for dataset_file in DATASET_PATH.glob("*.yml"):
    dataset = dataset_file.stem
    asset = Asset(f"s3://ecom/raw/{dataset}")

    assets.append(asset)

@dag(
    dag_id="ecom_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule= AssetAll(*assets),
    catchup=False,
)

def ecom_pipeline():

    load_tasks = []

    for dataset_file in DATASET_PATH.glob("*.yml"):
        
        dataset = dataset_file.stem

        @task(task_id = f"load_{dataset}")
        def load_datasets(dataset_name: str, ds = None):

            
           
            run_pipeline(dataset = dataset_name)

        load_tasks.append(load_datasets(dataset))

    # dbt_build = BashOperator(
    #     task_id="dbt_build",
    #     bash_command="""
    #     dbt run \
    #     --project-dir /opt/dbt/ecom \
    #     --profiles-dir /opt/dbt/profiles \
    #     --target docker
    #     """,
    # )

    # dbt_test = BashOperator(
    #     task_id="dbt_test",
    #     bash_command="""
    #     dbt test \
    #     --project-dir /opt/dbt/ecom \
    #     --profiles-dir /opt/dbt/profiles \
    #     --target docker
    #     """,
    # )

    load_tasks 
    # >> dbt_build >> dbt_test

ecom_pipeline()