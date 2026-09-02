from airflow.providers.clickhousedb.hooks.clickhouse import ClickHouseHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from services.metadata.metadata_catalog import MetadataCatalog

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

        credentials = s3_hook.get_credentials()
        client = s3_hook.get_conn()
        endpoint_url = client.meta.endpoint_url

        processed_key = MetadataCatalog().get_processed_key(
            dataset = config['name']
        )
        bucket = config['storage']['bucket']

        s3_url = f"{endpoint_url}/{bucket}/{processed_key}"

        database = config["target"]["database"]
        table_name = config["target"]["table"]

        self.client.command(f"truncate table {database}.{table_name}")

        insert_query = f"""
            insert into {database}.{table_name}
            select * from s3(
                '{s3_url}',
                '{credentials.access_key}',
                '{credentials.secret_key}',
                'Parquet'
            )
        """
        self.client.command(insert_query)

    def close(self):
        if hasattr(self.client, 'disconnect'):
            self.client.disconnect()
        elif hasattr(self.client, 'close'):
            self.client.close()