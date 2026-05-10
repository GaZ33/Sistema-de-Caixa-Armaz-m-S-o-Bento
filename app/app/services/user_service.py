from app.repositories.user_repository import UserRepository
from app.domain.user import User
from app.core.exceptions import NotFoundException

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, user: User) -> User:
        return self.repository.create(user)

    def get_all_users(self):
        return self.repository.get_all()

    def get_user_by_id(self, user_id: int) -> User:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundException(f"User with id {user_id} not found.")
        return user

    def update_user(self, user: User) -> User:
        return self.repository.update(user)

    def delete_user(self, user_id: int):
        self.repository.delete(user_id)