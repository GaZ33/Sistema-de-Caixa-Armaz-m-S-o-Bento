from flask import Blueprint, jsonify, request
from app.services.avisos_estoque_service import AvisosEstoqueService
from app.models import AvisosEstoque

avisos_estoque_blueprint = Blueprint('avisos_estoque', __name__)

def create_avisos_estoque_controller(service: AvisosEstoqueService):
    @avisos_estoque_blueprint.route('/avisos_estoque', methods=['POST'])
    def create_aviso_estoque():
        data = request.json
        aviso_estoque = AvisosEstoque(**data)
        created_aviso_estoque = service.create_aviso_estoque(aviso_estoque)
        return jsonify(created_aviso_estoque), 201

    @avisos_estoque_blueprint.route('/avisos_estoque', methods=['GET'])
    def get_avisos_estoque():
        avisos_estoque = service.get_all_avisos_estoque()
        return jsonify([aviso_estoque for aviso_estoque in avisos_estoque])

    @avisos_estoque_blueprint.route('/avisos_estoque/<int:aviso_estoque_id>', methods=['GET'])
    def get_aviso_estoque(aviso_estoque_id):
        aviso_estoque = service.get_aviso_estoque_by_id(aviso_estoque_id)
        return jsonify(aviso_estoque)

    @avisos_estoque_blueprint.route('/avisos_estoque/<int:aviso_estoque_id>', methods=['PUT'])
    def update_aviso_estoque(aviso_estoque_id):
        data = request.json
        aviso_estoque = AvisosEstoque(id=aviso_estoque_id, **data)
        updated_aviso_estoque = service.update_aviso_estoque(aviso_estoque)
        return jsonify(updated_aviso_estoque)

    @avisos_estoque_blueprint.route('/avisos_estoque/<int:aviso_estoque_id>', methods=['DELETE'])
    def delete_aviso_estoque(aviso_estoque_id):
        service.delete_aviso_estoque(aviso_estoque_id)
        return '', 204

    return avisos_estoque_blueprint