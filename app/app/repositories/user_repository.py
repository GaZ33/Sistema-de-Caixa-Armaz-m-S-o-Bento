from abc import ABC, abstractmethod
from typing import List
from app.domain.user import User

class UserRepository(ABC):
    @abstractmethod
    def create(self, user: User) -> User:
        pass

    @abstractmethod
    def get_all(self) -> List[User]:
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> User:
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        pass

    @abstractmethod
    def delete(self, user_id: int) -> None:
        pass

from app.models import Usuario  
from app import db

class SQLAlchemyUserRepository(UserRepository):
    def create(self, user):
        db.session.add(user)
        db.session.commit()
        return user

    def delete(self, user_id):
        user = self.get_by_id(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()

    def get_all(self):
        return Usuario.query.all()

    def get_by_id(self, user_id):
        return Usuario.query.get(user_id)

    def update(self, user_id, data):
        user = self.get_by_id(user_id)
        if user:
            for key, value in data.items():
                setattr(user, key, value)
            db.session.commit()
        return user