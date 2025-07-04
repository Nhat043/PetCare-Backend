from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PostBaseSchema(BaseModel):
    post_id: int
    user_id: int
    title: str
    content_html: str
    category_id: int
    image_url: Optional[str] = None
    status_id: int
    created_at: datetime
    updated_at: datetime


class PostCreateSchema(BaseModel):
    user_id: int
    title: str
    content_html: str
    category_id: int
    image_url: Optional[str] = None
    status_id: int = 1


def serialize_post(post):
    post = dict(post)
    for k, v in post.items():
        if isinstance(v, datetime):
            post[k] = v.isoformat()
    return post
