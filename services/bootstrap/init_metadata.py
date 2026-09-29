
from services.metadata.metadata_catalog import MetadataCatalog
import logging

"""
Script Purpose:
    This service module initializes the core platform infrastructure by creating the metadata 
    database and necessary catalog tables in ClickHouse.

    Entry Point Function: init_metadata()

Warnings & Edge Cases:
    - Initial Connection Failure: Relies on `MetadataCatalog` establishing a connection upon 
      instantiation; if ClickHouse is unreachable, initialization will fail immediately.
    - Non-Transactional DDL: DDL commands executed via ClickHouse are not transactional. 
      If table creation fails midway, previously created databases/objects will remain intact.
"""

logger = logging.getLogger(__name__)

def init_metadata():
    """
    Initializes the metadata catalog by creating the necessary tables
    in the target database.
    """
    logger.info("Starting to initials database metadata for project...")
    loader = MetadataCatalog()

    loader.create_metadata_table()
    logger.info("Successfully created metadata table...")