from packages.v1.tag.repository import TagRepository


class TagService:
    def __init__(self):
        self.repo = TagRepository()

    def get_tags(self):
        return self.repo.get_tags()

    def get_tag(self, tag_id: int):
        return self.repo.get_tag(tag_id)

    def create_tag(self, tag_name: str):
        return self.repo.create_tag(tag_name)

    def update_tag(self, tag_id: int, tag_name: str):
        return self.repo.update_tag(tag_id, tag_name)
