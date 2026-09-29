from airflow.sdk import dag, task, Asset
from services.bootstrap.init_metadata import init_metadata
from datetime import datetime

"""
 Script Purpose:
    This is the platform initialization script that executes `init_metadata()`. 
    It is designed to be triggered manually via the Airflow UI.
    
    Dag ID: init_plarform_pipeline
    Outlets: s3://streamify/init
    
 Workflows :
    init_platform (current) --> ...
"""

INIT_ASSET = Asset("s3://streamify/init")

@dag(
    dag_id = 'init_platform_pipeline',
    schedule = None,
    start_date = datetime(2026, 7, 24),
    catchup = False
)

def init_platform():
    @task(task_id = "initial_metadata", outlets = [INIT_ASSET])
    def setup():
        init_metadata()
    setup()

init_platform()