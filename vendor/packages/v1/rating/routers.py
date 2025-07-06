from pydantic import ValidationError
from packages.v1.rating.service import RatingService
from packages.v1.rating.schemas import (
    RatingCreateSchema,
    RatingBaseSchema,
    serialize_rating,
)
from chalice import Response


def rating_routers(app, prefix, cors=None):

    @app.route(f"{prefix}", methods=["GET"], cors=cors)
    def get_rating():
        rating_service = RatingService()
        result = rating_service.get_rating()
        return Response(
            body={
                "rating": [
                    serialize_rating(RatingBaseSchema(**rating)) for rating in result
                ]
            },
            status_code=200,
        )

    @app.route(f"{prefix}/{{entity_type}}/{{entity_id}}", methods=["GET"], cors=cors)
    def get_rating_by_entity_id(entity_type, entity_id):
        rating_service = RatingService()
        result = rating_service.get_rating_by_entity_id(entity_type, entity_id)
        return Response(
            body={
                "rating": [
                    serialize_rating(RatingBaseSchema(**rating)) for rating in result
                ]
            },
            status_code=200,
        )

    @app.route(f"{prefix}/user/{{user_id}}/{{entity_type}}", methods=["GET"], cors=cors)
    def get_rating_by_user_id(entity_type, user_id):
        rating_service = RatingService()
        result = rating_service.get_rating_by_user_id(entity_type, user_id)
        return Response(
            body={
                "rating": [
                    serialize_rating(RatingBaseSchema(**rating)) for rating in result
                ]
            },
            status_code=200,
        )

    @app.route(f"{prefix}", methods=["POST"], cors=cors)
    def create_rating():
        data = app.current_request.json_body
        try:
            schema = RatingCreateSchema(**data)
        except ValidationError as e:
            return Response(
                body={"error": "Invalid input", "details": e.errors()}, status_code=400
            )
        rating_service = RatingService()
        result = rating_service.create_rating(schema.model_dump())
        return Response(body={"rating_id": result}, status_code=201)

    @app.route(f"{prefix}/{{entity_type}}/{{entity_id}}", methods=["PUT"], cors=cors)
    def delete_rating_by_entity_id(entity_type, entity_id):
        rating_service = RatingService()
        rating_service.delete_rating_by_entity_id(entity_type, entity_id)
