from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from io import BytesIO
from services.metadata.ddl_generator import PyArrowSchemaGenerator
from services.metadata.metadata_catalog import MetadataCatalog

import pyarrow.csv as pcsv
import pyarrow.parquet as pq


class ParquetConverter:
    
    def csv_to_parquet(
                self, 
                date, 
                config, 
                minio_conn = 'minio_conn'
            ) -> str:
            
                raw_key = f"{config['storage']['layer']}/{config['storage']['folder']}/{date}/{config['name']}.{config['storage']['format']}"
                processed_key = f"processed/{config['storage']['folder']}/{date}/{config['name']}.parquet"
                s3_hook = S3Hook(aws_conn_id = minio_conn)

                csv_obj = s3_hook.get_key(key=raw_key, bucket_name= config['storage']['bucket'])
                csv_bytes = csv_obj.get()["Body"].read()

                schema = PyArrowSchemaGenerator().generate(config = config)
                convert_options = pcsv.ConvertOptions(column_types = schema, strings_can_be_null=True)
                parse_options = pcsv.ParseOptions(escape_char='\\')
                table = pcsv.read_csv(BytesIO(csv_bytes), convert_options=convert_options, parse_options=parse_options)


                parquet_buffer = BytesIO()
                pq.write_table(table, parquet_buffer)
                parquet_buffer.seek(0)

                s3_hook.load_bytes(
                    bytes_data=parquet_buffer.getvalue(),
                    key=processed_key,
                    bucket_name=config['storage']['bucket'],
                    replace=True,
                )

                MetadataCatalog().register(
                    dataset = config['name'],
                    processed_key = processed_key
                )
                

