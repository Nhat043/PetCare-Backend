from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class RatingBaseSchema(BaseModel):
    rating_id: int
    user_id: int
    entity_type: str
    entity_id: int
    rating: int
    status_id: int
    created_at: datetime
    updated_at: datetime


class RatingCreateSchema(BaseModel):
    user_id: int
    entity_type: str
    entity_id: int
    rating: int
    status_id: int = 1


def serialize_rating(rating):
    rating = dict(rating)
    for k, v in rating.items():
        if isinstance(v, datetime):
            rating[k] = v.isoformat()
    return rating
