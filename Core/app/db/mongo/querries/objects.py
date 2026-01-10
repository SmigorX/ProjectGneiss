import datetime
import json

import bson
import pymongo
from models.objects import (
    CreateObjectModel,
    DeleteObjectModel,
    ExportObjectsModel,
    GetObjectModel,
    ImportObjectsModel,
    ListObjectsModel,
    UpdateObjectModel,
)


def create_object(obj: CreateObjectModel, conn: pymongo.MongoClient) -> None:
    db = conn[obj.module_name]
    collection = db[obj.collection_name]
    doc_id = obj.object_path.strip("/")

    if collection.find_one({"_id": doc_id}):
        raise Exception(f"Object at {obj.object_path} already exists")

    collection.insert_one(
        {
            "_id": doc_id,
            "path": obj.object_path,
            "content": obj.object_content,
            "created_at": datetime.datetime.now(),
        }
    )


def delete_object(obj: DeleteObjectModel, conn: pymongo.MongoClient) -> None:
    db = conn[obj.module_name]
    collection = db[obj.collection_name]
    doc_id = obj.object_path.strip("/")

    result = collection.delete_one({"_id": doc_id})
    if result.deleted_count == 0:
        raise Exception(f"Object at {obj.object_path} not found")


def update_object(obj: UpdateObjectModel, conn: pymongo.MongoClient) -> None:
    db = conn[obj.module_name]
    collection = db[obj.collection_name]
    doc_id = obj.object_path.strip("/")

    result = collection.update_one(
        {"_id": doc_id},
        {"$set": {"content": obj.new_content, "updated_at": datetime.datetime.now()}},
    )
    if result.matched_count == 0:
        raise Exception(f"Object at {obj.object_path} not found")


def get_object(obj: GetObjectModel, conn: pymongo.MongoClient) -> dict:
    db = conn[obj.module_name]
    collection = db[obj.collection_name]
    doc_id = obj.object_path.strip("/")

    doc = collection.find_one({"_id": doc_id})
    if not doc:
        raise Exception(f"Object at {obj.object_path} not found")
    return doc


def list_objects(obj: ListObjectsModel, conn: pymongo.MongoClient) -> list:
    """Lists all objects within a specific module (DB) and collection."""
    db = conn[obj.module_name]
    collection = db[obj.collection_name]

    # Exclude content to keep the list lightweight
    cursor = collection.find({}, {"content": 0})
    return list(cursor)


def export_objects(obj: ExportObjectsModel, conn: pymongo.MongoClient) -> str:
    """
    Exports all collections from a specific module into one JSON string.
    Format: { "collection_1": [...], "collection_2": [...] }
    """
    db = conn[obj.module_name]
    export_data = {}

    for col_name in db.list_collection_names():
        # Exclude internal MongoDB system collections
        if col_name.startswith("system."):
            continue

        docs = list(db[col_name].find({}))
        for d in docs:
            # Handle ISO format for datetimes
            if "created_at" in d and isinstance(d["created_at"], datetime.datetime):
                d["created_at"] = d["created_at"].isoformat()
            if "updated_at" in d and isinstance(d["updated_at"], datetime.datetime):
                d["updated_at"] = d["updated_at"].isoformat()

            # Use the top-level bson module to check for ObjectId
            if isinstance(d.get("_id"), bson.ObjectId):
                d["_id"] = str(d["_id"])

        export_data[col_name] = docs

    return json.dumps(export_data, indent=4)


def import_objects(obj: ImportObjectsModel, conn: pymongo.MongoClient) -> None:
    """
    Imports a whole module's data. Collection names are derived from the JSON keys.
    """
    try:
        data = json.loads(obj.content)
    except json.JSONDecodeError:
        raise Exception("Invalid JSON content provided for import")

    if not isinstance(data, dict):
        raise Exception("Import content must be a dictionary of collections")

    db = conn[obj.module_name]

    for col_name, docs in data.items():
        collection = db[col_name]
        for doc in docs:
            if "_id" in doc:
                # Use replace_one with upsert to avoid duplicate errors on re-import
                collection.replace_one({"_id": doc["_id"]}, doc, upsert=True)
            else:
                collection.insert_one(doc)
