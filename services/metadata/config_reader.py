from pathlib import Path
import yaml

def load_config(dataset_name : str):
    path = (
        Path('/opt/airflow/config/datasets/')
        / f'{dataset_name}.yml'
    )

    with open(path) as f:
        return yaml.safe_load(f)
