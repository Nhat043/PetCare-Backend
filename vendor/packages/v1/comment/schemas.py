from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class CommentBaseSchema(BaseModel):
    comment_id: int
    user_id: int
    entity_type: str
    entity_id: int
    comment: str
    status_id: int
    created_at: datetime
    updated_at: datetime


class CommentResponseSchema(CommentBaseSchema):
    full_name: str


class CommentCreateSchema(BaseModel):
    user_id: int
    entity_type: str
    entity_id: int
    comment: str
    status_id: int = 1


def serialize_comment(comment):
    comment = dict(comment)
    for k, v in comment.items():
        if isinstance(v, datetime):
            comment[k] = v.isoformat()
    return comment
