import os
import sys

import fastapi
import uvicorn
from api.modules import router as modules_router
from api.objects import router as objects_router
from db.mongo.connection import get_mongo_client
from db.s3.connection import get_s3_client

app = fastapi.FastAPI()


def main():
    s3_client = get_s3_client()
    mongo_client = get_mongo_client()

    if s3_client:
        print("S3 client initialized successfully.")

    if mongo_client:
        print("MongoDB client initialized successfully.")

    if not s3_client and not mongo_client:
        print("No storage clients could be initialized.")
        sys.exit(1)

    app.include_router(modules_router)
    app.include_router(objects_router)
    print("API routes registered successfully.")

    port = int(os.getenv("PORT", 8000))

    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
