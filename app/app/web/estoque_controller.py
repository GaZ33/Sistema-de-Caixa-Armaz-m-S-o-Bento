from flask import Blueprint, jsonify, request
from app.services.estoque_service import EstoqueService
from app.models import Estoque

estoque_blueprint = Blueprint('estoque', __name__)

def create_estoque_controller(service: EstoqueService):
    @estoque_blueprint.route('/estoque', methods=['POST'])
    def create_estoque():
        data = request.json
        estoque = Estoque(**data)
        created_estoque = service.create_estoque(estoque)
        return jsonify(created_estoque), 201

    @estoque_blueprint.route('/estoque', methods=['GET'])
    def get_estoques():
        estoques = service.get_all_estoques()
        return jsonify([estoque for estoque in estoques])

    @estoque_blueprint.route('/estoque/<int:estoque_id>', methods=['GET'])
    def get_estoque(estoque_id):
        estoque = service.get_estoque_by_id(estoque_id)
        return jsonify(estoque)

    @estoque_blueprint.route('/estoque/<int:estoque_id>', methods=['PUT'])
    def update_estoque(estoque_id):
        data = request.json
        estoque = Estoque(id=estoque_id, **data)
        updated_estoque = service.update_estoque(estoque)
        return jsonify(updated_estoque)

    @estoque_blueprint.route('/estoque/<int:estoque_id>', methods=['DELETE'])
    def delete_estoque(estoque_id):
        service.delete_estoque(estoque_id)
        return '', 204

    return estoque_blueprint