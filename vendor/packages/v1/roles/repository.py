from packages.core.database.postgresql import Database


class RoleRepository:
    def __init__(self):
        self.db = Database()

    def get_roles(self):
        query = "SELECT * FROM roles"
        result = self.db.execute_query_dict(query)
        return result

    def get_role(self, role_id: int):
        query = "SELECT * FROM roles WHERE role_id = %s"
        result = self.db.execute_query_dict(query, (role_id,))
        return result[0] if result else None

    def create(self, data: dict):
        # Insert
        query = "INSERT INTO roles (role_name) VALUES (%s)"
        self.db.execute_query(query, (data["role_name"],))
        # Fetch the last inserted row (assuming role_name is unique)
        result = self.db.execute_query_dict(
            "SELECT role_id, role_name FROM roles WHERE role_name = %s ORDER BY role_id DESC LIMIT 1",
            (data["role_name"],),
        )
        return result[0] if result else None

    def update(self, role_id: int, data: dict):
        # Check if role exists
        exists = self.db.execute_query_dict(
            "SELECT role_id, role_name FROM roles WHERE role_id = %s", (role_id,)
        )
        if not exists:
            return None
        # Try to update
        query = "UPDATE roles SET role_name = %s WHERE role_id = %s RETURNING role_id, role_name"
        result = self.db.execute_query_dict(query, (data["role_name"], role_id))
        # If nothing updated, return the original
        return result[0] if result else exists[0]

    def delete(self, role_id: int):
        query = "DELETE FROM roles WHERE role_id = %s RETURNING role_id"
        result = self.db.execute_query_dict(query, (role_id,))
        print("DEBUG: result from delete:", result)
        return result[0] if result else None
