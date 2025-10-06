from src.cloud.s3_client import S3Client

def download_object(s3_client, bucket, object_key):
    ciphertext, metadata = s3_client.download(bucket, object_key)
    return ciphertext, metadata
