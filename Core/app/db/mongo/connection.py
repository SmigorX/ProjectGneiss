import os

import pymongo
from logger import log_debug, log_error, log_info

mongo_client = None


def get_mongo_client() -> pymongo.MongoClient | None:
    """
    Get a MongoDB client instance.
    Returns:
        pymongo.MongoClient: MongoDB client instance.
    """
    global mongo_client

    if mongo_client is not None:
        return mongo_client

    if mongo_client is None:
        mongo_uri = os.getenv("MONGO_URL")
        if not mongo_uri or mongo_uri.strip() == "":
            log_debug(
                "MongoDB URI is not configured. MongoDB client will not be created."
            )
            return None
        mongo_client = pymongo.MongoClient(mongo_uri)
    return mongo_client
