from airflow.sdk import dag, task, Asset
from services.bootstrap.init_metadata import init_metadata
from datetime import datetime
from pathlib import Path
from services.metadata.config_reader import load_config
from services.loaders.clickhouse_loader import ClickHouseLoader
from services.metadata.ddl_generator import ClickHouseDDLGenerator

DATASET_PATH = Path("/opt/airflow/config/datasets")

@dag(
    dag_id = 'init_platform_pipeline',
    schedule = None,
    start_date = datetime(2026, 7, 24),
    catchup = False
)

def init_platform():
    for dataset_file in DATASET_PATH.glob("*.yml"):
        dataset = dataset_file.stem
        config = load_config(dataset)

        @task(task_id = "initial_metadata")
        def setup():
            generator = ClickHouseDDLGenerator()
            loader = ClickHouseLoader()

            query = generator.create_kafka_streaming_sql(config = config)
            loader.execute_ddl(query)

        setup()
init_platform()