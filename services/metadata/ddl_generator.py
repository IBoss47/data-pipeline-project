import pyarrow as pa

class ClickHouseDDLGenerator:

    def create_table_sql(self, config):

        database = config['target']['database']
        table = config['target']['table']

        columns = []
        nullable = config.get("nullable", {}) or {}

        for column, dtype in config["column_types"].items():

            if nullable.get(column, False):
                dtype = f"Nullable({dtype})"

            columns.append(f"{column} {dtype}")
        
        columns_sql = ",\n".join(columns)
        order_by = ", ".join(config['target']['order_by'])
        engine = config['target']['engine']

        query = [
            f"create database if not exists {database}",

            f"""create table if not exists {database}.{table}(
                {columns_sql}
            )
            engine = {engine}
            order by ({order_by})
            """
        ]

        return query


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