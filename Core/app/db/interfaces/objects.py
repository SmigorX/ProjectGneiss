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


def create_object(obj: CreateObjectModel):
    log_debug(
        f"Starting creation for object: module={obj.module_name}, collection={obj.collection_name}, path={obj.object_path}"
    )
    s3_storage = get_s3_client()
    mongo_storage = get_mongo_client()

    try:
        if mongo_storage:
            mongo_create_object(obj, mongo_storage)
        if s3_storage:
            s3_create_object(obj, s3_storage)

    except Exception as e:
        log_error(f"Error creating object: {str(e)}")
        raise e


def delete_object(obj: DeleteObjectModel):
    log_debug(
        f"Starting deletion for object: module={obj.module_name}, collection={obj.collection_name}, path={obj.object_path}"
    )
    s3_storage = get_s3_client()
    mongo_storage = get_mongo_client()

    try:
        if mongo_storage:
            mongo_delete_object(obj, mongo_storage)
        if s3_storage:
            s3_delete_object(obj, s3_storage)

    except Exception as e:
        log_error(f"Error deleting object: {str(e)}")
        raise e


def update_object(obj: UpdateObjectModel):
    log_debug(
        f"Starting update for object: module={obj.module_name}, collection={obj.collection_name}, path={obj.object_path}"
    )
    s3_storage = get_s3_client()
    mongo_storage = get_mongo_client()

    try:
        if mongo_storage:
            mongo_update_object(obj, mongo_storage)
        if s3_storage:
            s3_update_object(obj, s3_storage)

    except Exception as e:
        log_error(f"Error updating object: {str(e)}")
        raise e


def get_object(obj: GetObjectModel):
    log_debug(
        f"Starting retrieval for object: module={obj.module_name}, collection={obj.collection_name}, path={obj.object_path}"
    )
    s3_storage = get_s3_client()
    mongo_storage = get_mongo_client()

    content = None

    try:
        if mongo_storage:
            content = mongo_get_object(obj, mongo_storage)
        elif s3_storage:
            content = s3_get_object(obj, s3_storage)

    except Exception as e:
        log_error(f"Error getting object: {str(e)}")
        raise e

    return content


def list_objects(obj: ListObjectsModel):
    log_debug(
        f"Starting to list objects: module={obj.module_name}, collection={obj.collection_name}"
    )
    s3_storage = get_s3_client()
    mongo_storage = get_mongo_client()

    objects = []

    try:
        if mongo_storage:
            objects = mongo_list_objects(obj, mongo_storage)
        elif s3_storage:
            objects = s3_list_objects(obj, s3_storage)

    except Exception as e:
        log_error(f"Error listing objects: {str(e)}")
        raise e

    return objects


def export_objects(obj: ExportObjectsModel):
    log_debug(f"Starting to export objects: module={obj.module_name}")
    s3_storage = get_s3_client()
    mongo_storage = get_mongo_client()

    objects = None

    try:
        if mongo_storage:
            objects = mongo_export_objects(obj, mongo_storage)
        elif s3_storage:
            objects = s3_export_objects(obj, s3_storage)

    except Exception as e:
        log_error(f"Error exporting objects: {str(e)}")
        raise e

    return objects


def import_objects(objects: ImportObjectsModel):
    log_debug(f"Starting to import objects into module={objects.module_name}")
    s3_storage = get_s3_client()
    mongo_storage = get_mongo_client()

    try:
        if mongo_storage:
            mongo_import_objects(objects, mongo_storage)
        if s3_storage:
            s3_import_objects(objects, s3_storage)

    except Exception as e:
        log_error(f"Error importing objects: {str(e)}")
        raise e
