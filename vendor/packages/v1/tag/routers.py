from packages.v1.tag.service import TagService
from packages.v1.tag.schemas import TagBaseSchema, TagCreateSchema
from chalice import Response
from pydantic import ValidationError


def tag_routers(app, prefix, cors=None):
    @app.route(prefix, methods=["GET"], cors=cors)
    def get_tags():
        tag_service = TagService()
        tags = tag_service.get_tags()
        return Response(
            body={"tags": [TagBaseSchema(**tag).model_dump() for tag in tags]}
        )

    @app.route(f"{prefix}/{{tag_id}}", methods=["GET"], cors=cors)
    def get_tag(tag_id: int):
        tag_service = TagService()
        tag = tag_service.get_tag(tag_id)
        return Response(body={"tag": TagBaseSchema(**tag).model_dump()})

    @app.route(prefix, methods=["POST"], cors=cors)
    def create_tag():
        tag_service = TagService()
        data = app.current_request.json_body
        try:
            schema = TagCreateSchema(**data)
        except ValidationError as e:
            return Response(
                body={"error": "Invalid input", "details": e.errors()}, status_code=400
            )
        tag_name = schema.tag_name
        tag_id = tag_service.create_tag(tag_name)
        return Response(body={"tag_id": tag_id})

    @app.route(f"{prefix}/{{tag_id}}", methods=["PUT"], cors=cors)
    def update_tag(tag_id: int):
        tag_service = TagService()
        data = app.current_request.json_body
        try:
            schema = TagCreateSchema(**data)
        except ValidationError as e:
            return Response(
                body={"error": "Invalid input", "details": e.errors()}, status_code=400
            )
        tag_name = schema.tag_name
        tag_id = tag_service.update_tag(tag_id, tag_name)
        return Response(body={"tag_id": tag_id})
