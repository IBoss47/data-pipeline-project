from airflow.sdk import dag, AssetAll, Asset
from datetime import datetime
from pathlib import Path
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, ExecutionConfig

"""
Script Purpose:
    This script orchestrates dbt transformations by triggering dbt build via Astronomer Cosmos.
    It waits for all ClickHouse ingestion assets to be updated before running data transformation models.

    DAG ID: dbt_pipeline
    Schedule: AssetAll (*assets)
    Outlets: None (dbt updates internal ClickHouse models/views directly)

Workflows :
    init_platform --> streamify_ingest_minio --> streamify_ingest_clickhouse --> streamify_dbt_process (current)

Warnings & Edge Cases:
    - Empty Directory Edge Case: If `/opt/airflow/config/datasets` contains no `.yml` files at parse time,
      `assets` will be empty (`[]`), causing the DAG schedule to fall back to `None` and resulting in an empty DAG.
    - dbt Path Dependency: Relies on hardcoded container paths (`/opt/dbt/...`). If the Docker volume mount paths 
      or virtual environment paths change, Cosmos will fail to locate the dbt project or executable.
"""

DATASET_PATH = Path("/opt/airflow/config/datasets")
assets = [Asset(f"s3://streamify/clickhouse/{f.stem}") for f in DATASET_PATH.glob('*.yml')]

@dag(
    dag_id = 'dbt_pipeline',
    schedule= AssetAll(*assets) if assets else None,
    start_date=datetime(2026, 7, 24),
    catchup=False
)

def dbt_process_pipeline():

    profile_config = ProfileConfig(
        profile_name = 'streamify',
        target_name = 'docker',
        profiles_yml_filepath = Path('/opt/dbt/profiles/profiles.yml')
    )

    project_config = ProjectConfig(
        dbt_project_path = '/opt/dbt/streamify'
    )

    dbt_build = DbtTaskGroup(
        group_id = 'dbt_build',
        project_config = project_config,
        profile_config = profile_config,
        execution_config = ExecutionConfig(
            dbt_executable_path = 'dbt'
        )
    )

    dbt_build
dbt_process_pipeline()