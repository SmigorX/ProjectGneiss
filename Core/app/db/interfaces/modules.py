from db.mongo.connection import get_mongo_client
from db.mongo.querries.modules import register_module as mongo_register_module
from db.s3.connection import get_s3_client
from db.s3.querries.modules import register_module as s3_register_module
from models.modules import ModuleModel


def register_module(module: ModuleModel):
    s3_storage = get_s3_client()
    mongo_storage = get_mongo_client()

    try:
        if mongo_storage:
            mongo_register_module(module, mongo_storage)
        if s3_storage:
            s3_register_module(module, s3_storage)

    except Exception as e:
        print(f"Error registering module: {e}")
        raise e
