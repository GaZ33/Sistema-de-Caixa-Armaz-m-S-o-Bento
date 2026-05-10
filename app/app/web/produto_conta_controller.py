from flask import Blueprint, jsonify, request
from app.services.produto_conta_service import ProdutoContaService
from app.models import ProdutoConta

produto_conta_blueprint = Blueprint('produto_conta', __name__)

def create_produto_conta_controller(service: ProdutoContaService):
    @produto_conta_blueprint.route('/produto_conta', methods=['POST'])
    def create_produto_conta():
        data = request.json
        produto_conta = ProdutoConta(**data)
        created_produto_conta = service.create_produto_conta(produto_conta)
        return jsonify(created_produto_conta), 201

    @produto_conta_blueprint.route('/produto_conta', methods=['GET'])
    def get_produtos_conta():
        produtos_conta = service.get_all_produtos_conta()
        return jsonify([produto_conta for produto_conta in produtos_conta])

    @produto_conta_blueprint.route('/produto_conta/<int:produto_conta_id>', methods=['GET'])
    def get_produto_conta(produto_conta_id):
        produto_conta = service.get_produto_conta_by_id(produto_conta_id)
        return jsonify(produto_conta)

    @produto_conta_blueprint.route('/produto_conta/<int:produto_conta_id>', methods=['PUT'])
    def update_produto_conta(produto_conta_id):
        data = request.json
        produto_conta = ProdutoConta(id=produto_conta_id, **data)
        updated_produto_conta = service.update_produto_conta(produto_conta)
        return jsonify(updated_produto_conta)

    @produto_conta_blueprint.route('/produto_conta/<int:produto_conta_id>', methods=['DELETE'])
    def delete_produto_conta(produto_conta_id):
        service.delete_produto_conta(produto_conta_id)
        return '', 204

    return produto_conta_blueprint