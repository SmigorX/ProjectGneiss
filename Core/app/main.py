import logging
import os
import sys

import fastapi
import uvicorn
from api.modules import router as modules_router
from api.objects import router as objects_router
from db.mongo.connection import get_mongo_client
from db.s3.connection import get_s3_client
from logger import log_debug, log_error, log_info, start_logger

app = fastapi.FastAPI()


def main():
    start_logger()
    log_debug("Connecting to S3")
    s3_client = get_s3_client()
    log_debug("Connecting to MongoDB")
    mongo_client = get_mongo_client()

    if s3_client:
        log_info("S3 client initialized successfully.")

    if mongo_client:
        log_info("MongoDB client initialized successfully.")

    if not s3_client and not mongo_client:
        log_error("No storage backend configured. Exiting application.")
        sys.exit(1)

    log_debug("Registering API routes")
    app.include_router(modules_router)
    log_debug("Modules router registered")
    app.include_router(objects_router)
    log_debug("Objects router registered")

    port = int(os.getenv("PORT", 8000))

    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
