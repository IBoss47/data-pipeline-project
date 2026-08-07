from airflow.sdk import dag, task
from services.bootstrap.init_metadata import init_metadata
from datetime import datetime

@dag(
    dag_id = 'init_platform_pipeline',
    schedule = None,
    start_date = datetime(2026, 7, 24),
    catchup = False
)

def init_platform():

    @task
    def setup():
        init_metadata()
    setup()

init_platform()