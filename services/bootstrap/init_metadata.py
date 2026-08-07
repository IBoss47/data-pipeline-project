from services.metadata.metadata_catalog import MetadataCatalog

def init_metadata():
    loader = MetadataCatalog()
    loader.create_metadata_table()