from packages.v1.category.service import CategoryService
from packages.v1.category.schemas import CategoryCreateSchema, CategoryUpdateSchema
from chalice import Response
from pydantic import ValidationError


def category_routers(app, prefix, cors=None):

    @app.route(f"{prefix}", methods=["GET"], cors=cors)
    def get_categories():
        category_service = CategoryService()
        result = category_service.get_categories()
        return Response(body={"categories": result}, status_code=200)

    @app.route(f"{prefix}/{{category_id}}", methods=["GET"], cors=cors)
    def get_category(category_id):
        category_service = CategoryService()
        result = category_service.get_category(category_id)
        return Response(body={"category": result}, status_code=200)

    @app.route(f"{prefix}/name/{{category_name}}", methods=["GET"], cors=cors)
    def get_category_by_name(category_name):
        category_service = CategoryService()
        result = category_service.get_category_by_name(category_name)
        return Response(body={"category": result}, status_code=200)

    @app.route(f"{prefix}", methods=["POST"], cors=cors)
    def create_category():
        category_service = CategoryService()
        data = app.current_request.json_body
        try:
            schema = CategoryCreateSchema(**data)
        except ValidationError as e:
            return Response(
                body={"error": "Invalid input", "details": e.errors()}, status_code=400
            )
        result = category_service.create_category(schema.model_dump())
        return Response(body={"category_id": result}, status_code=201)

    @app.route(f"{prefix}/{{category_id}}", methods=["PUT"], cors=cors)
    def update_category(category_id):
        category_service = CategoryService()
        data = app.current_request.json_body
        try:
            schema = CategoryUpdateSchema(**data)
        except ValidationError as e:
            return Response(
                body={"error": "Invalid input", "details": e.errors()}, status_code=400
            )
        result = category_service.update_category(category_id, schema.model_dump())
        return Response(body={"category": result}, status_code=200)

    # @app.route(f"{prefix}/{{category_id}}", methods=["DELETE"], cors=cors)
    # def delete_category(category_id):
    #     return category_service.delete_category(category_id)
