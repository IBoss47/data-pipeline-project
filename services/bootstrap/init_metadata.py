from services.metadata.metadata_catalog import MetadataCatalog
import logging

logger = logging.getLogger(__name__)

def init_metadata():
    logger.info("Starting to initials database metadata for project...")
    loader = MetadataCatalog()

    loader.create_metadata_table()
    logger.info("Successfully created metadata table...")