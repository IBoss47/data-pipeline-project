from pathlib import Path
import yaml
import logging

"""
 Script Purpose:
    This utility module reads and parses YAML configuration files for specific datasets.
    It returns the parsed configuration as a Python dictionary for downstream ETL execution.

    Entry Point Function: load_config(dataset_name)

 Warnings & Edge Cases:
    - Missing Configuration File: If `dataset_name.yml` does not exist in `/opt/airflow/config/datasets/`, 
      a `FileNotFoundError` will be raised before YAML parsing occurs.
    - Invalid YAML Syntax: If the configuration file contains syntax errors, `yaml.safe_load()` 
      will raise a `ScannerError` or `ParserError`.
"""

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
