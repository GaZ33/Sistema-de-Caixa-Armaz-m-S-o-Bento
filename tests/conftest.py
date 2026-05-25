import os
import sys
from datetime import UTC, datetime
from pathlib import Path

import pytest
from sqlalchemy import text

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / 'app'))

from app import app, bcrypt, db
from app.models import (
    AvisosEstoque,
    Conta,
    Estoque,
    LogAlteracoes,
    LogEstoque,
    LogPagamento,
    Modulo,
    Perfil,
    PerfilAcessos,
    Produto,
    ProdutoConta,
    Usuario,
)


def _assert_test_db_configured():
    if not os.getenv('DB_CONNECTION_TEST'):
        pytest.skip('Defina DB_CONNECTION_TEST com um banco MySQL de testes para executar a suite.')


MODELS_FOR_CLEANUP = [
    PerfilAcessos,
    AvisosEstoque,
    LogEstoque,
    ProdutoConta,
    LogPagamento,
    LogAlteracoes,
    Estoque,
    Conta,
    Produto,
    Usuario,
    Modulo,
    Perfil,
]


@pytest.fixture(scope='session', autouse=True)
def testing_database_ready():
    _assert_test_db_configured()

    app.config.update(
        TESTING=True,
        SECRET_KEY='test-secret-key',
    )

    with app.app_context():
        db.create_all()

    yield


@pytest.fixture(autouse=True)
def app_context(testing_database_ready):
    with app.app_context():
        yield


@pytest.fixture(autouse=True)
def clean_database(app_context):
    is_mysql = db.engine.dialect.name.startswith('mysql')

    if is_mysql:
        db.session.execute(text('SET FOREIGN_KEY_CHECKS = 0'))

    for model in MODELS_FOR_CLEANUP:
        db.session.query(model).delete()

    if is_mysql:
        db.session.execute(text('SET FOREIGN_KEY_CHECKS = 1'))

    db.session.commit()

    yield


@pytest.fixture()
def client(testing_database_ready):
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture()
def perfil_admin():
    perfil = Perfil(nome='Administrador', data_criacao=datetime.now(UTC))
    db.session.add(perfil)
    db.session.commit()
    return perfil


@pytest.fixture()
def auth_user(perfil_admin):
    salt = 'testsalt123'
    senha_hash = bcrypt.generate_password_hash(f"senha123{salt}").decode('utf-8')

    user = Usuario(
        perfil_id=perfil_admin.id,
        nome='Usuario Teste',
        sobrenome='Sistema',
        email='teste@login.com',
        cpf='00011122233',
        senha=senha_hash,
        salt=salt,
        username='teste_login',
        data_criacao=datetime.now(UTC),
        telefone='11999999999',
    )

    db.session.add(user)
    db.session.commit()
    return user
