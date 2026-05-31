from pathlib import Path
import sys

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / 'app'))

from app.core.exceptions import NotFoundException, ValidationException
from app.services.user_service import UserService


class FakeUser:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class FakeRepository:
    def __init__(self):
        self.user_by_id = {}
        self.user_by_username = {}
        self.user_by_email = {}
        self.create_called_with = None
        self.update_called_with = None
        self.delete_called_with = None

    def get_by_username(self, username):
        return self.user_by_username.get(username)

    def get_by_email(self, email):
        return self.user_by_email.get(email)

    def create(self, user):
        self.create_called_with = user
        return user

    def get_all(self):
        return list(self.user_by_id.values())

    def get_by_id(self, user_id):
        return self.user_by_id.get(user_id)

    def update(self, user_id, data):
        self.update_called_with = (user_id, data)
        return data

    def delete(self, user_id):
        self.delete_called_with = user_id

    def get_by_username_or_email(self, identifier):
        return self.user_by_username.get(identifier) or self.user_by_email.get(identifier)


@pytest.fixture
def repo():
    return FakeRepository()


@pytest.fixture
def service(repo):
    return UserService(repo)


def test_create_user_deve_falhar_sem_username_ou_senha(service):
    with pytest.raises(ValidationException, match='Username e senha sao obrigatorios'):
        service.create_user({'senha': 'x'})

    with pytest.raises(ValidationException, match='Username e senha sao obrigatorios'):
        service.create_user({'username': 'usuario'})


def test_create_user_deve_falhar_quando_username_ja_existe(service, repo):
    repo.user_by_username['jaexiste'] = FakeUser(id=1)

    with pytest.raises(ValidationException, match='Username ja cadastrado'):
        service.create_user({'username': 'jaexiste', 'senha': '123'})


def test_create_user_deve_falhar_quando_email_ja_existe(service, repo):
    repo.user_by_email['dup@test.com'] = FakeUser(id=1)

    with pytest.raises(ValidationException, match='Email ja cadastrado'):
        service.create_user(
            {'username': 'novo_usuario', 'senha': '123', 'email': 'dup@test.com'}
        )


def test_create_user_deve_gerar_hash_e_salt(service, repo):
    created = service.create_user(
        {
            'perfil_id': 2,
            'username': 'novo',
            'senha': 'segredo',
            'nome': 'Nome',
            'email': 'novo@test.com',
        }
    )

    assert repo.create_called_with is not None
    assert created.username == 'novo'
    assert created.senha != 'segredo'
    assert created.salt
    assert len(created.salt) == 32
    assert created.data_criacao is not None


def test_get_user_by_id_deve_retornar_usuario(service, repo):
    repo.user_by_id[10] = FakeUser(id=10, username='u10')

    user = service.get_user_by_id(10)

    assert user.id == 10


def test_get_user_by_id_deve_lancar_not_found(service):
    with pytest.raises(NotFoundException, match='User with id 999 not found'):
        service.get_user_by_id(999)


def test_update_user_deve_lancar_not_found_quando_usuario_nao_existe(service):
    with pytest.raises(NotFoundException, match='User with id 123 not found'):
        service.update_user(123, {'nome': 'Atualizado'})


def test_update_user_deve_hash_senha_quando_enviada(service, repo):
    repo.user_by_id[1] = FakeUser(id=1, username='user1')

    updated = service.update_user(1, {'senha': 'nova_senha'})
    user_id, payload = repo.update_called_with

    assert updated is payload
    assert user_id == 1
    assert payload['senha'] != 'nova_senha'
    assert payload['salt']
    assert payload['data_alteracao'] is not None


def test_update_user_sem_senha_nao_deve_criar_salt(service, repo):
    repo.user_by_id[2] = FakeUser(id=2, username='user2')

    service.update_user(2, {'nome': 'Nome 2'})
    _, payload = repo.update_called_with

    assert 'salt' not in payload
    assert payload['nome'] == 'Nome 2'
    assert payload['data_alteracao'] is not None


def test_delete_user_deve_lancar_not_found(service):
    with pytest.raises(NotFoundException, match='User with id 55 not found'):
        service.delete_user(55)


def test_delete_user_deve_chamar_repositorio(service, repo):
    repo.user_by_id[5] = FakeUser(id=5, username='user5')

    service.delete_user(5)

    assert repo.delete_called_with == 5


def test_authenticate_user_retorna_none_para_credenciais_vazias(service):
    assert service.authenticate_user('', '123') is None
    assert service.authenticate_user('user', '') is None


def test_authenticate_user_retorna_none_quando_usuario_nao_existe(service):
    assert service.authenticate_user('nao_existe', '123') is None


def test_authenticate_user_retorna_usuario_quando_senha_confere(service, repo):
    created = service.create_user(
        {
            'username': 'autenticavel',
            'senha': 'senha_correta',
            'nome': 'Auth',
            'email': 'auth@test.com',
        }
    )
    repo.user_by_username['autenticavel'] = created

    authenticated = service.authenticate_user('autenticavel', 'senha_correta')

    assert authenticated is created


def test_authenticate_user_retorna_none_quando_senha_errada(service, repo):
    created = service.create_user(
        {
            'username': 'autenticavel2',
            'senha': 'senha_correta',
            'nome': 'Auth2',
            'email': 'auth2@test.com',
        }
    )
    repo.user_by_username['autenticavel2'] = created

    authenticated = service.authenticate_user('autenticavel2', 'senha_errada')

    assert authenticated is None