from pydantic import BaseModel


class CategorySchema(BaseModel):
    category_id: int
    category_name: str


class CategoryCreateSchema(BaseModel):
    category_name: str


class CategoryUpdateSchema(BaseModel):
    category_name: str


class CategoryDeleteSchema(BaseModel):
    category_id: int
