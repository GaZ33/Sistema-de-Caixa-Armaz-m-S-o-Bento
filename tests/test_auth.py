def test_anonimo_redirecionado_para_login(client):
    response = client.get('/')

    assert response.status_code == 302
    assert '/login' in response.headers['Location']


def test_login_com_credenciais_validas_mantem_sessao(client, auth_user):
    login_response = client.post(
        '/login',
        data={'identifier': 'teste_login', 'senha': 'senha123'},
        follow_redirects=False,
    )

    assert login_response.status_code == 302
    assert login_response.headers['Location'].endswith('/')

    home_response = client.get('/')

    assert home_response.status_code == 200
    assert b'Usuario Teste' not in home_response.data
    assert b'teste_login' in home_response.data


def test_login_invalido_retorna_401(client, auth_user):
    response = client.post(
        '/login',
        data={'identifier': 'teste_login', 'senha': 'senha_incorreta'},
        follow_redirects=False,
    )

    assert response.status_code == 401
    assert b'Credenciais invalidas' in response.data


def test_logout_invalida_sessao(client, auth_user):
    client.post('/login', data={'identifier': 'teste_login', 'senha': 'senha123'})

    logout_response = client.post('/logout', follow_redirects=False)

    assert logout_response.status_code == 302
    assert '/login' in logout_response.headers['Location']

    protected_response = client.get('/')
    assert protected_response.status_code == 302
    assert '/login' in protected_response.headers['Location']
