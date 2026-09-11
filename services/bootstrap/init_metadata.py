from services.metadata.ddl_generator import ClickHouseDDLGenerator
import logging

logger = logging.getLogger(__name__)

def init_metadata():
    logger.info("Starting to initials database metadata for project...")
    loader = ClickHouseDDLGenerator.create_kafka_streaming_sql()

    loader.create_metadata_table()
    logger.info("Successfully created metadata table...")