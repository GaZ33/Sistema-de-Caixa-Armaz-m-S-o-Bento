def test_users_crud_flow(client, perfil_admin):
    payload = {
        'perfil_id': perfil_admin.id,
        'nome': 'Gabriel',
        'sobrenome': 'Silva',
        'email': 'gabriel.silva@test.com',
        'cpf': '12345678901',
        'senha': 'SenhaForte123',
        'username': 'gabriel_test',
        'telefone': '11977778888',
    }

    create_response = client.post('/api/users', json=payload)
    assert create_response.status_code == 201

    created_user = create_response.get_json()
    assert created_user['username'] == 'gabriel_test'
    assert 'senha' not in created_user

    user_id = created_user['id']

    list_response = client.get('/api/users')
    assert list_response.status_code == 200
    users = list_response.get_json()
    assert len(users) == 1

    get_response = client.get(f'/api/users/{user_id}')
    assert get_response.status_code == 200
    assert get_response.get_json()['email'] == 'gabriel.silva@test.com'

    update_response = client.put(
        f'/api/users/{user_id}',
        json={'nome': 'Gabriel Atualizado', 'telefone': '11911112222'},
    )
    assert update_response.status_code == 200
    assert update_response.get_json()['nome'] == 'Gabriel Atualizado'

    delete_response = client.delete(f'/api/users/{user_id}')
    assert delete_response.status_code == 204

    get_deleted_response = client.get(f'/api/users/{user_id}')
    assert get_deleted_response.status_code == 404
