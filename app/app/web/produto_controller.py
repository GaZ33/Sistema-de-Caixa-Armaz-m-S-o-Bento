from flask import Blueprint, jsonify, request
from app.services.produto_service import ProdutoService
from app.models import Produto

produto_blueprint = Blueprint('produto', __name__)

def create_produto_controller(service: ProdutoService):
    @produto_blueprint.route('/produtos', methods=['POST'])
    def create_produto():
        data = request.json
        produto = Produto(**data)
        created_produto = service.create_produto(produto)
        return jsonify(created_produto), 201

    @produto_blueprint.route('/produtos', methods=['GET'])
    def get_produtos():
        produtos = service.get_all_produtos()
        produtos_serializados = [
            {
                'id': produto.id,
                'nome': produto.nome,
                'preco_unidade': float(produto.preco_unidade),
                'quantidade': 0,
                'unidade': produto.unidade,
                'codigo': produto.codigo,
                'marca': produto.marca
            }
            for produto in produtos
        ]
        return jsonify(produtos_serializados)

    @produto_blueprint.route('/produtos/<int:produto_id>', methods=['GET'])
    def get_produto(produto_id):
        produto = service.get_produto_by_id(produto_id)
        produto_serializado = {
            'id': produto.id,
            'nome': produto.nome,
            'preco_unidade': float(produto.preco_unidade),
            'unidade': produto.unidade, 
            'codigo': produto.codigo,
            'marca': produto.marca
        }
        return jsonify(produto_serializado)

    @produto_blueprint.route('/produtos/<int:produto_id>', methods=['PUT'])
    def update_produto(produto_id):
        data = request.json
        produto = Produto(id=produto_id, **data)
        updated_produto = service.update_produto(produto)
        return jsonify(updated_produto)

    @produto_blueprint.route('/produtos/<int:produto_id>', methods=['DELETE'])
    def delete_produto(produto_id):
        service.delete_produto(produto_id)
        return '', 204

    @produto_blueprint.route('/produtos/buscar', methods=['GET'])
    def buscar_produtos():
        query = request.args.get('query', '')
        produtos = service.buscar_produtos(query)

        produtos_serializados = [
            {
                'id': produto.id,
                'nome': produto.nome,
                'preco_unidade': float(produto.preco_unidade),
                'codigo': produto.codigo,
                'unidade': produto.unidade,
                'marca': produto.marca
            }
            for produto in produtos
        ]
        return jsonify(produtos_serializados)

    return produto_blueprint