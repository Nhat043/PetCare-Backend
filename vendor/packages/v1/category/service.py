from packages.v1.category.repository import CategoryRepository


class CategoryService:
    def __init__(self):
        self.repo = CategoryRepository()

    def get_categories(self):
        return self.repo.get_categories()

    def get_category(self, category_id: int):
        return self.repo.get_category(category_id)

    def get_category_by_name(self, category_name: str):
        return self.repo.get_category_by_name(category_name)

    def create_category(self, category_data: dict):
        category_name = category_data.get("category_name")
        if not category_name:
            raise ValueError("category_name is required")
        return self.repo.create_category(category_name)

    def update_category(self, category_id: int, category_data: dict):
        category_name = category_data.get("category_name")
        if not category_name:
            raise ValueError("category_name is required")
        return self.repo.update_category(category_id, category_name)

    def delete_category(self, category_id: int):
        return self.repo.delete_category(category_id)
