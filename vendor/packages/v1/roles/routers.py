from chalice import Response
from packages.v1.roles.service import RoleService


def roles_routers(app, prefix, cors=None):
    @app.route(prefix, methods=["GET"], cors=cors)
    def get_roles():
        role_service = RoleService()
        roles = role_service.get_roles()
        return Response(body={"role": roles})
