from pathlib import Path
import sys

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / 'app'))

from app.services.produto_service import ProdutoService


class FakeRepository:
    def __init__(self):
        self.created = None
        self.updated = None
        self.deleted = None
        self.by_id = {}
        self.items = []
        self.search_result = []

    def create(self, produto):
        self.created = produto
        return produto

    def get_all(self):
        return list(self.items)

    def get_by_id(self, produto_id):
        return self.by_id.get(produto_id)

    def update(self, produto_id, data):
        self.updated = (produto_id, data)
        return {'id': produto_id, **data}

    def delete(self, produto_id):
        self.deleted = produto_id

    def buscar(self, query):
        return [item for item in self.search_result if query.lower() in item['nome'].lower()]


@pytest.fixture
def repo():
    return FakeRepository()


@pytest.fixture
def service(repo):
    return ProdutoService(repo)


def test_create_produto_delega_para_repositorio(service, repo):
    produto = {'nome': 'Cafe', 'codigo': 'CAF001'}

    created = service.create_produto(produto)

    assert created == produto
    assert repo.created == produto


def test_get_all_produtos_retorna_lista(service, repo):
    repo.items = [{'id': 1}, {'id': 2}, {'id': 3}]

    produtos = service.get_all_produtos()

    assert len(produtos) == 3


def test_get_produto_by_id_retorna_item(service, repo):
    repo.by_id[8] = {'id': 8, 'nome': 'Leite'}

    produto = service.get_produto_by_id(8)

    assert produto['nome'] == 'Leite'


def test_update_produto_delega_para_repositorio(service, repo):
    updated = service.update_produto(2, {'nome': 'Leite Integral'})

    assert repo.updated == (2, {'nome': 'Leite Integral'})
    assert updated['nome'] == 'Leite Integral'


def test_delete_produto_delega_para_repositorio(service, repo):
    service.delete_produto(4)

    assert repo.deleted == 4


def test_buscar_produtos_delega_busca(service, repo):
    repo.search_result = [
        {'id': 1, 'nome': 'Arroz Tipo 1'},
        {'id': 2, 'nome': 'Feijao Preto'},
    ]

    encontrados = service.buscar_produtos('Arroz')

    assert len(encontrados) == 1
    assert encontrados[0]['id'] == 1