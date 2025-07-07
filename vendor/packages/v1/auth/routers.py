from chalice import Response
from packages.v1.auth.service import AuthService
from packages.v1.auth.schemas import (
    LoginSchema,
    UserCreateSchema,
    UserResponseSchema,
    serialize_user,
)
from pydantic import ValidationError


def auth_routers(app, prefix, cors=None):
    @app.route(prefix, methods=["GET"], cors=cors)
    def get_users():
        auth_service = AuthService()
        request = app.current_request
        # Get query params with defaults
        page = int(request.query_params.get("page", 1)) if request.query_params else 1
        limit = (
            int(request.query_params.get("limit", 10)) if request.query_params else 10
        )
        role_id = request.query_params.get("role_id") if request.query_params else None
        status_id = (
            request.query_params.get("status_id") if request.query_params else None
        )
        email = request.query_params.get("email") if request.query_params else None

        users_data = auth_service.get_users(
            page=page, limit=limit, role_id=role_id, status_id=status_id, email=email
        )
        return Response(body=users_data)

    @app.route(f"{prefix}/email/{{email}}", methods=["GET"], cors=cors)
    def get_user_by_email(email):
        auth_service = AuthService()
        user = auth_service.get_user_by_email(email)
        return Response(body={"user": serialize_user(user)})

    @app.route(f"{prefix}/id/{{user_id}}", methods=["GET"], cors=cors)
    def get_user_by_id(user_id):
        auth_service = AuthService()
        user = auth_service.get_user_by_id(user_id)
        return Response(body={"user": serialize_user(user)})

    @app.route(f"{prefix}/login", methods=["POST"], cors=cors)
    def login():
        auth_service = AuthService()
        data = app.current_request.json_body
        try:
            schema = LoginSchema(**data)
        except ValidationError as e:
            return Response(
                body={"error": "Invalid input", "details": e.errors()}, status_code=400
            )
        user = auth_service.login(schema.model_dump())
        if not user:
            return Response(body={"error": "Invalid credentials"}, status_code=401)
        else:
            return Response(
                body={
                    "message": "Login successful",
                    "user_id": user["user_id"],
                    "full_name": user["full_name"],
                    "role_id": user["role_id"],
                }
            )

    @app.route(f"{prefix}", methods=["POST"], cors=cors)
    def create_user():
        auth_service = AuthService()
        data = app.current_request.json_body
        try:
            schema = UserCreateSchema(**data)
        except ValidationError as e:
            return Response(
                body={"error": "Invalid input", "details": e.errors()}, status_code=400
            )
        user = auth_service.create_user(schema.model_dump())
        if not user:
            return Response(body={"error": "Email already exists"}, status_code=400)
        return Response(body={"user": serialize_user(user)})
