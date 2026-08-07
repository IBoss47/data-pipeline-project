from airflow.providers.clickhousedb.hooks.clickhouse import ClickHouseHook


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