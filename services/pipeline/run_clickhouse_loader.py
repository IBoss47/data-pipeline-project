
from services.metadata.config_reader import load_config
from services.loaders.clickhouse_loader import ClickHouseLoader
from services.metadata.ddl_generator import ClickHouseDDLGenerator
import logging

"""
Script Purpose:
    This service module manages the execution workflow for loading datasets into ClickHouse.
    It orchestrates reading dataset configurations, dynamically generating and executing DDL statements, 
    and performing the data load while safely managing ClickHouse database sessions.

    Entry Point Function: run_pipeline(dataset)

Workflows :
    load_config --> ClickHouseDDLGenerator (create_table_sql) --> ClickHouseLoader (execute_ddl) --> ClickHouseLoader (load)

Warnings & Edge Cases:
    - Transaction/DDL Failures: If `create_table_sql()` or DDL execution fails, downstream data loading 
      is aborted immediately, but the `finally` block ensures the database session is gracefully closed.
    - Missing Dataset Configuration: Passing an invalid or non-existent `dataset` identifier will cause 
      `load_config()` to raise an exception before any database connections are established.
"""

logger = logging.getLogger(__name__)

def run_pipeline(dataset):
    loader = ClickHouseLoader()

    try:
        config = load_config(dataset)
        logger.info(f"Successfully loaded config for dataset: {dataset}")

        ddl = ClickHouseDDLGenerator().create_table_sql(config= config)
        loader.execute_ddl(ddl)
        logger.info(f"Successfully created table for dataset: {dataset}")

        loader.load(config)
        logger.info(f"Successfully load dataset ({dataset}) in ClickHouse")

    except Exception as e:
        raise e
    finally:
        logger.info(f"Closing ClickHouse session...")
        loader.close()
        logger.info(f"Successfully closed ClickHouse session")



