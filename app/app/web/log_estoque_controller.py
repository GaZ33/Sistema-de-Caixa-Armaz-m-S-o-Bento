from flask import Blueprint, jsonify, request
from app.services.log_estoque_service import LogEstoqueService
from app.models import LogEstoque

log_estoque_blueprint = Blueprint('log_estoque', __name__)

def create_log_estoque_controller(service: LogEstoqueService):
    @log_estoque_blueprint.route('/log_estoque', methods=['POST'])
    def create_log_estoque():
        data = request.json
        log_estoque = LogEstoque(**data)
        created_log_estoque = service.create_log_estoque(log_estoque)
        return jsonify(created_log_estoque), 201

    @log_estoque_blueprint.route('/log_estoque', methods=['GET'])
    def get_logs_estoque():
        logs_estoque = service.get_all_logs_estoque()
        return jsonify([log_estoque for log_estoque in logs_estoque])

    @log_estoque_blueprint.route('/log_estoque/<int:log_estoque_id>', methods=['GET'])
    def get_log_estoque(log_estoque_id):
        log_estoque = service.get_log_estoque_by_id(log_estoque_id)
        return jsonify(log_estoque)

    @log_estoque_blueprint.route('/log_estoque/<int:log_estoque_id>', methods=['PUT'])
    def update_log_estoque(log_estoque_id):
        data = request.json
        log_estoque = LogEstoque(id=log_estoque_id, **data)
        updated_log_estoque = service.update_log_estoque(log_estoque)
        return jsonify(updated_log_estoque)

    @log_estoque_blueprint.route('/log_estoque/<int:log_estoque_id>', methods=['DELETE'])
    def delete_log_estoque(log_estoque_id):
        service.delete_log_estoque(log_estoque_id)
        return '', 204

    return log_estoque_blueprint