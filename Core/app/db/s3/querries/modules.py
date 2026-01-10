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


def list_modules(s3_client: boto3.client) -> list[ModuleModel]:
    bucket_name = get_s3_bucket()
    prefix = "registered_modules/"
    modules = []

    try:
        paginator = s3_client.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

        for page in pages:
            for obj in page.get("Contents", []):
                if obj["Key"].endswith("metadata.json"):
                    response = s3_client.get_object(Bucket=bucket_name, Key=obj["Key"])
                    module_data = response["Body"].read().decode("utf-8")
                    module = ModuleModel.parse_raw(module_data)
                    modules.append(module)

        print(f"Retrieved {len(modules)} modules from S3")
        return modules

    except Exception as e:
        raise Exception(f"Error listing modules from S3: {str(e)}")
