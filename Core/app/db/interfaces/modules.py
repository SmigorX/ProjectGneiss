from db.mongo.connection import get_mongo_client
from db.mongo.querries.modules import list_modules as mongo_list_modules
from db.mongo.querries.modules import register_module as mongo_register_module
from db.s3.connection import get_s3_client
from db.s3.querries.modules import list_modules as s3_list_modules
from db.s3.querries.modules import register_module as s3_register_module
from logger import log_debug, log_error, log_info
from models.modules import ModuleModel


def register_module(module: ModuleModel):
    log_debug(f"Starting registration for module: {module.module_name}")
    s3_storage = get_s3_client()
    mongo_storage = get_mongo_client()

    try:
        if mongo_storage:
            mongo_register_module(module, mongo_storage)
        if s3_storage:
            s3_register_module(module, s3_storage)

    except Exception as e:
        log_error(f"Error registering module: {str(e)}")
        raise e


def list_modules():
    log_debug("Starting to list registered modules")
    s3_storage = get_s3_client()
    mongo_storage = get_mongo_client()

    modules = None

    try:
        if mongo_storage:
            modules = mongo_list_modules(mongo_storage)
        elif s3_storage:
            modules = s3_list_modules(s3_storage)

    except Exception as e:
        log_error(f"Error listing modules: {str(e)}")
        raise e

    return modules
