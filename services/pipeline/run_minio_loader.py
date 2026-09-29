from services.metadata.config_reader import load_config
from services.extractors.csv_extractor import CSVExtractor
from services.loaders.minio_loader import MinioLoader
from services.converters.parquet_converter import ParquetConverter
import logging

"""
Script Purpose:
    This service module orchestrates the ETL pipeline to extract raw CSV data, 
    upload it to MinIO landing storage, and convert it into Parquet format.

    Entry Point Function: run_minio_loader(dataset, date)

Workflows :
    load_config --> CSVExtractor (extractor) --> MinioLoader (load_data_to_minio) --> ParquetConverter (csv_to_parquet)

Warnings & Edge Cases:
    - High Memory Usage (In-Memory Processing): Extracting the entire CSV into a pandas Dataframe
      in memory (`CSVExtractor`) can cause Out-Of-Memory (OOM) errors on large datasets.
    - Idempotency & Overwrite Risk: Executing the pipeline multiple times for the same dataset and 
      date partition will overwrite existing raw CSV and Parquet files in MinIO.
"""

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



    