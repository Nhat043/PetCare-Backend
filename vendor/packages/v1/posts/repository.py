from packages.core.database.postgresql import Database
from typing import Optional, Dict, Any


class PostRepository:
    def __init__(self):
        self.db = Database()

    def get_posts(
        self,
        user_id: int = None,
        category_id: int = None,
        status_id: int = None,
        tag_id: int = None,
        title: str = None,
        page: int = 1,
        limit: int = 10,
    ):
        # Build WHERE clause based on filters
        where_conditions = []
        params = []

        if user_id:
            where_conditions.append("p.user_id = %s")
            params.append(user_id)
        if category_id:
            where_conditions.append("p.category_id = %s")
            params.append(category_id)
        if status_id:
            where_conditions.append("p.status_id = %s")
            params.append(status_id)
        if tag_id:
            where_conditions.append("p.tag_id = %s")
            params.append(tag_id)
        if title:
            where_conditions.append("p.title ILIKE %s")
            params.append(f"%{title}%")

        where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"

        # Count total posts
        count_query = f"SELECT COUNT(*) FROM posts p WHERE {where_clause}"
        total_result = self.db.execute_query_dict(count_query, tuple(params))
        total = total_result[0]["count"] if total_result else 0

        # Calculate pagination
        offset = (page - 1) * limit
        total_pages = (total + limit - 1) // limit
        has_next = page < total_pages
        has_prev = page > 1

        # Get posts with ratings, category, tag, and status names using LEFT JOINs
        query = f"""
            SELECT 
                p.post_id, 
                p.title, 
                p.user_id, 
                p.content_html, 
                p.category_id, 
                p.image_url, 
                p.status_id, 
                p.tag_id,
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
            FROM posts p
            LEFT JOIN category c ON p.category_id = c.category_id
            LEFT JOIN tag t ON p.tag_id = t.tag_id
            LEFT JOIN post_status ps ON p.status_id = ps.status_id
            LEFT JOIN rating r ON p.post_id = r.entity_id AND r.entity_type = 'post' AND r.status_id = 1
            WHERE {where_clause}
            GROUP BY p.post_id, p.title, p.user_id, p.content_html, p.category_id, p.image_url, p.status_id, p.tag_id, p.created_at, p.updated_at, c.category_name, t.tag_name, ps.status_name
            ORDER BY average_rating DESC, p.created_at DESC 
            LIMIT %s OFFSET %s
        """
        params.extend([limit, offset])
        posts = self.db.execute_query_dict(query, tuple(params))
        print("where_clause", where_clause)
        print("query", query)
        return {
            "posts": posts,
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": total_pages,
            "has_next": has_next,
            "has_prev": has_prev,
            "filters": {
                "user_id": user_id,
                "category_id": category_id,
                "status_id": status_id,
                "tag_id": tag_id,
                "title": title,
            },
        }

    def get_post(self, post_id: int):
        query = """
            SELECT 
                p.post_id, 
                p.title, 
                p.user_id, 
                p.content_html, 
                p.category_id, 
                p.image_url, 
                p.status_id, 
                p.tag_id,
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
            FROM posts p
            LEFT JOIN category c ON p.category_id = c.category_id
            LEFT JOIN tag t ON p.tag_id = t.tag_id
            LEFT JOIN post_status ps ON p.status_id = ps.status_id
            LEFT JOIN rating r ON p.post_id = r.entity_id AND r.entity_type = 'post' AND r.status_id = 1
            WHERE p.post_id = %s
            GROUP BY p.post_id, p.title, p.user_id, p.content_html, p.category_id, p.image_url, p.status_id, p.tag_id, p.created_at, p.updated_at, c.category_name, t.tag_name, ps.status_name
        """
        result = self.db.execute_query_dict(query, (post_id,))
        return result[0] if result else None

    def get_total_posts(self):
        query = "SELECT COUNT(*) as total FROM posts"
        result = self.db.execute_query_dict(query)
        return result[0]["total"] if result else 0

    def create_post(self, post: dict):
        query = """
            INSERT INTO posts (title, user_id, content_html, category_id, image_url, status_id, tag_id) 
            VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING post_id
        """
        result = self.db.execute_query_dict_returning(
            query,
            (
                post["title"],
                post["user_id"],
                post["content_html"],
                post["category_id"],
                post["image_url"],
                post["status_id"],
                post["tag_id"],
            ),
        )
        return result[0]["post_id"] if result else None

    def update_post(self, post_id: int, post: dict):
        # Only update fields that are present in the input dict (not None)
        allowed_fields = [
            "title",
            "content_html",
            "category_id",
            "image_url",
            "status_id",
            "tag_id",
        ]
        set_clauses = []
        params = []
        for field in allowed_fields:
            if field in post and post[field] is not None:
                set_clauses.append(f"{field} = %s")
                params.append(post[field])
        if not set_clauses:
            # No fields to update
            return None
        set_clause = ", ".join(set_clauses)
        query = f"UPDATE posts SET {set_clause} WHERE post_id = %s"
        params.append(post_id)
        self.db.execute_query(query, tuple(params))
        result = self.db.execute_query_dict(
            """
            SELECT 
                p.post_id, 
                p.title, 
                p.user_id, 
                p.content_html, 
                p.category_id, 
                p.image_url, 
                p.status_id, 
                p.tag_id,
                p.created_at, 
                p.updated_at,
                c.category_name,
                t.tag_name,
                ps.status_name
            FROM posts p
            LEFT JOIN category c ON p.category_id = c.category_id
            LEFT JOIN tag t ON p.tag_id = t.tag_id
            LEFT JOIN post_status ps ON p.status_id = ps.status_id
            WHERE p.post_id = %s
            """,
            (post_id,),
        )
        return result[0] if result else None

    def delete_post(self, post_id: int):
        query = "UPDATE posts SET status_id = 4 WHERE post_id = %s"
        return self.db.execute_query(query, (post_id,))
