from packages.core.database.postgresql import Database


class RatingRepository:
    def __init__(self):
        self.db = Database()

    def get_rating(self, page: int = 1, limit: int = 10):
        query = "SELECT * FROM rating WHERE status_id = 1 LIMIT %s OFFSET %s"
        return self.db.execute_query_dict(query, (limit, (page - 1) * limit))

    def get_rating_by_entity_id(self, entity_type: str, entity_id: int):
        query = "SELECT * FROM rating WHERE entity_type = %s AND entity_id = %s"
        return self.db.execute_query_dict(query, (entity_type, entity_id))

    def get_rating_by_user_id(self, entity_type: str, user_id: int):
        query = "SELECT * FROM rating WHERE entity_type = %s AND user_id = %s"
        return self.db.execute_query_dict(query, (entity_type, user_id))

    def get_rating_by_user_id_and_entity_id(
        self, entity_type: str, user_id: int, entity_id: int
    ):
        query = "SELECT * FROM rating WHERE entity_type = %s AND user_id = %s AND entity_id = %s"
        return self.db.execute_query_dict(query, (entity_type, user_id, entity_id))

    def create_rating(self, rating: dict):
        query = """
            INSERT INTO rating (user_id, entity_type, entity_id, rating, status_id)
            VALUES (%s, %s, %s, %s, %s) RETURNING rating_id
        """
        result = self.db.execute_query_dict_returning(
            query,
            (
                rating["user_id"],
                rating["entity_type"],
                rating["entity_id"],
                rating["rating"],
                rating["status_id"],
            ),
        )
        return result[0]["rating_id"] if result else None

    def update_rating(self, rating_id: int, rating: int):
        query = "UPDATE rating SET rating = %s WHERE rating_id = %s RETURNING rating_id"
        result = self.db.execute_query_dict_returning(query, (rating, rating_id))
        return result[0]["rating_id"] if result else None

    def delete_rating_by_entity_id(self, entity_type: str, entity_id: int):
        query = (
            "UPDATE rating SET status_id = 2 WHERE entity_type = %s AND entity_id = %s"
        )
        return self.db.execute_query_dict(query, (entity_type, entity_id))
