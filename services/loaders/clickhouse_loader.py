from airflow.providers.clickhousedb.hooks.clickhouse import ClickHouseHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from services.metadata.metadata_catalog import MetadataCatalog
from io import BytesIO
import pyarrow.parquet as pq

class ClickHouseLoader:
    
    def __init__(self, conn_id = "clickhouse_conn"):

        self.hook = ClickHouseHook(
            clickhouse_conn_id = conn_id
        )
        self.client = self.hook.get_client()

    def execute_ddl(self, ddl):

        for query in ddl:
            self.client.command(query)

    def load(self, config): 
        
        s3_hook = S3Hook(aws_conn_id = 'minio_conn')

        processed_key = MetadataCatalog().get_processed_key(
            dataset = config['name']
        )

        parquet_obj = s3_hook.get_key(
            key = processed_key,
            bucket_name = config['storage']['bucket']
        )

        parquet_bytes = parquet_obj.get()['Body'].read()
        table = pq.read_table(BytesIO(parquet_bytes))
        columns = table.column_names
        
        rows = []
        for i in range(table.num_rows):
            row = tuple(table.column(col)[i].as_py() for col in columns)
            rows.append(row)

        database = config["target"]["database"]
        table_name = config["target"]["table"]

        self.client.query(f"truncate table {database}.{table_name}")

        self.client.insert(
            f"{database}.{table_name}",
            rows,
            column_names = columns
        )