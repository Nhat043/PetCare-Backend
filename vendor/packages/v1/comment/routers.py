from packages.v1.comment.service import CommentService
from packages.v1.comment.schemas import (
    serialize_comment,
    CommentBaseSchema,
    CommentCreateSchema,
)
from chalice import Response
from pydantic import ValidationError


def comment_routers(app, prefix, cors=None):
    @app.route(f"{prefix}", methods=["GET"], cors=cors)
    def get_comment():
        query_params = app.current_request.query_params or {}
        page = int(query_params.get("page", 1))
        limit = int(query_params.get("limit", 10))
        comment_service = CommentService()
        result = comment_service.get_comment(page, limit)
        if not result["comments"]:
            return Response(body={"message": "No comment found"}, status_code=200)
        return Response(
            body={
                "comments": [
                    serialize_comment(CommentBaseSchema(**comment))
                    for comment in result["comments"]
                ],
                "total": result["total"],
                "total_pages": result["total_pages"],
                "has_next": result["has_next"],
                "has_prev": result["has_prev"],
            },
            status_code=200,
        )

    @app.route(f"{prefix}/{{entity_type}}/{{entity_id}}", methods=["GET"], cors=cors)
    def get_comment_by_entity_id(entity_type, entity_id):
        query_params = app.current_request.query_params or {}
        page = int(query_params.get("page", 1))
        limit = int(query_params.get("limit", 10))
        comment_service = CommentService()
        result = comment_service.get_comment_by_entity_id(
            entity_type, entity_id, page, limit
        )
        print(result)
        if not result["comments"]:
            return Response(body={"message": "No comment found"}, status_code=200)
        return Response(
            body={
                "comments": [
                    serialize_comment(CommentBaseSchema(**comment))
                    for comment in result["comments"]
                ],
                "total": result["total"],
                "total_pages": result["total_pages"],
                "has_next": result["has_next"],
                "has_prev": result["has_prev"],
            },
            status_code=200,
        )

    @app.route(f"{prefix}/user/{{user_id}}/{{entity_type}}", methods=["GET"], cors=cors)
    def get_comment_by_user_id(entity_type, user_id):
        query_params = app.current_request.query_params or {}
        page = int(query_params.get("page", 1))
        limit = int(query_params.get("limit", 10))
        comment_service = CommentService()
        result = comment_service.get_comment_by_user_id(
            entity_type, user_id, page, limit
        )
        if not result["comments"]:
            return Response(body={"message": "No comment found"}, status_code=200)
        return Response(
            body={
                "comments": [
                    serialize_comment(CommentBaseSchema(**comment))
                    for comment in result["comments"]
                ],
                "total": result["total"],
                "total_pages": result["total_pages"],
                "has_next": result["has_next"],
                "has_prev": result["has_prev"],
            },
            status_code=200,
        )

    @app.route(f"{prefix}", methods=["POST"], cors=cors)
    def create_comment():
        data = app.current_request.json_body
        try:
            schema = CommentCreateSchema(**data)
        except ValidationError as e:
            return Response(
                body={"error": "Invalid input", "details": e.errors()}, status_code=400
            )
        comment_service = CommentService()
        result = comment_service.create_comment(schema.model_dump())
        return Response(body={"comment_id": result}, status_code=201)

    @app.route(f"{prefix}/{{entity_type}}/{{entity_id}}", methods=["DELETE"], cors=cors)
    def delete_comment_by_entity_id(entity_type, entity_id):
        comment_service = CommentService()
        comment_service.delete_comment_by_entity_id(entity_type, entity_id)
        return Response(
            body={"message": "Comment deleted successfully"}, status_code=204
        )
