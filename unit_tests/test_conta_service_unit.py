from pathlib import Path
import sys

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / 'app'))

from app.core.exceptions import NotFoundException
from app.services.conta_service import ContaService


class FakeRepository:
    def __init__(self):
        self.by_id = {}
        self.items = []
        self.created = None
        self.updated = None
        self.deleted = None

    def create(self, conta):
        self.created = conta
        return conta

    def get_all(self):
        return list(self.items)

    def get_by_id(self, conta_id):
        return self.by_id.get(conta_id)

    def update(self, conta_id, data):
        self.updated = (conta_id, data)
        return {'id': conta_id, **data}

    def delete(self, conta_id):
        self.deleted = conta_id


@pytest.fixture
def repo():
    return FakeRepository()


@pytest.fixture
def service(repo):
    return ContaService(repo)


def test_create_conta_delega_para_repositorio(service, repo):
    conta = {'funcionario': 1, 'status': 'aberta'}

    created = service.create_conta(conta)

    assert created == conta
    assert repo.created == conta


def test_get_all_contas_retorna_lista_do_repositorio(service, repo):
    repo.items = [{'id': 1}, {'id': 2}]

    contas = service.get_all_contas()

    assert len(contas) == 2
    assert contas[0]['id'] == 1


def test_get_conta_by_id_retorna_conta(service, repo):
    repo.by_id[10] = {'id': 10, 'status': 'aberta'}

    conta = service.get_conta_by_id(10)

    assert conta['id'] == 10


def test_get_conta_by_id_lanca_not_found_quando_nao_existe(service):
    with pytest.raises(NotFoundException, match='Conta with id 99 not found'):
        service.get_conta_by_id(99)


def test_update_conta_delega_para_repositorio(service, repo):
    updated = service.update_conta(7, {'status': 'fechada'})

    assert repo.updated == (7, {'status': 'fechada'})
    assert updated['status'] == 'fechada'


def test_delete_conta_delega_para_repositorio(service, repo):
    service.delete_conta(11)

    assert repo.deleted == 11