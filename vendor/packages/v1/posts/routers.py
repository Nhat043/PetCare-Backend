from chalice import Response
from pydantic import ValidationError
import base64
from packages.v1.posts.service import PostService
from packages.v1.posts.schemas import (
    PostBaseSchema,
    PostResponseSchema,
    PostSingleResponseSchema,
    PostCreateSchema,
    PostImageSchema,
    serialize_post,
)


def posts_routers(app, prefix, cors=None):
    @app.route(prefix, methods=["GET"], cors=cors)
    def get_posts():
        # Get query parameters
        user_id = app.current_request.query_params.get("user_id")
        category_id = app.current_request.query_params.get("category_id")
        status_id = app.current_request.query_params.get("status_id")
        title = app.current_request.query_params.get("title")
        tag_id = app.current_request.query_params.get("tag_id")
        page = int(app.current_request.query_params.get("page", 1))
        limit = int(app.current_request.query_params.get("limit", 10))

        # Convert to integers if provided
        if user_id:
            user_id = int(user_id)
        if category_id:
            category_id = int(category_id)
        if status_id:
            status_id = int(status_id)
        if tag_id:
            try:
                tag_id = int(tag_id)
            except ValueError:
                return Response(
                    body={"error": "Invalid tag_id parameter"}, status_code=400
                )
        post_service = PostService()
        result = post_service.get_posts(
            user_id=user_id,
            category_id=category_id,
            status_id=status_id,
            title=title,
            tag_id=tag_id,
            page=page,
            limit=limit,
        )

        return Response(
            body={
                "posts": [
                    serialize_post(PostResponseSchema(**post).model_dump())
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
            body={"post": serialize_post(PostResponseSchema(**post).model_dump())}
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

        # @app.route(f"{prefix}/upload-image", methods=["POST"], cors=cors)
        # def upload_file():
        #     """
        #     Handle actual file upload to S3
        #     Expects multipart/form-data with 'image' field
        #     """
        #     post_service = PostService()

        #     # Get the uploaded file
        #     files = app.current_request.files
        #     if not files or "image" not in files:
        #         return Response(body={"error": "No image file provided"}, status_code=400)

        #     image_file = files["image"]
        #     filename = image_file.filename

        #     try:
        #         # Upload to S3
        #         s3_url = post_service.upload_file_to_s3(image_file.read(), filename)

        #         if s3_url is None:
        #             return Response(
        #                 body={"error": "Failed to upload image to S3"}, status_code=500
        #             )

        #         return Response(
        #             body={
        #                 "message": "Image uploaded successfully",
        #                 "s3_url": s3_url,
        #                 "filename": filename,
        #             },
        #             status_code=201,
        #         )

        #     except Exception as e:
        #         return Response(body={"error": f"Upload failed: {str(e)}"}, status_code=500)
        # @app.route(f"{prefix}/image", methods=["POST"], cors=cors)
        # def upload_image():
        #     post_service = PostService()
        #     data = app.current_request.json_body
        #     try:
        #         schema = PostImageSchema(**data)
        #     except ValidationError as e:
        #         return Response(
        #             body={"error": "Invalid input", "details": e.errors()},
        #             status_code=400,
        #         )
        #     image_url = post_service.upload_image(schema.image_url)
        #     print(image_url)
        #     if image_url is None:
        #         return Response(body={"error": "Image upload failed"}, status_code=400)
        #     return Response(body={"image_url": image_url}, status_code=201)

    @app.route(f"{prefix}/upload-base64", methods=["POST"], cors=cors)
    def upload_base64_image():
        """
        Handle base64-encoded image upload to S3
        Expects JSON with 'image_data' and 'filename' fields
        """
        post_service = PostService()

        try:
            data = app.current_request.json_body
            image_data = data.get("image_data")
            filename = data.get("filename", "image.jpg")

            if not image_data:
                return Response(
                    body={"error": "No image data provided"}, status_code=400
                )

            # Decode base64 image
            try:
                image_bytes = base64.b64decode(image_data)
            except Exception as e:
                return Response(
                    body={"error": "Invalid base64 image data"}, status_code=400
                )

            # Upload to S3
            s3_url = post_service.upload_file_to_s3(image_bytes, filename)

            if s3_url is None:
                return Response(
                    body={"error": "Failed to upload image to S3"}, status_code=500
                )

            return Response(
                body={
                    "message": "Image uploaded successfully",
                    "s3_url": s3_url,
                    "filename": filename,
                },
                status_code=201,
            )

        except Exception as e:
            return Response(body={"error": f"Upload failed: {str(e)}"}, status_code=500)
