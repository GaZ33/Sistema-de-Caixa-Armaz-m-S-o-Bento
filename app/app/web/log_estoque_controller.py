from flask import Blueprint, jsonify, request
from app.services.log_estoque_service import LogEstoqueService
from app.models import LogEstoque
from app.web.dto import model_to_dto, models_to_dtos

log_estoque_blueprint = Blueprint('log_estoque', __name__)

def create_log_estoque_controller(service: LogEstoqueService):
    @log_estoque_blueprint.route('/log_estoque', methods=['POST'])
    def create_log_estoque():
        data = request.get_json(silent=True) or {}
        log_estoque = LogEstoque(**data)
        created_log_estoque = service.create_log_estoque(log_estoque)
        return jsonify(model_to_dto(created_log_estoque)), 201

    @log_estoque_blueprint.route('/log_estoque', methods=['GET'])
    def get_logs_estoque():
        logs_estoque = service.get_all_logs_estoque()
        return jsonify(models_to_dtos(logs_estoque))

    @log_estoque_blueprint.route('/log_estoque/<int:log_estoque_id>', methods=['GET'])
    def get_log_estoque(log_estoque_id):
        log_estoque = service.get_log_estoque_by_id(log_estoque_id)
        if not log_estoque:
            return jsonify({'error': f'LogEstoque with id {log_estoque_id} not found.'}), 404
        return jsonify(model_to_dto(log_estoque))

    @log_estoque_blueprint.route('/log_estoque/<int:log_estoque_id>', methods=['PUT'])
    def update_log_estoque(log_estoque_id):
        data = request.get_json(silent=True) or {}
        updated_log_estoque = service.update_log_estoque(log_estoque_id, data)
        if not updated_log_estoque:
            return jsonify({'error': f'LogEstoque with id {log_estoque_id} not found.'}), 404
        return jsonify(model_to_dto(updated_log_estoque))

    @log_estoque_blueprint.route('/log_estoque/<int:log_estoque_id>', methods=['DELETE'])
    def delete_log_estoque(log_estoque_id):
        service.delete_log_estoque(log_estoque_id)
        return '', 204

    return log_estoque_blueprint