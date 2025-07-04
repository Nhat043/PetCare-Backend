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

    def get_products_paginated(self, page: int = 1, limit: int = 10):
        return self.repo.get_products_paginated(page=page, limit=limit)
