from app.repositories.user_repository import UserRepository
from app.core.exceptions import NotFoundException, ValidationException
from app.models import Usuario
from app import bcrypt
from datetime import UTC, datetime
import secrets

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, data: dict) -> Usuario:
        username = data.get('username')
        senha = data.get('senha')

        if not username or not senha:
            raise ValidationException('Username e senha sao obrigatorios.')

        if self.repository.get_by_username(username):
            raise ValidationException('Username ja cadastrado.')

        email = data.get('email')
        if email and self.repository.get_by_email(email):
            raise ValidationException('Email ja cadastrado.')

        salt = secrets.token_hex(16)
        senha_hash = bcrypt.generate_password_hash(f"{senha}{salt}").decode('utf-8')

        user = Usuario(
            perfil_id=data.get('perfil_id', 1),
            nome=data.get('nome', username),
            sobrenome=data.get('sobrenome'),
            email=email,
            cpf=data.get('cpf'),
            senha=senha_hash,
            salt=salt,
            username=username,
            data_criacao=datetime.now(UTC),
            data_alteracao=None,
            telefone=data.get('telefone'),
        )

        return self.repository.create(user)

    def get_all_users(self):
        return self.repository.get_all()

    def get_user_by_id(self, user_id: int) -> Usuario:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundException(f"User with id {user_id} not found.")
        return user

    def update_user(self, user_id: int, data: dict) -> Usuario:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundException(f"User with id {user_id} not found.")

        update_data = dict(data)
        if 'senha' in update_data and update_data['senha']:
            salt = secrets.token_hex(16)
            update_data['senha'] = bcrypt.generate_password_hash(
                f"{update_data['senha']}{salt}"
            ).decode('utf-8')
            update_data['salt'] = salt

        update_data['data_alteracao'] = datetime.now(UTC)
        return self.repository.update(user_id, update_data)

    def delete_user(self, user_id: int):
        user = self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundException(f"User with id {user_id} not found.")
        self.repository.delete(user_id)

    def authenticate_user(self, identifier: str, senha: str):
        if not identifier or not senha:
            return None

        user = self.repository.get_by_username_or_email(identifier)
        if not user:
            return None

        if bcrypt.check_password_hash(user.senha, f"{senha}{user.salt}"):
            return user

        return None