from db.interfaces.modules import list_modules, register_module
from fastapi import APIRouter, HTTPException, status
from models.modules import ModuleModel

router = APIRouter()


@router.post("/api/v1/modules/new")
async def new_module(module: ModuleModel):
    try:
        register_module(module)
        return {"message": f"Module {module.module_name} registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/api/v1/modules")
async def list_all_modules():
    try:
        modules = list_modules()
        return {"modules": modules}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
