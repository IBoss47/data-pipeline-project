
from services.metadata.config_reader import load_config
from services.loaders.clickhouse_loader import ClickHouseLoader
from services.metadata.ddl_generator import ClickHouseDDLGenerator
import logging

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



