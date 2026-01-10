import boto3
from db.s3.connection import get_s3_bucket
from models.modules import ModuleModel


def register_module(module: ModuleModel, s3_client: boto3.client) -> None:
    bucket_name = get_s3_bucket()
    module_key = f"registered_modules/{module.module_name}/metadata.json"

    try:
        s3_client.head_object(Bucket=bucket_name, Key=module_key)
        raise ValueError(f"Module {module.module_name} already registered")
    except s3_client.exceptions.NoSuchKey:
        module_data = module.json().encode("utf-8")

        s3_client.put_object(
            Bucket=bucket_name,
            Key=module_key,
            Body=module_data,
            ContentType="application/json",
        )
        print(f"Module {module.module_name} registered successfully in S3")
    except Exception as e:
        raise Exception(f"Error checking module registration: {str(e)}")
