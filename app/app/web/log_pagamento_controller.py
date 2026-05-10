from flask import Blueprint, jsonify, request
from app.services.log_pagamento_service import LogPagamentoService
from app.models import LogPagamento

log_pagamento_blueprint = Blueprint('log_pagamento', __name__)

def create_log_pagamento_controller(service: LogPagamentoService):
    @log_pagamento_blueprint.route('/log_pagamentos', methods=['POST'])
    def create_log_pagamento():
        data = request.json
        log_pagamento = LogPagamento(**data)
        created_log_pagamento = service.create_log_pagamento(log_pagamento)
        return jsonify(created_log_pagamento), 201

    @log_pagamento_blueprint.route('/log_pagamentos', methods=['GET'])
    def get_logs_pagamento():
        logs_pagamento = service.get_all_logs_pagamento()
        return jsonify([log for log in logs_pagamento])

    @log_pagamento_blueprint.route('/log_pagamentos/<int:log_pagamento_id>', methods=['GET'])
    def get_log_pagamento(log_pagamento_id):
        log_pagamento = service.get_log_pagamento_by_id(log_pagamento_id)
        return jsonify(log_pagamento)

    @log_pagamento_blueprint.route('/log_pagamentos/<int:log_pagamento_id>', methods=['PUT'])
    def update_log_pagamento(log_pagamento_id):
        data = request.json
        log_pagamento = LogPagamento(id=log_pagamento_id, **data)
        updated_log_pagamento = service.update_log_pagamento(log_pagamento)
        return jsonify(updated_log_pagamento)

    @log_pagamento_blueprint.route('/log_pagamentos/<int:log_pagamento_id>', methods=['DELETE'])
    def delete_log_pagamento(log_pagamento_id):
        service.delete_log_pagamento(log_pagamento_id)
        return '', 204

    return log_pagamento_blueprint