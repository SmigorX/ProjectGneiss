from pydantic import BaseModel


class CreateObjectModel(BaseModel):
    module_name: str
    collection_name: str
    object_path: str
    object_content: str


class DeleteObjectModel(BaseModel):
    module_name: str
    collection_name: str
    object_path: str


class GetObjectModel(BaseModel):
    module_name: str
    collection_name: str
    object_path: str


class UpdateObjectModel(BaseModel):
    module_name: str
    collection_name: str
    object_path: str
    new_content: str


class ImportObjectsModel(BaseModel):
    module_name: str
    content: dict


class ExportObjectsModel(BaseModel):
    module_name: str


class ListObjectsModel(BaseModel):
    module_name: str
    collection_name: str
