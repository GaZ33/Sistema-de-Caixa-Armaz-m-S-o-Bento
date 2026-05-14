from flask import Blueprint, jsonify, request
from app.services.modulo_service import ModuloService
from app.models import Modulo

modulo_blueprint = Blueprint('modulo', __name__)

def create_modulo_controller(service: ModuloService):
    @modulo_blueprint.route('/modulos', methods=['POST'])
    def create_modulo():
        data = request.json
        modulo = Modulo(**data)
        created_modulo = service.create_modulo(modulo)
        return jsonify(created_modulo), 201

    @modulo_blueprint.route('/modulos', methods=['GET'])
    def get_modulos():
        modulos = service.get_all_modulos()
        return jsonify([modulo for modulo in modulos])

    @modulo_blueprint.route('/modulos/<int:modulo_id>', methods=['GET'])
    def get_modulo(modulo_id):
        modulo = service.get_modulo_by_id(modulo_id)
        return jsonify(modulo)

    @modulo_blueprint.route('/modulos/<int:modulo_id>', methods=['PUT'])
    def update_modulo(modulo_id):
        data = request.json
        modulo = Modulo(idmodulo=modulo_id, **data)
        updated_modulo = service.update_modulo(modulo)
        return jsonify(updated_modulo)

    @modulo_blueprint.route('/modulos/<int:modulo_id>', methods=['DELETE'])
    def delete_modulo(modulo_id):
        service.delete_modulo(modulo_id)
        return '', 204

    return modulo_blueprint