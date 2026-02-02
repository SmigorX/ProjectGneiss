import datetime
import json

import boto3
from db.s3.connection import get_s3_bucket
from logger import log_debug, log_error, log_info
from models.objects import (
    CreateObjectModel,
    DeleteObjectModel,
    ExportObjectsModel,
    GetObjectModel,
    ImportObjectsModel,
    ListObjectsModel,
    UpdateObjectModel,
)


def _get_key(module: str, collection: str, path: str) -> str:
    """Helper to generate consistent S3 keys."""
    log_debug(
        f"Generating S3 key for module: {module}, collection: {collection}, path: {path}"
    )
    clean_path = path.strip("/")
    return f"modules/{module}/{collection}/{clean_path}.json"


def create_object(obj: CreateObjectModel, s3_client: boto3.client) -> None:
    log_debug(
        f"Creating object in S3: module={obj.module_name}, collection={obj.collection_name}, path={obj.object_path}"
    )
    bucket_name = get_s3_bucket()
    key = _get_key(obj.module_name, obj.collection_name, obj.object_path)

    try:
        s3_client.head_object(Bucket=bucket_name, Key=key)
        log_error(f"Object at {obj.object_path} already exists in S3")
        raise Exception(f"Object at {obj.object_path} already exists in S3")
    except s3_client.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "404":
            log_debug(
                f"Object at {obj.object_path} does not exist in S3, proceeding to create"
            )
        if e.response["Error"]["Code"] != "404":
            log_error(
                f"Error checking existence of object at {obj.object_path} in S3: {str(e)}"
            )
            raise e

    data = {
        "path": obj.object_path,
        "content": obj.object_content,
        "created_at": datetime.datetime.now().isoformat(),
    }

    s3_client.put_object(
        Bucket=bucket_name,
        Key=key,
        Body=json.dumps(data).encode("utf-8"),
        ContentType="application/json",
    )


def delete_object(obj: DeleteObjectModel, s3_client: boto3.client) -> None:
    log_debug(
        f"Deleting object in S3: module={obj.module_name}, collection={obj.collection_name}, path={obj.object_path}"
    )
    bucket_name = get_s3_bucket()
    key = _get_key(obj.module_name, obj.collection_name, obj.object_path)

    try:
        s3_client.head_object(Bucket=bucket_name, Key=key)
        s3_client.delete_object(Bucket=bucket_name, Key=key)
    except s3_client.exceptions.ClientError:
        log_error(f"Object at {obj.object_path} not found in S3")
        raise Exception(f"Object at {obj.object_path} not found in S3")


def update_object(obj: UpdateObjectModel, s3_client: boto3.client) -> None:
    log_debug(
        f"Updating object in S3: module={obj.module_name}, collection={obj.collection_name}, path={obj.object_path}"
    )
    bucket_name = get_s3_bucket()
    key = _get_key(obj.module_name, obj.collection_name, obj.object_path)

    try:
        # S3 requires full overwrite, so we fetch, update, and put
        response = s3_client.get_object(Bucket=bucket_name, Key=key)
        data = json.loads(response["Body"].read().decode("utf-8"))

        data["content"] = obj.new_content
        data["updated_at"] = datetime.datetime.now().isoformat()

        s3_client.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=json.dumps(data).encode("utf-8"),
            ContentType="application/json",
        )
    except s3_client.exceptions.ClientError:
        log_error(f"Object at {obj.object_path} not found in S3")
        raise Exception(f"Object at {obj.object_path} not found in S3")


def get_object(obj: GetObjectModel, s3_client: boto3.client) -> dict:
    log_debug(
        f"Getting object from S3: module={obj.module_name}, collection={obj.collection_name}, path={obj.object_path}"
    )
    bucket_name = get_s3_bucket()
    key = _get_key(obj.module_name, obj.collection_name, obj.object_path)

    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=key)
        return json.loads(response["Body"].read().decode("utf-8"))
    except s3_client.exceptions.ClientError:
        log_error(f"Object at {obj.object_path} not found in S3")
        raise Exception(f"Object at {obj.object_path} not found in S3")


def list_objects(obj: ListObjectsModel, s3_client: boto3.client) -> list:
    log_debug(
        f"Listing objects in S3: module={obj.module_name}, collection={obj.collection_name}"
    )
    bucket_name = get_s3_bucket()
    prefix = f"modules/{obj.module_name}/{obj.collection_name}/"

    objects = []
    paginator = s3_client.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
        for item in page.get("Contents", []):
            # To match Mongo's 'exclude content' behavior, we just return metadata
            objects.append(
                {
                    "key": item["Key"],
                    "size": item["Size"],
                    "last_modified": item["LastModified"].isoformat(),
                }
            )
    return objects


def export_objects(obj: ExportObjectsModel, s3_client: boto3.client) -> dict:
    """
    Exports all collections from a specific module.
    Format: { "module_name": "...", "content": { "collection_1": [...], "collection_2": [...] } }
    """
    log_debug(f"Exporting objects from S3 for module: {obj.module_name}")
    bucket_name = get_s3_bucket()
    prefix = f"modules/{obj.module_name}/"
    export_data = {}

    paginator = s3_client.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
        for item in page.get("Contents", []):
            key = item["Key"]
            # Path parts: modules / module_name / collection_name / object.json
            parts = key.split("/")
            if len(parts) < 4:
                continue

            col_name = parts[2]
            if col_name not in export_data:
                export_data[col_name] = []

            response = s3_client.get_object(Bucket=bucket_name, Key=key)
            doc = json.loads(response["Body"].read().decode("utf-8"))

            # Ensure _id is present for compatibility with the import logic
            if "_id" not in doc:
                doc["_id"] = parts[-1].replace(".json", "")

            export_data[col_name].append(doc)

    return {"module_name": obj.module_name, "content": export_data}


def import_objects(obj: ImportObjectsModel, s3_client: boto3.client) -> None:
    """
    Imports a whole module's data into S3.
    """
    log_debug(f"Importing objects into S3 for module: {obj.module_name}")
    bucket_name = get_s3_bucket()
    data = obj.content

    if not isinstance(data, dict):
        raise Exception("Import content must be a dictionary of collections")

    for col_name, docs in data.items():
        for doc in docs:
            # Reconstruct the S3 key
            obj_path = doc.get("path") or doc.get("_id")
            if not obj_path:
                continue

            # Uses helper to create: modules/{module}/{collection}/{path}.json
            key = _get_key(obj.module_name, col_name, obj_path)

            s3_client.put_object(
                Bucket=bucket_name,
                Key=key,
                Body=json.dumps(doc).encode("utf-8"),
                ContentType="application/json",
            )
