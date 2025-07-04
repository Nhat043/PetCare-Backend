from chalice import Response
from pydantic import ValidationError
from packages.v1.posts.service import PostService
from packages.v1.posts.schemas import PostBaseSchema, PostCreateSchema, serialize_post


def posts_routers(app, prefix, cors=None):
    @app.route(prefix, methods=["GET"], cors=cors)
    def get_posts():
        # Get query parameters
        user_id = app.current_request.query_params.get("user_id")
        category_id = app.current_request.query_params.get("category_id")
        status_id = app.current_request.query_params.get("status_id")
        title = app.current_request.query_params.get("title")
        page = int(app.current_request.query_params.get("page", 1))
        limit = int(app.current_request.query_params.get("limit", 10))

        # Convert to integers if provided
        if user_id:
            user_id = int(user_id)
        if category_id:
            category_id = int(category_id)
        if status_id:
            status_id = int(status_id)

        post_service = PostService()
        result = post_service.get_posts(
            user_id=user_id,
            category_id=category_id,
            status_id=status_id,
            title=title,
            page=page,
            limit=limit,
        )

        return Response(
            body={
                "posts": [
                    serialize_post(PostBaseSchema(**post).model_dump())
                    for post in result["posts"]
                ],
                "pagination": {
                    "page": result["page"],
                    "limit": result["limit"],
                    "total": result["total"],
                    "total_pages": result["total_pages"],
                    "has_next": result["has_next"],
                    "has_prev": result["has_prev"],
                },
                "filters": result["filters"],
            }
        )

    @app.route(f"{prefix}/{{post_id}}", methods=["GET"], cors=cors)
    def get_post(post_id):
        post_service = PostService()
        post = post_service.get_post(post_id)
        if post is None:
            return Response(status_code=404, body={"error": "Post not found"})
        return Response(
            body={"post": serialize_post(PostBaseSchema(**post).model_dump())}
        )

    @app.route(f"{prefix}", methods=["POST"], cors=cors)
    def create_post():
        post_service = PostService()
        data = app.current_request.json_body
        try:
            schema = PostCreateSchema(**data)
        except ValidationError as e:
            return Response(
                body={"error": "Invalid input", "details": e.errors()}, status_code=400
            )
        post = post_service.create_post(schema.model_dump())
        if post is None:
            return Response(body={"error": "Post created failed"}, status_code=400)
        else:
            return Response(body={"post_id": post}, status_code=201)

    @app.route(f"{prefix}/{{post_id}}", methods=["DELETE"], cors=cors)
    def delete_post(post_id):
        post_service = PostService()
        post = post_service.delete_post(post_id)
        if post is None:
            return Response(status_code=404, body={"error": "Post not found"})
        return Response(status_code=204, body={"message": "Post deleted successfully"})
