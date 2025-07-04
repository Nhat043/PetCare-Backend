from packages.core.database.postgresql import Database
from .schemas import ProductCreateSchema


class ProductRepository:
    def __init__(self):
        self.db = Database()

    def get_products_paginated(self, page: int = 1, limit: int = 10):
        # Get products with pagination
        products_query = """
            SELECT * FROM products 
            ORDER BY created_at DESC 
            LIMIT %s OFFSET %s
        """
        products = self.db.execute_query_dict(
            products_query, (limit, (page - 1) * limit)
        )

        # Get total count
        count_query = "SELECT COUNT(*) as total FROM products"
        total_result = self.db.execute_query_dict(count_query)
        total = total_result[0]["total"] if total_result else 0

        # Calculate pagination info
        total_pages = (total + limit - 1) // limit  # Ceiling division
        has_next = page < total_pages
        has_prev = page > 1

        return {
            "products": products,
            "total": total,
            "total_pages": total_pages,
            "has_next": has_next,
            "has_prev": has_prev,
        }

    def get_products(self):
        query = "SELECT * FROM products"
        result = self.db.execute_query_dict(query)
        return result

    def get_product(self, product_id: int):
        query = "SELECT * FROM products WHERE product_id = %s"
        result = self.db.execute_query_dict(query, (product_id,))
        return result[0] if result else None

    def create_product(self, product: dict):
        query = """
            INSERT INTO products (name, description, price, stock, category_id, status_id, image_url) 
            VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING product_id
        """
        result = self.db.execute_query_dict_returning(
            query,
            (
                product["name"],
                product.get("description"),
                product["price"],
                product.get("stock", 0),
                product.get("category_id"),
                product.get("status_id"),
                product.get("image_url"),
            ),
        )
        print("result", result)
        return result[0]["product_id"] if result else None

    def delete_product(self, product_id: int):
        query = "UPDATE products SET status_id = 2 WHERE product_id = %s"
        return self.db.execute_query(query, (product_id,))
