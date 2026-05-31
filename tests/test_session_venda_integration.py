from decimal import Decimal

from app import db
from app.models import Conta, Produto, ProdutoConta


def _login_json(client, identifier='teste_login', senha='senha123'):
    return client.post(
        '/login',
        json={'identifier': identifier, 'senha': senha},
    )


def test_session_info_anonimo_retorna_401(client):
    response = client.get('/api/session')

    assert response.status_code == 401
    payload = response.get_json()
    assert payload['authenticated'] is False
    assert payload['user'] is None


def test_login_json_preenche_session_info(client, auth_user):
    login_response = _login_json(client)

    assert login_response.status_code == 200
    login_payload = login_response.get_json()
    assert login_payload['message'] == 'Login realizado com sucesso.'
    assert login_payload['user']['username'] == auth_user.username

    session_response = client.get('/api/session')

    assert session_response.status_code == 200
    session_payload = session_response.get_json()
    assert session_payload['authenticated'] is True
    assert session_payload['user']['username'] == auth_user.username


def test_logout_json_invalida_session_api(client, auth_user):
    _login_json(client)

    logout_response = client.post('/logout', json={})

    assert logout_response.status_code == 200
    assert logout_response.get_json()['message'] == 'Logout realizado com sucesso.'

    session_response = client.get('/api/session')
    assert session_response.status_code == 401
    assert session_response.get_json()['authenticated'] is False


def test_finalizar_venda_sem_login_redireciona_para_login(client):
    response = client.post(
        '/api/venda/finalizar',
        json={'carrinho': [{'id': 1, 'qtd': 1}], 'forma_pagamento': 'pix'},
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert '/login' in response.headers['Location']


def test_finalizar_venda_com_carrinho_vazio_retorna_400(client, auth_user):
    _login_json(client)

    response = client.post(
        '/api/venda/finalizar',
        json={'carrinho': [], 'forma_pagamento': 'pix'},
    )

    assert response.status_code == 400
    assert response.get_json()['error'] == 'Carrinho vazio.'


def test_finalizar_venda_cria_conta_e_itens_no_banco(client, auth_user):
    produto = Produto(
        nome='Cafe Torrado',
        preco_unidade=Decimal('18.50'),
        unidade='pacote',
        codigo='CAFE001',
        marca='Marca Cafe',
    )
    db.session.add(produto)
    db.session.commit()

    _login_json(client)

    response = client.post(
        '/api/venda/finalizar',
        json={
            'carrinho': [{'id': produto.id, 'qtd': 2}],
            'forma_pagamento': 'pix',
            'cliente_id': None,
        },
    )

    assert response.status_code == 201
    payload = response.get_json()
    assert payload['message'] == 'Venda finalizada com sucesso.'
    assert payload['forma_pagamento'] == 'pix'
    assert payload['conta']['funcionario'] == auth_user.id
    assert float(payload['conta']['valor_total']) == 37.0
    assert len(payload['itens']) == 1
    assert float(payload['itens'][0]['subtotal']) == 37.0

    contas = db.session.query(Conta).all()
    itens = db.session.query(ProdutoConta).all()

    assert len(contas) == 1
    assert contas[0].status == 'fechada'
    assert float(contas[0].valor_total) == 37.0
    assert len(itens) == 1
    assert itens[0].produto_id == produto.id
    assert float(itens[0].subtotal) == 37.0


def test_finalizar_venda_com_produto_inexistente_retorna_404(client, auth_user):
    _login_json(client)

    response = client.post(
        '/api/venda/finalizar',
        json={
            'carrinho': [{'id': 9999, 'qtd': 1}],
            'forma_pagamento': 'cartao_credito',
        },
    )

    assert response.status_code == 404
    assert response.get_json()['error'] == 'Produto 9999 nao encontrado.'