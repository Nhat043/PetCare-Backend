from packages.core.database.postgresql import Database


class CommentRepository:
    def __init__(self):
        self.db = Database()

    def get_comment_paginated(self, page: int = 1, limit: int = 10):
        # Get comments with pagination
        comments_query = """
            SELECT * FROM comment 
            WHERE status_id = 1
            ORDER BY created_at DESC 
            LIMIT %s OFFSET %s
        """
        comments = self.db.execute_query_dict(
            comments_query, (limit, (page - 1) * limit)
        )

        # Get total count
        count_query = "SELECT COUNT(*) as total FROM comment WHERE status_id = 1"
        total_result = self.db.execute_query_dict(count_query)
        total = total_result[0]["total"] if total_result else 0

        # Calculate pagination info
        total_pages = (total + limit - 1) // limit  # Ceiling division
        has_next = page < total_pages
        has_prev = page > 1

        return {
            "comments": comments,
            "total": total,
            "total_pages": total_pages,
            "has_next": has_next,
            "has_prev": has_prev,
        }

    def get_comment(self, page: int = 1, limit: int = 10):
        query = "SELECT * FROM comment WHERE status_id = 1 LIMIT %s OFFSET %s"
        return self.db.execute_query_dict(query, (limit, (page - 1) * limit))

    def get_comment_by_entity_id_paginated(
        self,
        entity_type: str,
        entity_id: int,
        page: int = 1,
        limit: int = 10,
    ):
        # Get comments with pagination
        comments_query = """
            SELECT * FROM comment 
            WHERE entity_type = %s AND entity_id = %s AND status_id = 1
            ORDER BY created_at DESC 
            LIMIT %s OFFSET %s
        """
        comments = self.db.execute_query_dict(
            comments_query, (entity_type, entity_id, limit, (page - 1) * limit)
        )

        # Get total count
        count_query = "SELECT COUNT(*) as total FROM comment WHERE entity_type = %s AND entity_id = %s AND status_id = 1"
        total_result = self.db.execute_query_dict(count_query, (entity_type, entity_id))
        total = total_result[0]["total"] if total_result else 0

        # Calculate pagination info
        total_pages = (total + limit - 1) // limit  # Ceiling division
        has_next = page < total_pages
        has_prev = page > 1

        return {
            "comments": comments,
            "total": total,
            "total_pages": total_pages,
            "has_next": has_next,
            "has_prev": has_prev,
        }

    def get_comment_by_entity_id(
        self,
        entity_type: str,
        entity_id: int,
        page: int = 1,
        limit: int = 10,
    ):
        query = "SELECT * FROM comment WHERE entity_type = %s AND entity_id = %s AND status_id = 1 LIMIT %s OFFSET %s"
        return self.db.execute_query_dict(
            query, (entity_type, entity_id, limit, (page - 1) * limit)
        )

    def get_comment_by_user_id_paginated(
        self, entity_type: str, user_id: int, page: int = 1, limit: int = 10
    ):
        # Get comments with pagination
        comments_query = """
            SELECT * FROM comment 
            WHERE entity_type = %s AND user_id = %s AND status_id = 1
            ORDER BY created_at DESC 
            LIMIT %s OFFSET %s
        """
        comments = self.db.execute_query_dict(
            comments_query, (entity_type, user_id, limit, (page - 1) * limit)
        )

        # Get total count
        count_query = "SELECT COUNT(*) as total FROM comment WHERE entity_type = %s AND user_id = %s AND status_id = 1"
        total_result = self.db.execute_query_dict(count_query, (entity_type, user_id))
        total = total_result[0]["total"] if total_result else 0

        # Calculate pagination info
        total_pages = (total + limit - 1) // limit  # Ceiling division
        has_next = page < total_pages
        has_prev = page > 1

        return {
            "comments": comments,
            "total": total,
            "total_pages": total_pages,
            "has_next": has_next,
            "has_prev": has_prev,
        }

    def get_comment_by_user_id(
        self, entity_type: str, user_id: int, page: int = 1, limit: int = 10
    ):
        query = "SELECT * FROM comment WHERE entity_type = %s AND user_id = %s AND status_id = 1 LIMIT %s OFFSET %s"
        return self.db.execute_query_dict(
            query, (entity_type, user_id, limit, (page - 1) * limit)
        )

    def create_comment(self, comment: dict):
        query = "INSERT INTO comment (user_id, entity_type, entity_id, comment, status_id) VALUES (%s, %s, %s, %s, %s) RETURNING comment_id"
        result = self.db.execute_query_dict_returning(
            query,
            (
                comment["user_id"],
                comment["entity_type"],
                comment["entity_id"],
                comment["comment"],
                comment["status_id"],
            ),
        )
        return result[0]["comment_id"] if result else None

    def delete_comment_by_entity_id(self, entity_type: str, entity_id: int):
        query = (
            "UPDATE comment SET status_id = 2 WHERE entity_type = %s AND entity_id = %s"
        )
        return self.db.execute_query_dict(query, (entity_type, entity_id))
