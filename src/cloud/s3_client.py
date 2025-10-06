import boto3
from botocore.exceptions import ClientError
import time

class S3Client:
    def __init__(self, aws_access_key, aws_secret_key, region):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region
        )

    def upload(self, bucket, key, data, metadata):
        try:
            self.s3.put_object(Bucket=bucket, Key=key, Body=data, Metadata=metadata)
        except ClientError:
            time.sleep(2)
            self.s3.put_object(Bucket=bucket, Key=key, Body=data, Metadata=metadata)

    def download(self, bucket, key):
        try:
            obj = self.s3.get_object(Bucket=bucket, Key=key)
            return obj['Body'].read(), obj['Metadata']
        except ClientError:
            raise
