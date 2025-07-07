from packages.core.database.postgresql import Database


class TagRepository:
    def __init__(self):
        self.db = Database()

    def get_tags(self):
        query = "SELECT * FROM tag"
        result = self.db.execute_query_dict(query)
        return result

    def get_tag(self, tag_id: int):
        query = "SELECT * FROM tag WHERE tag_id = %s"
        result = self.db.execute_query_dict(query, (tag_id,))
        return result[0] if result else None

    def create_tag(self, tag_name: str):
        query = "INSERT INTO tag (tag_name) VALUES (%s) RETURNING tag_id"
        result = self.db.execute_query_dict(query, (tag_name,))
        return result[0]["tag_id"] if result else None

    def update_tag(self, tag_id: int, tag_name: str):
        query = "UPDATE tag SET tag_name = %s WHERE tag_id = %s RETURNING tag_id"
        result = self.db.execute_query_dict(query, (tag_name, tag_id))
        return result[0]["tag_id"] if result else None
