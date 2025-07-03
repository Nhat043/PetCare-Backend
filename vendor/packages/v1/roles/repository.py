from packages.core.database.postgresql import execute_query_dict


class RoleRepository:
    def get_roles(self):
        roles = execute_query_dict("SELECT * FROM roles")
        return roles
