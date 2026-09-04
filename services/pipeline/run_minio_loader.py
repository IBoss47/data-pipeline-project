from services.metadata.config_reader import load_config
from services.extractors.csv_extractor import CSVExtractor
from services.loaders.minio_loader import MinioLoader
from services.converters.parquet_converter import ParquetConverter
import logging

logger = logging.getLogger(__name__)

def run_minio_loader(dataset, date):
    logger.info(f"Starting MinIO pipeline for dataset: {dataset} on date: {date}")
    try:
        config = load_config(dataset)
        logger.info(f"Successfully loaded config for dataset: {dataset}")

        df = CSVExtractor().extractor(config)
        logger.info(f"Successfully extracted dataset: {dataset} ({len(df)} rows) from CSV")

        MinioLoader().load_data_to_minio(date, config)
        logger.info("Successfully loaded dataset into MinIO")

        ParquetConverter().csv_to_parquet(date, config)
        logger.info("Successfully converted CSV format to Parquet format and save in MinIO")
    except Exception as e:
        logger.error(f"Pipeline failed for dataset {dataset}: {str(e)}")
        raise e



    