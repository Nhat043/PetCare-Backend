from chalice import Response
from packages.v1.products.service import ProductService
from packages.v1.products.schemas import (
    ProductCreateSchema,
    ProductResponseSchema,
    serialize_product,
)
from pydantic import ValidationError
import base64


def products_routers(app, prefix, cors=None):
    @app.route(prefix, methods=["GET"], cors=cors)
    def get_products():
        # Get pagination parameters from query string
        page = int(app.current_request.query_params.get("page", 1))
        limit = int(app.current_request.query_params.get("limit", 10))

        # Get filter parameters from query string
        name = app.current_request.query_params.get("name")
        category_id = app.current_request.query_params.get("category_id")
        status_id = app.current_request.query_params.get("status_id")
        tag_id = app.current_request.query_params.get("tag_id")
        min_price = app.current_request.query_params.get("min_price")
        max_price = app.current_request.query_params.get("max_price")

        # Validate pagination parameters
        if page < 1:
            page = 1
        if limit < 1 or limit > 100:  # Set reasonable limits
            limit = 10

        # Convert filter parameters to appropriate types
        if category_id:
            try:
                category_id = int(category_id)
            except ValueError:
                return Response(
                    body={"error": "Invalid category_id parameter"}, status_code=400
                )

        if status_id:
            try:
                status_id = int(status_id)
            except ValueError:
                return Response(
                    body={"error": "Invalid status_id parameter"}, status_code=400
                )

        if min_price:
            try:
                min_price = float(min_price)
            except ValueError:
                return Response(
                    body={"error": "Invalid min_price parameter"}, status_code=400
                )

        if max_price:
            try:
                max_price = float(max_price)
            except ValueError:
                return Response(
                    body={"error": "Invalid max_price parameter"}, status_code=400
                )

        if tag_id:
            try:
                tag_id = int(tag_id)
            except ValueError:
                return Response(
                    body={"error": "Invalid tag_id parameter"}, status_code=400
                )

        product_service = ProductService()
        result = product_service.get_products_paginated(
            page=page,
            limit=limit,
            name=name,
            category_id=category_id,
            status_id=status_id,
            min_price=min_price,
            max_price=max_price,
            tag_id=tag_id,
        )

        return Response(
            body={
                "products": [
                    serialize_product(ProductResponseSchema(**product).model_dump())
                    for product in result["products"]
                ],
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total": result["total"],
                    "total_pages": result["total_pages"],
                    "has_next": result["has_next"],
                    "has_prev": result["has_prev"],
                },
                "filters": result["filters"],
            }
        )

    @app.route(f"{prefix}/{{product_id}}", methods=["GET"], cors=cors)
    def get_product(product_id):
        product_service = ProductService()
        product = product_service.get_product(product_id)
        if product is None:
            return Response(status_code=404, body={"error": "Product not found"})
        return Response(
            body={
                "product": serialize_product(
                    ProductResponseSchema(**product).model_dump()
                )
            }
        )

    @app.route(f"{prefix}", methods=["POST"], cors=cors)
    def create_product():
        product_service = ProductService()
        data = app.current_request.json_body
        try:
            schema = ProductCreateSchema(**data)
        except ValidationError as e:
            return Response(
                body={"error": "Invalid input", "details": e.errors()}, status_code=400
            )
        product = product_service.create_product(schema.model_dump())
        if product is None:
            return Response(body={"error": "Product created failed"}, status_code=400)
        return Response(body={"product_id": product}, status_code=201)

    @app.route(f"{prefix}/upload-base64", methods=["POST"], cors=cors)
    def upload_base64_image():
        """
        Handle base64-encoded image upload to S3
        Expects JSON with 'image_data' and 'filename' fields
        """
        product_service = ProductService()

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
            s3_url = product_service.upload_file_to_s3(image_bytes, filename)

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

    @app.route(f"{prefix}/{{product_id}}", methods=["DELETE"], cors=cors)
    def delete_product(product_id):
        product_service = ProductService()
        product = product_service.delete_product(product_id)
        if product is None:
            return Response(status_code=404, body={"error": "Product not found"})
        return Response(
            status_code=204, body={"message": "Product deleted successfully"}
        )
