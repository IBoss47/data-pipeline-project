from services.metadata.config_reader import load_config
from services.extractors.csv_extractor import CSVExtractor
from services.loaders.minio_loader import MinioLoader
from services.converters.parquet_converter import ParquetConverter

def run_minio_loader(dataset, date):

    config = load_config(dataset)

    df = CSVExtractor().extractor(config)

    MinioLoader().load_data_to_minio(date, config)

    ParquetConverter().csv_to_parquet(date, config)

    