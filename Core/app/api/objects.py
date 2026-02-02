from db.interfaces.objects import (
    create_object,
    delete_object,
    export_objects,
    get_object,
    import_objects,
    list_objects,
    update_object,
)
from fastapi import APIRouter, HTTPException, status
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

router = APIRouter()


@router.post("/api/v1/objects/new")
async def new_object(obj: CreateObjectModel):
    try:
        create_object(obj)
        return {"message": f"Object {obj.object_path} created successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/api/v1/objects/delete")
async def remove_object(obj: DeleteObjectModel):
    try:
        delete_object(obj)
        return {"message": f"Object {obj.object_path} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/api/v1/objects/update")
async def modify_object(obj: UpdateObjectModel):
    try:
        update_object(obj)
        return {"message": f"Object {obj.object_path} updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/api/v1/objects/get")
async def fetch_object(obj: GetObjectModel):
    try:
        result = get_object(obj)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/api/v1/objects/import")
async def import_object(obj: ImportObjectsModel):
    try:
        import_objects(obj)
        return {"message": f"Objects imported successfully into {obj.module_name}"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/api/v1/objects/export")
async def export_data(obj: ExportObjectsModel):
    try:
        result = export_objects(obj)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/api/v1/objects/list")
async def list_all_objects(obj: ListObjectsModel):
    try:
        result = list_objects(obj)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
