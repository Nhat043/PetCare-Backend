from chalice import Response
from packages.v1.auth.service import AuthService
from packages.v1.auth.schemas import LoginSchema, UserCreateSchema, serialize_user
from pydantic import ValidationError


def auth_routers(app, prefix, cors=None):
    @app.route(prefix, methods=["GET"], cors=cors)
    def get_users():
        auth_service = AuthService()
        users = auth_service.get_users()
        return Response(body={"users": [serialize_user(user) for user in users]})

    @app.route(f"{prefix}/{{email}}", methods=["GET"], cors=cors)
    def get_user(email):
        auth_service = AuthService()
        user = auth_service.get_user(email)
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
            return Response(body={"message": "Login successful"})

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
