from flask import Blueprint, jsonify, request
from app.services.modulo_service import ModuloService
from app.models import Modulo
from app.web.dto import model_to_dto, models_to_dtos

modulo_blueprint = Blueprint('modulo', __name__)

def create_modulo_controller(service: ModuloService):
    @modulo_blueprint.route('/modulos', methods=['POST'])
    def create_modulo():
        data = request.get_json(silent=True) or {}
        modulo = Modulo(**data)
        created_modulo = service.create_modulo(modulo)
        return jsonify(model_to_dto(created_modulo)), 201

    @modulo_blueprint.route('/modulos', methods=['GET'])
    def get_modulos():
        modulos = service.get_all_modulos()
        return jsonify(models_to_dtos(modulos))

    @modulo_blueprint.route('/modulos/<int:modulo_id>', methods=['GET'])
    def get_modulo(modulo_id):
        modulo = service.get_modulo_by_id(modulo_id)
        if not modulo:
            return jsonify({'error': f'Modulo with id {modulo_id} not found.'}), 404
        return jsonify(model_to_dto(modulo))

    @modulo_blueprint.route('/modulos/<int:modulo_id>', methods=['PUT'])
    def update_modulo(modulo_id):
        data = request.get_json(silent=True) or {}
        updated_modulo = service.update_modulo(modulo_id, data)
        if not updated_modulo:
            return jsonify({'error': f'Modulo with id {modulo_id} not found.'}), 404
        return jsonify(model_to_dto(updated_modulo))

    @modulo_blueprint.route('/modulos/<int:modulo_id>', methods=['DELETE'])
    def delete_modulo(modulo_id):
        service.delete_modulo(modulo_id)
        return '', 204

    return modulo_blueprint