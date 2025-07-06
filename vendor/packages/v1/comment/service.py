from packages.v1.comment.repository import CommentRepository


class CommentService:
    def __init__(self):
        self.repo = CommentRepository()

    def get_comment(self, page: int = 1, limit: int = 10):
        return self.repo.get_comment_paginated(page, limit)

    def get_comment_by_entity_id(
        self, entity_type: str, entity_id: int, page: int = 1, limit: int = 10
    ):
        return self.repo.get_comment_by_entity_id_paginated(
            entity_type, entity_id, page, limit
        )

    def get_comment_by_user_id(
        self, entity_type: str, user_id: int, page: int = 1, limit: int = 10
    ):
        return self.repo.get_comment_by_user_id_paginated(
            entity_type, user_id, page, limit
        )

    def create_comment(self, comment: dict):
        return self.repo.create_comment(comment)

    def delete_comment_by_entity_id(self, entity_type: str, entity_id: int):
        return self.repo.delete_comment_by_entity_id(entity_type, entity_id)
