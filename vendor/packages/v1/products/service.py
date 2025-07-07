from .repository import ProductRepository
from .schemas import ProductCreateSchema


class ProductService:
    def __init__(self):
        self.repo = ProductRepository()

    def get_products(self):
        return self.repo.get_products()

    def get_product(self, product_id: int):
        return self.repo.get_product(product_id)

    def create_product(self, product: ProductCreateSchema):
        return self.repo.create_product(product)

    def get_products_paginated(
        self,
        page: int = 1,
        limit: int = 10,
        name: str = None,
        category_id: int = None,
        status_id: int = None,
        min_price: float = None,
        max_price: float = None,
        tag_id: int = None,
    ):
        return self.repo.get_products_paginated(
            page=page,
            limit=limit,
            name=name,
            category_id=category_id,
            status_id=status_id,
            min_price=min_price,
            max_price=max_price,
            tag_id=tag_id,
        )

    def delete_product(self, product_id: int):
        product = self.get_product(product_id)
        if product is None:
            return None
        return self.repo.delete_product(product_id)
