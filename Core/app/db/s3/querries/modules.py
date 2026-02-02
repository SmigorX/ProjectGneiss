import boto3
from botocore.exceptions import ClientError
from db.s3.connection import get_s3_bucket
from logger import log_debug, log_error, log_info
from models.modules import ModuleModel


def register_module(module: ModuleModel, s3_client: boto3.client) -> None:
    log_debug(f"Registering module {module.module_name} in S3")
    bucket_name = get_s3_bucket()
    module_key = f"registered_modules/{module.module_name}/metadata.json"

    try:
        s3_client.head_object(Bucket=bucket_name, Key=module_key)
        log_error(f"Module {module.module_name} is already registered in S3")
        raise ValueError(f"Module {module.module_name} is already registered")

    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            module_data = module.json().encode("utf-8")
            s3_client.put_object(
                Bucket=bucket_name,
                Key=module_key,
                Body=module_data,
                ContentType="application/json",
            )
            log_debug(f"Module {module.module_name} registered successfully in S3")
        else:
            log_error(
                f"AWS S3 ClientError while checking module {module.module_name}: {str(e)}"
            )
            raise Exception(f"AWS S3 error while checking module: {str(e)}")

    except Exception as e:
        log_error(
            f"Unexpected error while checking module {module.module_name}: {str(e)}"
        )
        raise Exception(f"Unexpected error while checking module: {str(e)}")


def list_modules(s3_client: boto3.client) -> list[ModuleModel]:
    log_debug("Listing registered modules from S3")
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
        log_error(f"Error listing modules from S3: {str(e)}")
        raise Exception(f"Error listing modules from S3: {str(e)}")
