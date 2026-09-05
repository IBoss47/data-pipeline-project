from airflow.sdk import dag, AssetAll, Asset
from datetime import datetime
from pathlib import Path
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, ExecutionConfig

DATASET_PATH = Path("/opt/airflow/config/datasets")

assets = []
for dataset_file in DATASET_PATH.glob("*.yml"):
    dataset = dataset_file.stem
    asset = Asset(f"s3://streamify/clickhouse/{dataset}")

    assets.append(asset)

@dag(
    dag_id = 'dbt_pipeline',
    schedule= AssetAll(*assets),
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