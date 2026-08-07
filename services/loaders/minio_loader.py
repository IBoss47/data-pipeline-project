from airflow.providers.amazon.aws.hooks.s3 import S3Hook

class MinioLoader:

    def __init__(self, conn_id = "minio_conn"):

        self.hook = S3Hook(
            aws_conn_id = conn_id
        )

    def load_data_to_minio(self, date, config):

        if not self.hook.check_for_bucket(bucket_name = config['storage']['bucket']):
            self.hook.create_bucket(bucket_name = config['storage']['bucket'])

        raw_key = f"{config['storage']['layer']}/{config['storage']['folder']}/{date}/{config['name']}.{config['storage']['format']}"
        self.hook.load_file(
            filename = config['source']['path'],
            key = raw_key,
            bucket_name = config['storage']['bucket'],
            replace = True
        )
        


