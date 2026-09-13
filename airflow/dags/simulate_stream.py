from airflow.sdk import dag, Asset, AssetAll
from datetime import datetime
from airflow.operators.bash import BashOperator
from pathlib import Path
from airflow.dags.init_platform import DATASET_PATH


DATASET_PATH = Path("/opt/airflow/config/datasets")

assets = []
for dataset_file in DATASET_PATH.glob("*.yml"):
    dataset = dataset_file.stem
    asset = Asset(f"s3://streamify/producer/{dataset}")
    assets.append(asset)

@dag(
    dag_id = 'simulate_kafka_stream',
    schedule= AssetAll(*assets),
    start_date=datetime(2026, 7, 24),
    catchup=False
)

def simulation_stream():
    start_streaming = BashOperator(
        task_id = 'start_producer',
        bash_command = (
            "python /opt/kafka/producer/kafka_producer.py "
            "--file /opt/data/listen_events.csv "
            "--topic stream_listen_events "
            "--broker kafka:29092"
        )
    )
    start_streaming
simulation_stream()