from packages.v1.roles.repository import RoleRepository


class RoleService:
    def get_roles(self):
        role_repository = RoleRepository()
        roles = role_repository.get_roles()
        return roles
