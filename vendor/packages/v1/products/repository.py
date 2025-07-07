from packages.core.database.postgresql import Database
from .schemas import ProductCreateSchema


class ProductRepository:
    def __init__(self):
        self.db = Database()

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
        # Build WHERE clause based on filters
        where_conditions = []
        params = []

        if name:
            where_conditions.append("p.name ILIKE %s")
            params.append(f"%{name}%")
        if category_id:
            where_conditions.append("p.category_id = %s")
            params.append(category_id)
        if status_id:
            where_conditions.append("p.status_id = %s")
            params.append(status_id)
        if tag_id:
            where_conditions.append("p.tag_id = %s")
            params.append(tag_id)
        if min_price is not None:
            where_conditions.append("p.price >= %s")
            params.append(min_price)
        if max_price is not None:
            where_conditions.append("p.price <= %s")
            params.append(max_price)

        where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"

        # Count total products with filters
        count_query = f"SELECT COUNT(*) as total FROM products p WHERE {where_clause}"
        total_result = self.db.execute_query_dict(count_query, tuple(params))
        total = total_result[0]["total"] if total_result else 0

        # Calculate pagination info
        offset = (page - 1) * limit
        total_pages = (total + limit - 1) // limit  # Ceiling division
        has_next = page < total_pages
        has_prev = page > 1

        # Get products with category, tag, and status names using LEFT JOINs
        products_query = f"""
            SELECT 
                p.product_id,
                p.name,
                p.description,
                p.price,
                p.stock,
                p.category_id,
                p.status_id,
                p.tag_id,
                p.image_url,
                p.created_at,
                p.updated_at,
                c.category_name,
                t.tag_name,
                ps.status_name,
                CASE 
                    WHEN COUNT(r.rating_id) = 0 THEN 5
                    ELSE COALESCE(AVG(r.rating), 5)
                END as average_rating,
                COUNT(r.rating_id) as review_count
            FROM products p
            LEFT JOIN category c ON p.category_id = c.category_id
            LEFT JOIN tag t ON p.tag_id = t.tag_id
            LEFT JOIN product_status ps ON p.status_id = ps.status_id
            LEFT JOIN rating r ON p.product_id = r.entity_id AND r.entity_type = 'product' AND r.status_id = 1
            WHERE {where_clause}
            GROUP BY p.product_id, p.name, p.description, p.price, p.stock, p.category_id, p.status_id, p.tag_id, p.image_url, p.created_at, p.updated_at, c.category_name, t.tag_name, ps.status_name
            ORDER BY p.created_at DESC 
            LIMIT %s OFFSET %s
        """
        params.extend([limit, offset])
        products = self.db.execute_query_dict(products_query, tuple(params))

        return {
            "products": products,
            "total": total,
            "total_pages": total_pages,
            "has_next": has_next,
            "has_prev": has_prev,
            "filters": {
                "name": name,
                "category_id": category_id,
                "status_id": status_id,
                "min_price": min_price,
                "max_price": max_price,
                "tag_id": tag_id,
            },
        }

    def get_products(self):
        query = """
            SELECT 
                p.product_id,
                p.name,
                p.description,
                p.price,
                p.stock,
                p.category_id,
                p.status_id,
                p.tag_id,
                p.image_url,
                p.created_at,
                p.updated_at,
                c.category_name,
                t.tag_name,
                ps.status_name,
                CASE 
                    WHEN COUNT(r.rating_id) = 0 THEN 5
                    ELSE COALESCE(AVG(r.rating), 5)
                END as average_rating,
                COUNT(r.rating_id) as review_count
            FROM products p
            LEFT JOIN category c ON p.category_id = c.category_id
            LEFT JOIN tag t ON p.tag_id = t.tag_id
            LEFT JOIN product_status ps ON p.status_id = ps.status_id
            LEFT JOIN rating r ON p.product_id = r.entity_id AND r.entity_type = 'product' AND r.status_id = 1
            GROUP BY p.product_id, p.name, p.description, p.price, p.stock, p.category_id, p.status_id, p.tag_id, p.image_url, p.created_at, p.updated_at, c.category_name, t.tag_name, ps.status_name
        """
        result = self.db.execute_query_dict(query)
        return result

    def get_product(self, product_id: int):
        query = """
            SELECT 
                p.product_id,
                p.name,
                p.description,
                p.price,
                p.stock,
                p.category_id,
                p.status_id,
                p.tag_id,
                p.image_url,
                p.created_at,
                p.updated_at,
                c.category_name,
                t.tag_name,
                ps.status_name,
                CASE 
                    WHEN COUNT(r.rating_id) = 0 THEN 5
                    ELSE COALESCE(AVG(r.rating), 5)
                END as average_rating,
                COUNT(r.rating_id) as review_count
            FROM products p
            LEFT JOIN category c ON p.category_id = c.category_id
            LEFT JOIN tag t ON p.tag_id = t.tag_id
            LEFT JOIN product_status ps ON p.status_id = ps.status_id
            LEFT JOIN rating r ON p.product_id = r.entity_id AND r.entity_type = 'product' AND r.status_id = 1
            WHERE p.product_id = %s
            GROUP BY p.product_id, p.name, p.description, p.price, p.stock, p.category_id, p.status_id, p.tag_id, p.image_url, p.created_at, p.updated_at, c.category_name, t.tag_name, ps.status_name
            ORDER BY p.average_rating DESC
        """
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
