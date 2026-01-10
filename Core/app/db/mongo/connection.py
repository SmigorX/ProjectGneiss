import os

import pymongo

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
            return None
        mongo_client = pymongo.MongoClient(mongo_uri)
    return mongo_client
