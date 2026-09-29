import pyarrow as pa

"""
 Script Purpose:
    This utility module dynamically generates ClickHouse DDL queries and PyArrow schemas 
    based on YAML configuration definitions for raw data ingestion and pipeline conversion.

    Classes:
    - ClickHouseDDLGenerator: Constructs CREATE DATABASE and CREATE TABLE SQL statements.
    - PyArrowSchemaGenerator: Converts YAML data types to explicit PyArrow schema definitions.

 Warnings & Edge Cases:
    - Unmapped Data Types: If `column_types` in the YAML config contains a data type not present in 
      `PyArrowSchemaGenerator.TYPE_MAPPING` (e.g., Decimal, Array, or LowCardinality), 
      a `KeyError` will be raised during schema generation.
    - Missing Config Keys: Assumes required keys (`target.database`, `target.table`, `target.engine`, 
      `target.order_by`, `column_types`) exist in the configuration; missing keys will raise a `KeyError`.
    - Complex ClickHouse Types: Nested ClickHouse types or parameters (such as `DateTime64(3, 'UTC')`) 
      are not directly supported in the simple string-based `TYPE_MAPPING`.
"""

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