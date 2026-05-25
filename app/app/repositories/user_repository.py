from abc import ABC, abstractmethod
from typing import List
from app.models import Usuario

class UserRepository(ABC):
    @abstractmethod
    def create(self, user: Usuario) -> Usuario:
        pass

    @abstractmethod
    def get_all(self) -> List[Usuario]:
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> Usuario:
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> Usuario:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Usuario:
        pass

    @abstractmethod
    def get_by_username_or_email(self, identifier: str) -> Usuario:
        pass

    @abstractmethod
    def update(self, user_id: int, data: dict) -> Usuario:
        pass

    @abstractmethod
    def delete(self, user_id: int) -> None:
        pass

from app import db

class SQLAlchemyUserRepository(UserRepository):
    def create(self, user: Usuario):
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
        return db.session.get(Usuario, user_id)

    def get_by_username(self, username: str):
        return Usuario.query.filter_by(username=username).first()

    def get_by_email(self, email: str):
        return Usuario.query.filter_by(email=email).first()

    def get_by_username_or_email(self, identifier: str):
        return Usuario.query.filter(
            (Usuario.username == identifier) | (Usuario.email == identifier)
        ).first()

    def update(self, user_id, data):
        user = self.get_by_id(user_id)
        if user:
            for key, value in data.items():
                setattr(user, key, value)
            db.session.commit()
        return user