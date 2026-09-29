from airflow.providers.clickhousedb.hooks.clickhouse import ClickHouseHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from services.metadata.metadata_catalog import MetadataCatalog

"""
 Script Purpose:
    This service module handles executing DDL statements and inserting Parquet data into ClickHouse.
    It fetches MinIO credentials and S3 object keys dynamically via `MetadataCatalog`, then performs 
    a full load into ClickHouse using the native `s3()` table function.

    Class: ClickHouseLoader
    Key Methods:
    - execute_ddl(ddl): Executes database setup and DDL queries.
    - load(config): Truncates the target table and loads Parquet data from MinIO into ClickHouse.
    - close(): Gracefully closes the ClickHouse client session.

 Warnings & Edge Cases:
    - Non-Idempotent Full Refresh: Executing `load()` automatically truncates the target table 
      (`TRUNCATE TABLE`) before loading. Historical data in ClickHouse will be lost if not partitioned or appended.
    - Plaintext Credential Exposure in Logs: Injecting `access_key` and `secret_key` directly into the 
      `s3()` SQL query string can expose sensitive credentials in Airflow task log output or ClickHouse query logs.
    - Missing Metadata Catalog Key: If `MetadataCatalog().get_processed_key()` returns no result or fails, 
      constructing the `s3_url` will fail or raise an `IndexError`.
"""

class ClickHouseLoader:
    """
    Loader class responsible for loading Parquet data from MinIO into ClickHouse.
    """
    
    def __init__(self, conn_id = "clickhouse_conn"):
        """Initializes the ClickHouse connection."""
        self.hook = ClickHouseHook(
            clickhouse_conn_id = conn_id
        )
        self.client = self.hook.get_client()

    def execute_ddl(self, ddl):
        """Executes a list of DDL queries on the ClickHouse database."""
        for query in ddl:
            self.client.command(query)

    def load(self, config): 
        """
        Loads data from MinIO into the target ClickHouse table.
        Truncates the target table before performing the insert.
        """
        s3_hook = S3Hook(aws_conn_id = 'minio_conn')

        # Retrieve MinIO credentials to construct the S3 function URL
        credentials = s3_hook.get_credentials()
        client = s3_hook.get_conn()
        endpoint_url = client.meta.endpoint_url

        # Get the processed Parquet file key from the metadata catalog
        processed_key = MetadataCatalog().get_processed_key(
            dataset = config['name']
        )
        bucket = config['storage']['bucket']

        s3_url = f"{endpoint_url}/{bucket}/{processed_key}"

        database = config["target"]["database"]
        table_name = config["target"]["table"]

        # Truncate existing data (Full Load)
        self.client.command(f"truncate table {database}.{table_name}")

        # Construct and execute the insert query using ClickHouse's s3() table function
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
        """Closes the ClickHouse client connection safely."""
        if hasattr(self.client, 'disconnect'):
            self.client.disconnect()
        elif hasattr(self.client, 'close'):
            self.client.close()