from datetime import UTC, datetime

from app.models import Produto


def test_contas_crud_flow(client, auth_user):
    payload = {
        'funcionario': auth_user.id,
        'cliente': None,
        'data_criacao': datetime.now(UTC).isoformat(),
        'data_alteracao': None,
        'data_fechamento': None,
        'status': 'aberta',
        'valor_total': 0,
    }

    create_response = client.post('/api/contas', json=payload)
    assert create_response.status_code == 201

    created_conta = create_response.get_json()
    assert created_conta['funcionario'] == auth_user.id
    assert created_conta['status'] == 'aberta'

    conta_id = created_conta['id']

    list_response = client.get('/api/contas')
    assert list_response.status_code == 200
    assert len(list_response.get_json()) == 1

    get_response = client.get(f'/api/contas/{conta_id}')
    assert get_response.status_code == 200
    assert get_response.get_json()['id'] == conta_id

    update_response = client.put(
        f'/api/contas/{conta_id}',
        json={'status': 'fechada', 'valor_total': 32},
    )
    assert update_response.status_code == 200
    updated_conta = update_response.get_json()
    assert updated_conta['status'] == 'fechada'
    assert float(updated_conta['valor_total']) == 32.0
    assert updated_conta['data_fechamento'] is not None

    delete_response = client.delete(f'/api/contas/{conta_id}')
    assert delete_response.status_code == 204

    get_deleted_response = client.get(f'/api/contas/{conta_id}')
    assert get_deleted_response.status_code == 404


def test_estoque_crud_flow(client):
    produto = Produto(
        nome='Acucar Refinado',
        preco_unidade=7.5,
        unidade='pacote',
        codigo='ACUCAR001',
        marca='Marca Doce',
    )

    from app import db

    db.session.add(produto)
    db.session.commit()

    payload = {
        'produto_id': produto.id,
        'quantidade_atual': 20,
        'quantidade_minima': 5,
        'data_alteracao': datetime.now(UTC).isoformat(),
    }

    create_response = client.post('/api/estoque', json=payload)
    assert create_response.status_code == 201

    created_estoque = create_response.get_json()
    assert created_estoque['produto_id'] == produto.id
    assert float(created_estoque['quantidade_atual']) == 20.0

    estoque_id = created_estoque['id']

    list_response = client.get('/api/estoque')
    assert list_response.status_code == 200
    assert len(list_response.get_json()) == 1

    get_response = client.get(f'/api/estoque/{estoque_id}')
    assert get_response.status_code == 200
    assert get_response.get_json()['produto_id'] == produto.id

    update_response = client.put(
        f'/api/estoque/{estoque_id}',
        json={'quantidade_atual': 12, 'quantidade_minima': 4},
    )
    assert update_response.status_code == 200
    updated_estoque = update_response.get_json()
    assert float(updated_estoque['quantidade_atual']) == 12.0
    assert float(updated_estoque['quantidade_minima']) == 4.0

    delete_response = client.delete(f'/api/estoque/{estoque_id}')
    assert delete_response.status_code == 204

    get_deleted_response = client.get(f'/api/estoque/{estoque_id}')
    assert get_deleted_response.status_code == 404