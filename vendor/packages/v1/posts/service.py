from .repository import PostRepository


class PostService:
    def __init__(self):
        self.repo = PostRepository()

    def get_posts(
        self,
        user_id: int = None,
        category_id: int = None,
        status_id: int = None,
        title: str = None,
        page: int = 1,
        limit: int = 10,
    ):
        return self.repo.get_posts(user_id, category_id, status_id, title, page, limit)

    def get_post(self, post_id: int):
        return self.repo.get_post(post_id)

    def get_posts_paginated(self, page: int = 1, limit: int = 10):
        return self.repo.get_posts_paginated(page, limit)

    def get_total_posts(self):
        return self.repo.get_total_posts()

    def create_post(self, post: dict):
        return self.repo.create_post(post)

    def update_post(self, post_id: int, post: dict):
        return self.repo.update_post(post_id, post)

    def delete_post(self, post_id: int):
        return self.repo.delete_post(post_id)
