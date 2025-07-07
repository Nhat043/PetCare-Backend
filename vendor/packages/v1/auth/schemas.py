from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class UserBaseSchema(BaseModel):
    user_id: int
    email: str
    password_hash: str
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    role_id: int
    status_id: int
    created_at: datetime
    updated_at: datetime


class UserResponseSchema(UserBaseSchema):
    role_name: str
    status_name: str


class UserCreateSchema(BaseModel):
    email: str
    password: str
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    role_id: int = 2
    status_id: int = 1


class UserUpdateSchema(BaseModel):
    password: Optional[str] = None
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None


class LoginSchema(BaseModel):
    email: str
    password: str


def serialize_user(user):
    user = dict(user)
    for k, v in user.items():
        if isinstance(v, datetime):
            user[k] = v.isoformat()
    return user
