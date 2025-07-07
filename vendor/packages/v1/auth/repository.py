from packages.core.database.postgresql import Database


class AuthRepository:
    def __init__(self):
        self.db = Database()

    def get_users(self):
        query = "SELECT * FROM users"
        result = self.db.execute_query_dict(query)
        return result

    def get_user(self, user_id: int = None, email: str = None):
        if user_id:
            query = "SELECT * FROM users WHERE user_id = %s"
            result = self.db.execute_query_dict(query, (user_id,))
        elif email:
            query = "SELECT * FROM users WHERE email = %s"
            result = self.db.execute_query_dict(query, (email,))
        else:
            return None
        return result[0] if result else None

    def create_user(self, data: dict):
        query = "INSERT INTO users (email, password_hash, full_name, avatar_url, bio, role_id, status_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        self.db.execute_query(
            query,
            (
                data["email"],
                data["password_hash"],
                data["full_name"],
                data["avatar_url"],
                data["bio"],
                data["role_id"],
                data["status_id"],
            ),
        )
        result = self.db.execute_query_dict(
            "SELECT user_id, email, password_hash, full_name, avatar_url, bio, role_id, created_at, updated_at FROM users WHERE email = %s",
            (data["email"],),
        )
        return result[0] if result else None
