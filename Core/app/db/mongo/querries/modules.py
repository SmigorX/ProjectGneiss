import pymongo
from logger import log_debug, log_error, log_info
from models.modules import ModuleModel


def register_module(module: ModuleModel, conn: pymongo.MongoClient) -> None:
    log_debug(f"Registering module {module.module_name} in MongoDB")
    db = conn["gneiss_database"]
    collection = db["registered_modules"]

    check_existing = collection.find_one({"module_name": module.module_name})
    if check_existing:
        log_error(f"Module {module.module_name} already registered in MongoDB")
        raise Exception(f"Module {module.module_name} already registered")

    collection.insert_one(module.dict())

    print(f"Module {module.module_name} registered successfully in MongoDB")
    return


def list_modules(conn: pymongo.MongoClient) -> list[ModuleModel]:
    log_debug("Listing registered modules from MongoDB")
    db = conn["gneiss_database"]
    collection = db["registered_modules"]

    modules_cursor = collection.find({})
    modules = [ModuleModel(**doc) for doc in modules_cursor]

    return modules
