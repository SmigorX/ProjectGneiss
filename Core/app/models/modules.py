from pydantic import BaseModel


class ModuleModel(BaseModel):
    module_name: str
    module_version: str
    module_type: str
