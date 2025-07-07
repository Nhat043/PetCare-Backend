from packages.core.database.postgresql import Database


class AuthRepository:
    def __init__(self):
        self.db = Database()

    def get_users(self, page=1, limit=10, role_id=None, status_id=None, email=None):
        where_conditions = []
        params = []

        if role_id:
            where_conditions.append("u.role_id = %s")
            params.append(role_id)
        if status_id:
            where_conditions.append("u.status_id = %s")
            params.append(status_id)
        if email:
            where_conditions.append("u.email ILIKE %s")
            params.append(f"%{email}%")

        where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"

        # Count total users
        count_query = f"SELECT COUNT(*) FROM users u WHERE {where_clause}"
        total_result = self.db.execute_query_dict(count_query, tuple(params))
        total = total_result[0]["count"] if total_result else 0

        offset = (page - 1) * limit
        total_pages = (total + limit - 1) // limit
        has_next = page < total_pages
        has_prev = page > 1

        query = f"""SELECT u.*, r.role_name, s.status_name
            FROM users u
            LEFT JOIN roles r ON u.role_id = r.role_id
            LEFT JOIN statuses s ON u.status_id = s.status_id
            WHERE {where_clause}
            ORDER BY u.created_at DESC
            LIMIT %s OFFSET %s
        """
        params.extend([limit, offset])
        users = self.db.execute_query_dict(query, tuple(params))

        return {
            "users": users,
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": total_pages,
            "has_next": has_next,
            "has_prev": has_prev,
            "filters": {
                "role_id": role_id,
                "status_id": status_id,
                "email": email,
            },
        }

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
