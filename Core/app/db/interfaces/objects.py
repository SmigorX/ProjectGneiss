from db.mongo.connection import get_mongo_client
from db.mongo.querries.objects import create_object as mongo_create_object
from db.mongo.querries.objects import delete_object as mongo_delete_object
from db.mongo.querries.objects import export_objects as mongo_export_objects
from db.mongo.querries.objects import get_object as mongo_get_object
from db.mongo.querries.objects import import_objects as mongo_import_objects
from db.mongo.querries.objects import list_objects as mongo_list_objects
from db.mongo.querries.objects import update_object as mongo_update_object
from db.s3.connection import get_s3_client
from db.s3.querries.objects import create_object as s3_create_object
from db.s3.querries.objects import delete_object as s3_delete_object
from db.s3.querries.objects import export_objects as s3_export_objects
from db.s3.querries.objects import get_object as s3_get_object
from db.s3.querries.objects import import_objects as s3_import_objects
from db.s3.querries.objects import list_objects as s3_list_objects
from db.s3.querries.objects import update_object as s3_update_object
from models.objects import (
    CreateObjectModel,
    DeleteObjectModel,
    ExportObjectsModel,
    GetObjectModel,
    ImportObjectsModel,
    ListObjectsModel,
    UpdateObjectModel,
)


def create_object(obj: CreateObjectModel):
    s3_storage = get_s3_client()
    mongo_storage = get_mongo_client()

    try:
        if mongo_storage:
            mongo_create_object(obj, mongo_storage)
        if s3_storage:
            s3_create_object(obj, s3_storage)

    except Exception as e:
        print(f"Error creating object: {e}")
        raise e


def delete_object(obj: DeleteObjectModel):
    s3_storage = get_s3_client()
    mongo_storage = get_mongo_client()

    try:
        if mongo_storage:
            mongo_delete_object(obj, mongo_storage)
        if s3_storage:
            s3_delete_object(obj, s3_storage)

    except Exception as e:
        print(f"Error deleting object: {e}")
        raise e


def update_object(obj: UpdateObjectModel):
    s3_storage = get_s3_client()
    mongo_storage = get_mongo_client()

    try:
        if mongo_storage:
            mongo_update_object(obj, mongo_storage)
        if s3_storage:
            s3_update_object(obj, s3_storage)

    except Exception as e:
        print(f"Error updating object: {e}")
        raise e


def get_object(obj: GetObjectModel):
    s3_storage = get_s3_client()
    mongo_storage = get_mongo_client()

    content = None

    try:
        if mongo_storage:
            content = mongo_get_object(obj, mongo_storage)
        elif s3_storage:
            content = s3_get_object(obj, s3_storage)

    except Exception as e:
        print(f"Error getting object: {e}")
        raise e

    return content


def list_objects(obj: ListObjectsModel):
    s3_storage = get_s3_client()
    mongo_storage = get_mongo_client()

    objects = []

    try:
        if mongo_storage:
            objects = mongo_list_objects(obj, mongo_storage)
        elif s3_storage:
            objects = s3_list_objects(obj, s3_storage)

    except Exception as e:
        print(f"Error listing objects: {e}")
        raise e

    return objects


def export_objects(obj: ExportObjectsModel):
    s3_storage = get_s3_client()
    mongo_storage = get_mongo_client()

    objects = None

    try:
        if mongo_storage:
            objects = mongo_export_objects(obj, mongo_storage)
        elif s3_storage:
            objects = s3_export_objects(obj, s3_storage)

    except Exception as e:
        print(f"Error exporting objects: {e}")
        raise e

    return objects


def import_objects(objects: ImportObjectsModel):
    s3_storage = get_s3_client()
    mongo_storage = get_mongo_client()

    try:
        if mongo_storage:
            mongo_import_objects(objects, mongo_storage)
        if s3_storage:
            s3_import_objects(objects, s3_storage)

    except Exception as e:
        print(f"Error importing objects: {e}")
        raise e
