from pathlib import Path
import yaml
import logging

logger = logging.getLogger(__name__)

def load_config(dataset_name : str):
    path = (
        Path('/opt/airflow/config/datasets/')
        / f'{dataset_name}.yml'
    )

    with open(path) as f:
        try:
            return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to load config")
            raise e
