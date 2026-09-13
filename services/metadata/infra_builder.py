import pyarrow as pa

class ClickHouseDDLGenerator:

    def create_kafka_streaming_sql(self, config, kafka_broker='kafka:29092', kafka_topic='stream_listen_events', kafka_group='clickhouse_consumer'):
        database = config['target']['database']
        table = config['target']['table']
        order_by = ", ".join(config['target']['order_by'])

        columns = []
        nullable = config.get("nullable", {}) or {}

        for column, dtype in config["column_types"].items():
            # For Kafka streaming with our Python ISO8601 formatting, we need DateTime64(3)
            if dtype == "DateTime":
                dtype = "DateTime64(3)"
                
            if nullable.get(column, False):
                dtype = f"Nullable({dtype})"

            columns.append(f"{column} {dtype}")
        
        columns_sql = ",\n                ".join(columns)

        queries = [
            # 1. Create the database
            f"create database if not exists {database}",
            
            # 2. Create the Storage Table (MergeTree)
            f"""create table if not exists {database}.{table}(
                {columns_sql}
            )
            engine = MergeTree()
            order by ({order_by})
            """,
            
            # 3. Create the Kafka Engine Table
            f"""create table if not exists {database}.kafka_{table}_queue(
                {columns_sql}
            )
            engine = Kafka()
            settings
                kafka_broker_list = '{kafka_broker}',
                kafka_topic_list = '{kafka_topic}',
                kafka_group_name = '{kafka_group}',
                kafka_format = 'JSONEachRow'
            """,
            
            # 4. Create the Materialized View
            f"""create materialized view if not exists {database}.mv_{table}
            to {database}.{table} as
            select * from {database}.kafka_{table}_queue
            """
        ]

        return queries


class PyArrowSchemaGenerator:

    TYPE_MAPPING = {
        "UInt32": pa.uint32(),
        "UInt64": pa.uint64(),
        "Int32": pa.int32(),
        "Int64": pa.int64(),
        "Float32": pa.float32(),
        "Float64": pa.float64(),
        "String": pa.string(),
        "Date": pa.date32(),
        "DateTime": pa.timestamp("ms", tz="UTC"),
        "Boolean": pa.bool_(),
        "Bool": pa.bool_()
    }

    def generate(self, config):

        fields = []

        nullable = config.get("nullable") or {}

        for column, dtype in config["column_types"].items():

            arrow_type = self.TYPE_MAPPING[dtype]

            fields.append(
                pa.field(
                    column,
                    arrow_type,
                    nullable=nullable.get(column, False)
                )
            )

        return pa.schema(fields)