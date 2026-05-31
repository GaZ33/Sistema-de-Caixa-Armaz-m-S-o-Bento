from flask import Blueprint, jsonify, request
from app.services.log_alteracoes_service import LogAlteracoesService
from app.models import LogAlteracoes
from app.core.exceptions import NotFoundException
from app.web.dto import model_to_dto, models_to_dtos

log_alteracoes_blueprint = Blueprint('log_alteracoes', __name__)

def create_log_alteracoes_controller(service: LogAlteracoesService):
    @log_alteracoes_blueprint.route('/log_alteracoes', methods=['POST'])
    def create_log_alteracao():
        data = request.get_json(silent=True) or {}
        log_alteracao = LogAlteracoes(**data)
        created_log_alteracao = service.create_log_alteracao(log_alteracao)
        return jsonify(model_to_dto(created_log_alteracao)), 201

    @log_alteracoes_blueprint.route('/log_alteracoes', methods=['GET'])
    def get_logs_alteracoes():
        logs_alteracoes = service.get_all_logs_alteracoes()
        return jsonify(models_to_dtos(logs_alteracoes))

    @log_alteracoes_blueprint.route('/log_alteracoes/<int:log_alteracao_id>', methods=['GET'])
    def get_log_alteracao(log_alteracao_id):
        try:
            log_alteracao = service.get_log_alteracao_by_id(log_alteracao_id)
            return jsonify(model_to_dto(log_alteracao))
        except NotFoundException as ex:
            return jsonify({'error': str(ex)}), 404

    @log_alteracoes_blueprint.route('/log_alteracoes/<int:log_alteracao_id>', methods=['PUT'])
    def update_log_alteracao(log_alteracao_id):
        data = request.get_json(silent=True) or {}
        updated_log_alteracao = service.update_log_alteracao(log_alteracao_id, data)
        if not updated_log_alteracao:
            return jsonify({'error': f'LogAlteracoes with id {log_alteracao_id} not found.'}), 404
        return jsonify(model_to_dto(updated_log_alteracao))

    @log_alteracoes_blueprint.route('/log_alteracoes/<int:log_alteracao_id>', methods=['DELETE'])
    def delete_log_alteracao(log_alteracao_id):
        service.delete_log_alteracao(log_alteracao_id)
        return '', 204

    return log_alteracoes_blueprint