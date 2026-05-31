def test_produtos_crud_flow(client):
    payload = {
        'nome': 'Arroz 5kg',
        'preco_unidade': 29.9,
        'unidade': 'pacote',
        'codigo': 'ARROZ5KG001',
        'marca': 'Marca Teste',
    }

    create_response = client.post('/api/produtos', json=payload)
    assert create_response.status_code == 201

    created_produto = create_response.get_json()
    assert created_produto['nome'] == 'Arroz 5kg'

    produto_id = created_produto['id']

    list_response = client.get('/api/produtos')
    assert list_response.status_code == 200
    produtos = list_response.get_json()
    assert len(produtos) == 1

    get_response = client.get(f'/api/produtos/{produto_id}')
    assert get_response.status_code == 200
    assert get_response.get_json()['codigo'] == 'ARROZ5KG001'

    update_response = client.put(
        f'/api/produtos/{produto_id}',
        json={'nome': 'Arroz Tipo 1 5kg', 'marca': 'Marca Atualizada'},
    )
    assert update_response.status_code == 200
    assert update_response.get_json()['nome'] == 'Arroz Tipo 1 5kg'

    busca_response = client.get('/api/produtos/buscar?query=Tipo 1')
    assert busca_response.status_code == 200
    assert len(busca_response.get_json()) == 1

    delete_response = client.delete(f'/api/produtos/{produto_id}')
    assert delete_response.status_code == 204

    get_deleted_response = client.get(f'/api/produtos/{produto_id}')
    assert get_deleted_response.status_code == 404
