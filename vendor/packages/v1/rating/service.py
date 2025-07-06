from packages.v1.rating.repository import RatingRepository


class RatingService:
    def __init__(self):
        self.repo = RatingRepository()

    def get_rating(self, page: int = 1, limit: int = 10):
        return self.repo.get_rating(page, limit)

    def get_rating_by_entity_id(self, entity_type: str, entity_id: int):
        return self.repo.get_rating_by_entity_id(entity_type, entity_id)

    def get_rating_by_user_id(self, entity_type: str, user_id: int):
        return self.repo.get_rating_by_user_id(entity_type, user_id)

    def get_rating_by_user_id_and_entity_id(
        self, entity_type: str, user_id: int, entity_id: int
    ):
        return self.repo.get_rating_by_user_id_and_entity_id(
            entity_type, user_id, entity_id
        )

    def create_rating(self, rating: dict):
        print(rating)
        existing_rating = self.get_rating_by_user_id_and_entity_id(
            rating["entity_type"], rating["user_id"], rating["entity_id"]
        )
        print(existing_rating)
        if existing_rating:
            # existing_rating is a list, get the first item
            existing_rating_data = existing_rating[0]
            return self.repo.update_rating(
                existing_rating_data["rating_id"], rating["rating"]
            )
        else:
            return self.repo.create_rating(rating)

    def delete_rating_by_entity_id(self, entity_type: str, entity_id: int):
        return self.repo.delete_rating_by_entity_id(entity_type, entity_id)
