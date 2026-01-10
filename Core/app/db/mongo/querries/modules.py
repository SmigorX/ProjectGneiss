import pymongo
from models.modules import ModuleModel


def register_module(module: ModuleModel, conn: pymongo.MongoClient) -> None:
    db = conn["gneiss_database"]
    collection = db["registered_modules"]

    check_existing = collection.find_one({"module_name": module.module_name})
    if check_existing:
        raise Exception(f"Module {module.module_name} already registered")

    collection.insert_one(module.dict())

    print(f"Module {module.module_name} registered successfully")
    return


def list_modules(conn: pymongo.MongoClient) -> list[ModuleModel]:
    db = conn["gneiss_database"]
    collection = db["registered_modules"]

    modules_cursor = collection.find({})
    modules = [ModuleModel(**doc) for doc in modules_cursor]

    return modules
