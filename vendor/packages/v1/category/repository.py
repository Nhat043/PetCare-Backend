from packages.core.database.postgresql import Database


class CategoryRepository:
    def __init__(self):
        self.db = Database()

    def get_categories(self):
        query = "SELECT * FROM category"
        return self.db.execute_query_dict(query)

    def get_category(self, category_id: int):
        query = "SELECT * FROM category WHERE category_id = %s"
        return self.db.execute_query_dict(query, (category_id,))

    def get_category_by_name(self, category_name: str):
        query = "SELECT * FROM category WHERE category_name = %s"
        return self.db.execute_query_dict(query, (category_name,))

    def create_category(self, category_name: str):
        query = "INSERT INTO category (category_name) VALUES (%s)"
        result = self.db.execute_query_dict_returning(query, (category_name,))
        return result[0]["category_id"] if result else None

    def update_category(self, category_id: int, category_name: str):
        query = "UPDATE category SET category_name = %s WHERE category_id = %s"
        return self.db.execute_query_dict(query, (category_name, category_id))

    def delete_category(self, category_id: int):
        query = "DELETE FROM category WHERE category_id = %s"
        return self.db.execute_query_dict(query, (category_id,))

    def get_total_categories(self):
        query = "SELECT COUNT(*) as total FROM category"
        return self.db.execute_query_dict(query)
