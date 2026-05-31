from flask import Blueprint, jsonify, request
from app.services.produto_conta_service import ProdutoContaService
from app.models import ProdutoConta
from app.web.dto import model_to_dto, models_to_dtos

produto_conta_blueprint = Blueprint('produto_conta', __name__)

def create_produto_conta_controller(service: ProdutoContaService):
    @produto_conta_blueprint.route('/produto_conta', methods=['POST'])
    def create_produto_conta():
        data = request.get_json(silent=True) or {}
        produto_conta = ProdutoConta(**data)
        created_produto_conta = service.create_produto_conta(produto_conta)
        return jsonify(model_to_dto(created_produto_conta)), 201

    @produto_conta_blueprint.route('/produto_conta', methods=['GET'])
    def get_produtos_conta():
        produtos_conta = service.get_all_produtos_conta()
        return jsonify(models_to_dtos(produtos_conta))

    @produto_conta_blueprint.route('/produto_conta/<int:produto_conta_id>', methods=['GET'])
    def get_produto_conta(produto_conta_id):
        produto_conta = service.get_produto_conta_by_id(produto_conta_id)
        if not produto_conta:
            return jsonify({'error': f'ProdutoConta with id {produto_conta_id} not found.'}), 404
        return jsonify(model_to_dto(produto_conta))

    @produto_conta_blueprint.route('/produto_conta/<int:produto_conta_id>', methods=['PUT'])
    def update_produto_conta(produto_conta_id):
        data = request.get_json(silent=True) or {}
        updated_produto_conta = service.update_produto_conta(produto_conta_id, data)
        if not updated_produto_conta:
            return jsonify({'error': f'ProdutoConta with id {produto_conta_id} not found.'}), 404
        return jsonify(model_to_dto(updated_produto_conta))

    @produto_conta_blueprint.route('/produto_conta/<int:produto_conta_id>', methods=['DELETE'])
    def delete_produto_conta(produto_conta_id):
        service.delete_produto_conta(produto_conta_id)
        return '', 204

    return produto_conta_blueprint