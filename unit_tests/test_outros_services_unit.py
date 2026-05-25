from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / 'app'))

from app.services.avisos_estoque_service import AvisosEstoqueService
from app.services.estoque_service import EstoqueService
from app.services.produto_conta_service import ProdutoContaService


class FakeRepository:
    def __init__(self):
        self.created = None
        self.updated = None
        self.deleted = None
        self.by_id = {}
        self.items = []

    def create(self, payload):
        self.created = payload
        return payload

    def get_all(self):
        return list(self.items)

    def get_by_id(self, item_id):
        return self.by_id.get(item_id)

    def update(self, item_id, data):
        self.updated = (item_id, data)
        return {'id': item_id, **data}

    def delete(self, item_id):
        self.deleted = item_id


def test_estoque_service_fluxo_basico():
    repo = FakeRepository()
    service = EstoqueService(repo)

    created = service.create_estoque({'produto_id': 1, 'quantidade_atual': 10})
    assert created['produto_id'] == 1

    repo.items = [{'id': 1}, {'id': 2}]
    assert len(service.get_all_estoques()) == 2

    repo.by_id[9] = {'id': 9, 'quantidade_atual': 5}
    assert service.get_estoque_by_id(9)['id'] == 9

    updated = service.update_estoque(9, {'quantidade_atual': 7})
    assert repo.updated == (9, {'quantidade_atual': 7})
    assert updated['quantidade_atual'] == 7

    service.delete_estoque(9)
    assert repo.deleted == 9


def test_avisos_estoque_service_fluxo_basico():
    repo = FakeRepository()
    service = AvisosEstoqueService(repo)

    created = service.create_aviso_estoque({'estoque_id': 1, 'status': 'pendente'})
    assert created['status'] == 'pendente'

    repo.items = [{'id': 1}]
    assert len(service.get_all_avisos_estoque()) == 1

    repo.by_id[3] = {'id': 3, 'descricao': 'Baixo estoque'}
    assert service.get_aviso_estoque_by_id(3)['descricao'] == 'Baixo estoque'

    updated = service.update_aviso_estoque(3, {'status': 'resolvido'})
    assert repo.updated == (3, {'status': 'resolvido'})
    assert updated['status'] == 'resolvido'

    service.delete_aviso_estoque(3)
    assert repo.deleted == 3


def test_produto_conta_service_fluxo_basico():
    repo = FakeRepository()
    service = ProdutoContaService(repo)

    created = service.create_produto_conta({'conta_id': 1, 'produto_id': 2, 'quantidade': 1})
    assert created['produto_id'] == 2

    repo.items = [{'id': 1}, {'id': 2}, {'id': 3}]
    assert len(service.get_all_produtos_conta()) == 3

    repo.by_id[4] = {'id': 4, 'subtotal': 39.9}
    assert service.get_produto_conta_by_id(4)['subtotal'] == 39.9

    updated = service.update_produto_conta(4, {'quantidade': 2})
    assert repo.updated == (4, {'quantidade': 2})
    assert updated['quantidade'] == 2

    service.delete_produto_conta(4)
    assert repo.deleted == 4