from chalice import Response
from packages.v1.products.service import ProductService
from packages.v1.products.schemas import (
    ProductCreateSchema,
    ProductBaseSchema,
    serialize_product,
)
from pydantic import ValidationError


def products_routers(app, prefix, cors=None):
    @app.route(prefix, methods=["GET"], cors=cors)
    def get_products():
        # Get pagination parameters from query string
        page = int(app.current_request.query_params.get("page", 1))
        limit = int(app.current_request.query_params.get("limit", 10))

        # Validate pagination parameters
        if page < 1:
            page = 1
        if limit < 1 or limit > 100:  # Set reasonable limits
            limit = 10

        product_service = ProductService()
        result = product_service.get_products_paginated(page=page, limit=limit)

        return Response(
            body={
                "products": [
                    serialize_product(ProductBaseSchema(**product).model_dump())
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
                "product": serialize_product(ProductBaseSchema(**product).model_dump())
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

    @app.route(f"{prefix}/{{product_id}}", methods=["DELETE"], cors=cors)
    def delete_product(product_id):
        product_service = ProductService()
        product = product_service.delete_product(product_id)
        if product is None:
            return Response(status_code=404, body={"error": "Product not found"})
        return Response(
            status_code=204, body={"message": "Product deleted successfully"}
        )
