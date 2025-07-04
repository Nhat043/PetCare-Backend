from packages.v1.auth.repository import AuthRepository
import hashlib


class AuthService:
    def __init__(self):
        self.repo = AuthRepository()

    def get_user(self, email: str):
        return self.repo.get_user(email)

    def get_users(self):
        return self.repo.get_users()

    def login(self, data: dict):
        user = self.repo.get_user(data["email"])
        if not user:
            return None
        password_hash = hash_password_md5(data["password"])
        if not check_password_md5(data["password"], user["password_hash"]):
            print("password_hash", password_hash)
            print("user['password_hash']", user["password_hash"])
            return None
        return user

    def check_duplicate_email(self, email: str):
        return self.repo.get_user(email)

    def create_user(self, data: dict):
        if self.check_duplicate_email(data["email"]):
            return None
        plain_password = data.pop("password")
        data["password_hash"] = hash_password_md5(plain_password)
        return self.repo.create_user(data)

    # def update_user(self, email: str, data: dict):
    #     return self.repo.update_user(email, data)

    # def delete_user(self, email: str):
    #     return self.repo.delete_user(email)


def hash_password_md5(plain_password: str) -> str:
    return hashlib.md5(plain_password.encode("utf-8")).hexdigest()


def check_password_md5(plain_password: str, stored_hash: str) -> bool:
    return hash_password_md5(plain_password) == stored_hash
