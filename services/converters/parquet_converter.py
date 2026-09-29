from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from io import BytesIO
from services.metadata.ddl_generator import PyArrowSchemaGenerator
from services.metadata.metadata_catalog import MetadataCatalog

import pyarrow.csv as pcsv
import pyarrow.parquet as pq

"""
Script Purpose:
    This service module converts raw CSV files stored in MinIO into optimized Parquet format in-memory.
    It applies PyArrow schemas generated from YAML configs, uploads the Parquet binary back to the MinIO 
    processed layer, and registers the newly created file key into the MetadataCatalog.

    Class: ParquetConverter
    Entry Point Method: csv_to_parquet(date, config, minio_conn='minio_conn')

Warnings & Edge Cases:
    - High Memory Usage (In-Memory Processing): Reading the full CSV payload into `csv_bytes` and writing 
      to an in-memory `BytesIO` Parquet buffer can trigger High Memory Overhead or OOM crashes on large files.
    - Missing Raw Object Key: If `raw_key` does not exist in the MinIO bucket, `s3_hook.get_key()` will 
      fail or return `None`, raising an `AttributeError` when accessing `.get()`.
    - PyArrow Schema Mismatch: If raw CSV field data violates data type constraints defined in `PyArrowSchemaGenerator`, 
      `pcsv.read_csv()` will throw a `ArrowInvalid` parsing exception.
"""

class ParquetConverter:
    """
    Converter class for transforming CSV files in MinIO to Parquet format.
    """
    
    def csv_to_parquet(
                self, 
                date, 
                config, 
                minio_conn = 'minio_conn'
            ) -> str:
                """
                Downloads a raw CSV from MinIO, applies the corresponding PyArrow schema, 
                converts it to Parquet in-memory, uploads the Parquet file back to MinIO,
                and registers the processed metadata.
                
                Args:
                    date (str): The partition date string.
                    config (dict): Configuration dictionary for the dataset.
                    minio_conn (str): Airflow connection ID for MinIO. Defaults to 'minio_conn'.
                    
                Returns:
                    str: The processed key of the uploaded Parquet file (implied, though currently returns None).
                """
                raw_key = f"{config['storage']['layer']}/{config['storage']['folder']}/{date}/{config['name']}.{config['storage']['format']}"
                processed_key = f"processed/{config['storage']['folder']}/{date}/{config['name']}.parquet"
                s3_hook = S3Hook(aws_conn_id = minio_conn)

                # Fetch raw CSV file from MinIO
                csv_obj = s3_hook.get_key(key=raw_key, bucket_name= config['storage']['bucket'])
                csv_bytes = csv_obj.get()["Body"].read()

                # Generate PyArrow schema based on config and set read options
                schema = PyArrowSchemaGenerator().generate(config = config)
                convert_options = pcsv.ConvertOptions(column_types = schema, strings_can_be_null=True)
                parse_options = pcsv.ParseOptions(escape_char='\\')
                
                # Parse CSV bytes into a PyArrow table
                table = pcsv.read_csv(BytesIO(csv_bytes), convert_options=convert_options, parse_options=parse_options)


                # Write the PyArrow table to an in-memory Parquet buffer
                parquet_buffer = BytesIO()
                pq.write_table(table, parquet_buffer)
                parquet_buffer.seek(0)

                # Upload the Parquet buffer to MinIO's processed layer
                s3_hook.load_bytes(
                    bytes_data=parquet_buffer.getvalue(),
                    key=processed_key,
                    bucket_name=config['storage']['bucket'],
                    replace=True,
                )

                # Register the successful processing in the metadata catalog
                MetadataCatalog().register(
                    dataset = config['name'],
                    processed_key = processed_key
                )
                

