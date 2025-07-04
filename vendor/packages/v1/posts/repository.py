from packages.core.database.postgresql import Database
from typing import Optional, Dict, Any


class PostRepository:
    def __init__(self):
        self.db = Database()

    def get_post(self, post_id: int):
        query = "SELECT * FROM posts WHERE post_id = %s"
        result = self.db.execute_query_dict(query, (post_id,))
        return result[0] if result else None

    def get_posts_paginated(self, page: int = 1, limit: int = 10):
        offset = (page - 1) * limit
        query = "SELECT * FROM posts ORDER BY created_at DESC LIMIT %s OFFSET %s"
        return self.db.execute_query_dict(query, (limit, offset))

    def get_total_posts(self):
        query = "SELECT COUNT(*) as total FROM posts"
        return self.db.execute_query_dict(query)

    def get_posts(
        self,
        user_id: Optional[int] = None,
        category_id: Optional[int] = None,
        status_id: Optional[int] = None,
        title: Optional[str] = None,
        page: int = 1,
        limit: int = 10,
    ) -> Dict[str, Any]:
        """
        Flexible search method that filters by any combination of parameters
        """
        # Build WHERE clause dynamically
        conditions = []
        params = []

        if user_id is not None:
            conditions.append("user_id = %s")
            params.append(user_id)

        if category_id is not None:
            conditions.append("category_id = %s")
            params.append(category_id)

        if status_id is not None:
            conditions.append("status_id = %s")
            params.append(status_id)

        if title is not None:
            conditions.append("title ILIKE %s")
            params.append(f"%{title}%")

        # Build the query
        where_clause = ""
        if conditions:
            where_clause = "WHERE " + " AND ".join(conditions)

        # Get total count for pagination
        count_query = f"SELECT COUNT(*) as total FROM posts {where_clause}"
        total_result = self.db.execute_query_dict(count_query, tuple(params))
        total = total_result[0]["total"] if total_result else 0

        # Get paginated results
        offset = (page - 1) * limit
        search_query = f"""
            SELECT * FROM posts 
            {where_clause}
            ORDER BY created_at DESC 
            LIMIT %s OFFSET %s
        """
        search_params = params + [limit, offset]
        posts = self.db.execute_query_dict(search_query, tuple(search_params))

        # Calculate pagination info
        total_pages = (total + limit - 1) // limit
        has_next = page < total_pages
        has_prev = page > 1

        return {
            "posts": posts,
            "total": total,
            "total_pages": total_pages,
            "has_next": has_next,
            "has_prev": has_prev,
            "page": page,
            "limit": limit,
            "filters": {
                "user_id": user_id,
                "category_id": category_id,
                "status_id": status_id,
                "title": title,
            },
        }

    def create_post(self, post: dict):
        query = """
            INSERT INTO posts (title, user_id, content_html, category_id, image_url, status_id) 
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING post_id
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
            ),
        )
        print("result", result)
        return result[0]["post_id"] if result else None

    def update_post(self, post_id: int, post: dict):
        query = "UPDATE posts SET title = %s, content_html = %s, category_id = %s, image_url = %s, status_id = %s WHERE post_id = %s"
        self.db.execute_query(
            query,
            (
                post["title"],
                post["content_html"],
                post["category_id"],
                post["image_url"],
                post["status_id"],
                post_id,
            ),
        )
        result = self.db.execute_query_dict(
            "SELECT post_id, title, user_id, content_html, category_id, image_url, status_id, created_at, updated_at FROM posts WHERE post_id = %s",
            (post_id,),
        )
        return result[0] if result else None

    def delete_post(self, post_id: int):
        query = "UPDATE posts SET status_id = 4 WHERE post_id = %s"
        return self.db.execute_query(query, (post_id,))
