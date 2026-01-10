import os

import boto3

s3_client = None
s3_bucket = None


def get_s3_client() -> boto3.client:
    """
    Get an S3 client instance.
    Returns:
        boto3.client: S3 client instance.
    """
    global s3_client, s3_bucket

    if s3_client is not None:
        return s3_client

    if s3_client is None:
        s3_access_key = os.getenv("S3_ACCESS_KEY_ID")
        s3_secret_key = os.getenv("S3_SECRET_ACCESS_KEY")
        s3_region = os.getenv("S3_REGION")
        s3_bucket = os.getenv("S3_BUCKET_NAME")

        if not all([s3_access_key, s3_secret_key, s3_region, s3_bucket]):
            return None

        s3_client = boto3.client(
            "s3",
            region_name=s3_region,
            aws_access_key_id=s3_access_key,
            aws_secret_access_key=s3_secret_key,
        )

        s3_bucket = s3_bucket
    return s3_client


def get_s3_bucket() -> str | None:
    """
    Get the S3 bucket name.
    Returns:
        str: S3 bucket name.
    """
    global s3_bucket
    if s3_bucket is None:
        s3_bucket = os.getenv("S3_BUCKET_NAME")
    return s3_bucket
