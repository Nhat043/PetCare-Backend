from datetime import datetime
from pydantic import BaseModel, field_validator
from typing import Optional


class ProductBaseSchema(BaseModel):
    product_id: int
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    category_id: int
    status_id: int
    tag_id: int
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class ProductResponseSchema(ProductBaseSchema):
    category_name: str
    status_name: str
    tag_name: str
    average_rating: Optional[float] = 0.0
    review_count: Optional[int] = 0


class ProductCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int = 0
    category_id: int
    status_id: int = 1
    image_url: Optional[str] = None


def serialize_product(product):
    product = dict(product)
    for k, v in product.items():
        if isinstance(v, datetime):
            product[k] = v.isoformat()
    return product
