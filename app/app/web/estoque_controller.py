from flask import Blueprint, jsonify, request
from app.services.estoque_service import EstoqueService
from app.models import Estoque
from app.web.dto import model_to_dto, models_to_dtos

estoque_blueprint = Blueprint('estoque', __name__)

def create_estoque_controller(service: EstoqueService):
    @estoque_blueprint.route('/estoque', methods=['POST'])
    def create_estoque():
        data = request.get_json(silent=True) or {}
        estoque = Estoque(**data)
        created_estoque = service.create_estoque(estoque)
        return jsonify(model_to_dto(created_estoque)), 201

    @estoque_blueprint.route('/estoque', methods=['GET'])
    def get_estoques():
        estoques = service.get_all_estoques()
        return jsonify(models_to_dtos(estoques))

    @estoque_blueprint.route('/estoque/<int:estoque_id>', methods=['GET'])
    def get_estoque(estoque_id):
        estoque = service.get_estoque_by_id(estoque_id)
        if not estoque:
            return jsonify({'error': f'Estoque with id {estoque_id} not found.'}), 404
        return jsonify(model_to_dto(estoque))

    @estoque_blueprint.route('/estoque/<int:estoque_id>', methods=['PUT'])
    def update_estoque(estoque_id):
        data = request.get_json(silent=True) or {}
        updated_estoque = service.update_estoque(estoque_id, data)
        if not updated_estoque:
            return jsonify({'error': f'Estoque with id {estoque_id} not found.'}), 404
        return jsonify(model_to_dto(updated_estoque))

    @estoque_blueprint.route('/estoque/<int:estoque_id>', methods=['DELETE'])
    def delete_estoque(estoque_id):
        service.delete_estoque(estoque_id)
        return '', 204

    return estoque_blueprint