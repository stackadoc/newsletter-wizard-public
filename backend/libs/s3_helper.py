import boto3
import requests

from libs import config


s3_client = boto3.client(
    's3',
    endpoint_url=config.CUSTOM_AWS_ENDPOINT_URL,
    aws_access_key_id=config.CUSTOM_AWS_ACCESS_KEY_ID,
    aws_secret_access_key=config.CUSTOM_AWS_SECRET_ACCESS_KEY,
    region_name=config.CUSTOM_AWS_REGION_NAME,
)

def upload_file_from_url(url: str, bucket_name: str, s3_key: str, extra: dict = None):

    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        s3_client.upload_fileobj(response.raw, bucket_name, s3_key, ExtraArgs=extra)

    # Return the public URL
    return f"{config.CUSTOM_AWS_ENDPOINT_URL}/{bucket_name}/{s3_key}"


def upload_from_bytes(image_bytes, bucket_name, s3_key, extra: dict = None):

    s3_client.put_object(
        Bucket=bucket_name,
        Key=s3_key,
        Body=image_bytes,
        **extra,
    )

    # Return the public URL
    return f"{config.CUSTOM_AWS_ENDPOINT_URL}/{bucket_name}/{s3_key}"