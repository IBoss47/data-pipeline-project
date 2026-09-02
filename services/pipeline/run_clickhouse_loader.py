
from services.metadata.config_reader import load_config
from services.extractors.csv_extractor import CSVExtractor
from services.loaders.clickhouse_loader import ClickHouseLoader
from services.loaders.minio_loader import MinioLoader
from services.metadata.ddl_generator import ClickHouseDDLGenerator


def run_pipeline(dataset):

    config = load_config(dataset)

    ddl = ClickHouseDDLGenerator().create_table_sql(config= config)

    loader = ClickHouseLoader()

    try:
        loader.execute_ddl(ddl)
        loader.load(config)
    except Exception as e:
        return e
    finally:
        loader.close()



