from flask import Blueprint, jsonify, request
from app.services.avisos_estoque_service import AvisosEstoqueService
from app.models import AvisosEstoque
from app.web.dto import model_to_dto, models_to_dtos

avisos_estoque_blueprint = Blueprint('avisos_estoque', __name__)

def create_avisos_estoque_controller(service: AvisosEstoqueService):
    @avisos_estoque_blueprint.route('/avisos_estoque', methods=['POST'])
    def create_aviso_estoque():
        data = request.get_json(silent=True) or {}
        aviso_estoque = AvisosEstoque(**data)
        created_aviso_estoque = service.create_aviso_estoque(aviso_estoque)
        return jsonify(model_to_dto(created_aviso_estoque)), 201

    @avisos_estoque_blueprint.route('/avisos_estoque', methods=['GET'])
    def get_avisos_estoque():
        avisos_estoque = service.get_all_avisos_estoque()
        return jsonify(models_to_dtos(avisos_estoque))

    @avisos_estoque_blueprint.route('/avisos_estoque/<int:aviso_estoque_id>', methods=['GET'])
    def get_aviso_estoque(aviso_estoque_id):
        aviso_estoque = service.get_aviso_estoque_by_id(aviso_estoque_id)
        if not aviso_estoque:
            return jsonify({'error': f'AvisosEstoque with id {aviso_estoque_id} not found.'}), 404
        return jsonify(model_to_dto(aviso_estoque))

    @avisos_estoque_blueprint.route('/avisos_estoque/<int:aviso_estoque_id>', methods=['PUT'])
    def update_aviso_estoque(aviso_estoque_id):
        data = request.get_json(silent=True) or {}
        updated_aviso_estoque = service.update_aviso_estoque(aviso_estoque_id, data)
        if not updated_aviso_estoque:
            return jsonify({'error': f'AvisosEstoque with id {aviso_estoque_id} not found.'}), 404
        return jsonify(model_to_dto(updated_aviso_estoque))

    @avisos_estoque_blueprint.route('/avisos_estoque/<int:aviso_estoque_id>', methods=['DELETE'])
    def delete_aviso_estoque(aviso_estoque_id):
        service.delete_aviso_estoque(aviso_estoque_id)
        return '', 204

    return avisos_estoque_blueprint