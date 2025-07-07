from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class PostBaseSchema(BaseModel):
    post_id: int
    user_id: int
    title: str
    content_html: str
    category_id: int
    image_url: Optional[str] = None
    status_id: int
    tag_id: int
    created_at: datetime
    updated_at: datetime


class PostResponseSchema(PostBaseSchema):
    category_name: str
    status_name: str
    tag_name: str
    average_rating: Optional[float] = 0.0
    review_count: Optional[int] = 0


class PostSingleResponseSchema(PostBaseSchema):
    average_rating: Optional[float] = 0.0
    review_count: Optional[int] = 0
    comments: List[str]


class PostCreateSchema(BaseModel):
    user_id: int
    title: str
    content_html: str
    category_id: int
    image_url: Optional[str] = None
    status_id: int = 1


class PostImageSchema(BaseModel):
    image_url: str


def serialize_post(post):
    post = dict(post)
    for k, v in post.items():
        if isinstance(v, datetime):
            post[k] = v.isoformat()
    return post
