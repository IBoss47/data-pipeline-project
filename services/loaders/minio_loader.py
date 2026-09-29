from airflow.providers.amazon.aws.hooks.s3 import S3Hook

"""
 Script Purpose:
    This service module manages the uploading of raw source files into MinIO object storage.
    It provisions necessary target buckets and constructs partition paths based on dataset configurations.

    Class: MinioLoader
    Entry Point Method: load_data_to_minio(date, config)

 Warnings & Edge Cases:
    - File Existence Dependency: Assumes `config['source']['path']` points to a valid local file; 
      if the file is missing, `S3Hook.load_file()` will raise a `FileNotFoundError`.
    - Key Nesting & Formatting: Constructs the S3 object key dynamically based on YAML config metadata. 
      Missing keys in `config['storage']` or `config['source']` will result in a `KeyError`.
    - Overwrite Behavior (`replace=True`): Re-executing the loader for the same date partition and 
      dataset will silently overwrite existing raw files in MinIO.
"""

class MinioLoader:
    """
    Loader class for uploading raw data files into MinIO object storage.
    """

    def __init__(self, conn_id = "minio_conn"):
        """Initializes the S3 hook for MinIO connection."""
        self.hook = S3Hook(
            aws_conn_id = conn_id
        )

    def load_data_to_minio(self, date, config):
        """
        Uploads a local file to MinIO based on the provided configuration.
        Creates the target bucket if it does not already exist.
        
        Args:
            date (str): Partition date for the storage path.
            config (dict): Configuration dictionary containing source path and storage details.
        """
        # Ensure the target bucket exists
        if not self.hook.check_for_bucket(bucket_name = config['storage']['bucket']):
            self.hook.create_bucket(bucket_name = config['storage']['bucket'])

        raw_key = f"{config['storage']['layer']}/{config['storage']['folder']}/{date}/{config['name']}.{config['storage']['format']}"
        
        # Upload the local file to MinIO
        self.hook.load_file(
            filename = config['source']['path'],
            key = raw_key,
            bucket_name = config['storage']['bucket'],
            replace = True
        )
        


