from pydantic import BaseModel


class TagBaseSchema(BaseModel):
    tag_id: int
    tag_name: str


class TagCreateSchema(BaseModel):
    tag_name: str
