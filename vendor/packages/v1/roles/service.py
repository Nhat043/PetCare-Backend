from packages.v1.roles.repository import RoleRepository
from packages.v1.roles.schemas import RoleCreateSchema, RoleUpdateSchema


class RoleService:
    def __init__(self):
        self.repo = RoleRepository()

    def get_roles(self):
        roles = self.repo.get_roles()
        return roles

    def get_role(self, role_id: int):
        role = self.repo.get_role(role_id)
        return role

    def create_role(self, data: RoleCreateSchema):
        role = self.repo.create(data.dict())
        return role

    def update_role(self, role_id: int, data: RoleUpdateSchema):
        # Update the role in the database (pseudo-code, adapt to your repo/ORM)
        # Example: repo.update(role_id, data.dict())
        role = self.repo.get_role(role_id)
        updated = self.repo.update(role_id, data.dict())
        return role

    def delete_role(self, role_id: int):
        # Delete the role in the database (pseudo-code)
        role = self.repo.get_role(role_id)
        deleted = self.repo.delete(role_id)
        return role
