from airflow.sdk import dag, task, AssetAll, Asset
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime

@dag(
    dag_id = 'dbt_pipeline',
    schedule= None,
    start_date=datetime(2026, 7, 24),
    catchup=False
)

def dbt_process_pipeline():

    dbt_build = BashOperator(
            task_id="dbt_build",
            bash_command="""
            dbt build \
            --project-dir /opt/dbt/streamify \
            --profiles-dir /opt/dbt/profiles \
            --target docker
            """,
        )

    dbt_build
dbt_process_pipeline()