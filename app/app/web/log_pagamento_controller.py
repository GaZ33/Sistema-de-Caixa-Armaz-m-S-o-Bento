from flask import Blueprint, jsonify, request
from app.services.log_pagamento_service import LogPagamentoService
from app.models import LogPagamento
from app.core.exceptions import NotFoundException
from app.web.dto import model_to_dto, models_to_dtos

log_pagamento_blueprint = Blueprint('log_pagamento', __name__)

def create_log_pagamento_controller(service: LogPagamentoService):
    @log_pagamento_blueprint.route('/log_pagamentos', methods=['POST'])
    def create_log_pagamento():
        data = request.get_json(silent=True) or {}
        log_pagamento = LogPagamento(**data)
        created_log_pagamento = service.create_log_pagamento(log_pagamento)
        return jsonify(model_to_dto(created_log_pagamento)), 201

    @log_pagamento_blueprint.route('/log_pagamentos', methods=['GET'])
    def get_logs_pagamento():
        logs_pagamento = service.get_all_logs_pagamento()
        return jsonify(models_to_dtos(logs_pagamento))

    @log_pagamento_blueprint.route('/log_pagamentos/<int:log_pagamento_id>', methods=['GET'])
    def get_log_pagamento(log_pagamento_id):
        try:
            log_pagamento = service.get_log_pagamento_by_id(log_pagamento_id)
            return jsonify(model_to_dto(log_pagamento))
        except NotFoundException as ex:
            return jsonify({'error': str(ex)}), 404

    @log_pagamento_blueprint.route('/log_pagamentos/<int:log_pagamento_id>', methods=['PUT'])
    def update_log_pagamento(log_pagamento_id):
        data = request.get_json(silent=True) or {}
        updated_log_pagamento = service.update_log_pagamento(log_pagamento_id, data)
        if not updated_log_pagamento:
            return jsonify({'error': f'LogPagamento with id {log_pagamento_id} not found.'}), 404
        return jsonify(model_to_dto(updated_log_pagamento))

    @log_pagamento_blueprint.route('/log_pagamentos/<int:log_pagamento_id>', methods=['DELETE'])
    def delete_log_pagamento(log_pagamento_id):
        service.delete_log_pagamento(log_pagamento_id)
        return '', 204

    return log_pagamento_blueprint