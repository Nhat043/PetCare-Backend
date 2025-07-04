from pydantic import BaseModel


class RoleBaseSchema(BaseModel):
    role_id: int
    role_name: str


class RoleCreateSchema(BaseModel):
    role_name: str


class RoleUpdateSchema(BaseModel):
    role_name: str
