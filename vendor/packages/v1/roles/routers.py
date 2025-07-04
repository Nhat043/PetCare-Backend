from chalice import Response
from packages.v1.roles.service import RoleService
from chalice import BadRequestError, NotFoundError
from packages.v1.roles.schemas import RoleBaseSchema, RoleCreateSchema, RoleUpdateSchema
from pydantic import ValidationError


def roles_routers(app, prefix, cors=None):
    @app.route(prefix, methods=["GET"], cors=cors)
    def get_roles():
        role_service = RoleService()
        roles = role_service.get_roles()
        return Response(
            body={"roles": [RoleBaseSchema(**role).model_dump() for role in roles]}
        )

    @app.route(f"{prefix}/{{role_id}}", methods=["GET"], cors=cors)
    def get_role(role_id):
        role_service = RoleService()
        role = role_service.get_role(int(role_id))
        return Response(body={"role": RoleBaseSchema(**role).model_dump()})

    @app.route(f"{prefix}", methods=["POST"], cors=cors)
    def create_role():
        role_service = RoleService()
        data = app.current_request.json_body
        try:
            schema = RoleCreateSchema(**data)
        except ValidationError as e:
            return Response(
                body={"error": "Invalid input", "details": e.errors()}, status_code=400
            )
        role = role_service.create_role(schema)
        return Response(body={"role": RoleBaseSchema(**role).model_dump()})

    @app.route(f"{prefix}/{{role_id}}", methods=["PUT"], cors=cors)
    def update_role(role_id):
        role_service = RoleService()
        data = app.current_request.json_body
        try:
            schema = RoleUpdateSchema(**data)
        except ValidationError as e:
            return Response(
                body={"error": "Invalid input", "details": e.errors()}, status_code=400
            )
        updated = role_service.update_role(int(role_id), schema)
        if not updated:
            return Response(
                body={"error": "Role not found or not updated"}, status_code=404
            )
        else:
            return Response(body={"message": "Role updated"})

    @app.route(f"{prefix}/{{role_id}}", methods=["DELETE"], cors=cors)
    def delete_role(role_id):
        role_service = RoleService()
        deleted = role_service.delete_role(int(role_id))
        if deleted:
            return Response(body={"message": "Role deleted"})
        else:
            raise NotFoundError("Role not found")
