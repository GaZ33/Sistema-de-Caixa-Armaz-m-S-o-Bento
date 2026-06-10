from flask import Blueprint, jsonify, request
from app.services.produto_service import ProdutoService
from app.models import Produto
from app.web.dto import model_to_dto, models_to_dtos

produto_blueprint = Blueprint('produto', __name__)

def create_produto_controller(service: ProdutoService):
    @produto_blueprint.route('/produtos', methods=['POST'])
    def create_produto():
        data = request.get_json(silent=True) or {}
        produto = Produto(**data)
        created_produto = service.create_produto(produto)
        return jsonify(model_to_dto(created_produto)), 201

    @produto_blueprint.route('/produtos', methods=['GET'])
    def get_produtos():
        produtos = service.get_all_produtos()
        return jsonify(models_to_dtos(produtos))

    @produto_blueprint.route('/produtos/<int:produto_id>', methods=['GET'])
    def get_produto(produto_id):
        produto = service.get_produto_by_id(produto_id)
        if not produto:
            return jsonify({'error': f'Produto with id {produto_id} not found.'}), 404
        return jsonify(model_to_dto(produto))

    @produto_blueprint.route('/produtos/<int:produto_id>', methods=['PUT'])
    def update_produto(produto_id):
        data = request.get_json(silent=True) or {}
        updated_produto = service.update_produto(produto_id, data)
        if not updated_produto:
            return jsonify({'error': f'Produto with id {produto_id} not found.'}), 404
        return jsonify(model_to_dto(updated_produto))

    @produto_blueprint.route('/produtos/<int:produto_id>', methods=['DELETE'])
    def delete_produto(produto_id):
        service.delete_produto(produto_id)
        return '', 204

    @produto_blueprint.route('/produtos/buscar', methods=['GET'])
    def buscar_produtos():
        query = request.args.get('query', '')
        print(f"[BACKEND] Buscando produtos com a query: '{query}'", flush=True)
        produtos = service.buscar_produtos(query)
        print(f"[BACKEND] Encontrados {len(produtos)} produtos.", flush=True)
        return jsonify(models_to_dtos(produtos))

    return produto_blueprint