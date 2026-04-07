# services/auth_service.py

import hashlib
from repositories.user_repo import UserRepository
from models.user import User


class AuthService:

    def __init__(self):
        self.user_repo = UserRepository()

    # 🔐 Хешування пароля
    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    # 🆕 Реєстрація користувача
    def register(self, username: str, password: str, role_id: int) -> User:

        password_hash = self._hash_password(password)
        user_id = self.user_repo.add(username, password_hash, role_id)

        # Після створення дістаємо повного користувача (з роллю)
        return self.user_repo.get_by_username(username)

    # 🔑 Логін
    def login(self, username: str, password: str) -> User | None:

        user = self.user_repo.get_by_username(username)

        if not user:
            return None

        if user.password_hash == self._hash_password(password):
            return user

        return None

    # 🔄 Зміна пароля
    def change_password(self, user_id: int, new_password: str):

        password_hash = self._hash_password(new_password)
        self.user_repo.update_password(user_id, password_hash)