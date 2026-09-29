from airflow.providers.clickhousedb.hooks.clickhouse import ClickHouseHook

"""
 Script Purpose:
    This service module manages execution state and file processing metadata in ClickHouse.
    It provisions the `metadata.file_catalog` table to track processed keys/watermarks, 
    enabling downstream DAGs to execute incremental data loading and prevent duplicate processing.

    Class: MetadataCatalog
    Key Methods:
    - create_metadata_table(): Initializes the 'metadata' database and 'file_catalog' table.
    - register(dataset, processed_key): Records newly processed file keys with automated timestamps.
    - get_processed_key(dataset): Retrieves the latest processed key for incremental query boundaries.

 Warnings & Edge Cases:
    - Empty Table Query Error: Calling `get_processed_key()` before registering any file key 
      for a dataset will trigger an `IndexError` when attempting to access `result.result_rows[0][0]`.
    - SQL Injection Risk: Formatting SQL queries using f-strings in `get_processed_key()` can expose 
      the system to SQL injection if input dataset parameters are not sanitized upstream.
    - Connection Lifecycle: The class initializes a ClickHouse client directly on instantiation (`__init__`); 
      ensure connections are properly closed or managed to avoid connection leakages in worker tasks.
"""

class MetadataCatalog:

    def __init__(self):
        hook = ClickHouseHook(clickhouse_conn_id="clickhouse_conn")
        self.client = hook.get_client()

    def create_metadata_table(self):

        self.client.command("""
        CREATE DATABASE IF NOT EXISTS metadata
        """)

        self.client.command("""

        CREATE TABLE IF NOT EXISTS metadata.file_catalog
        (
            dataset String,
            processed_key String,
            created_at DateTime DEFAULT now()
        )
        ENGINE = MergeTree
        ORDER BY (dataset, created_at)
        """)

    def register(self, dataset, processed_key):

        self.client.insert(
            "metadata.file_catalog",
            [[dataset, processed_key]],
            column_names=[
                "dataset",
                "processed_key",
            ],
        )

    def get_processed_key(self, dataset):

        result = self.client.query(f"""
            SELECT processed_key
            FROM metadata.file_catalog
            WHERE dataset = '{dataset}'
            ORDER BY created_at DESC
            LIMIT 1
        """)

        return result.result_rows[0][0]