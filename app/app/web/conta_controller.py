from flask import Blueprint, jsonify, request
from app.services.conta_service import ContaService
from app.models import Conta
from app.core.exceptions import NotFoundException
from app.web.dto import model_to_dto, models_to_dtos

conta_blueprint = Blueprint('conta', __name__)

def create_conta_controller(service: ContaService):
    @conta_blueprint.route('/contas', methods=['POST'])
    def create_conta():
        data = request.get_json(silent=True) or {}
        conta = Conta(**data)
        created_conta = service.create_conta(conta)
        return jsonify(model_to_dto(created_conta)), 201

    @conta_blueprint.route('/contas', methods=['GET'])
    def get_contas():
        contas = service.get_all_contas()
        return jsonify(models_to_dtos(contas))

    @conta_blueprint.route('/contas/<int:conta_id>', methods=['GET'])
    def get_conta(conta_id):
        try:
            conta = service.get_conta_by_id(conta_id)
            return jsonify(model_to_dto(conta))
        except NotFoundException as ex:
            return jsonify({'error': str(ex)}), 404

    @conta_blueprint.route('/contas/<int:conta_id>', methods=['PUT'])
    def update_conta(conta_id):
        data = request.get_json(silent=True) or {}
        updated_conta = service.update_conta(conta_id, data)
        if not updated_conta:
            return jsonify({'error': f'Conta with id {conta_id} not found.'}), 404
        return jsonify(model_to_dto(updated_conta))

    @conta_blueprint.route('/contas/<int:conta_id>', methods=['DELETE'])
    def delete_conta(conta_id):
        service.delete_conta(conta_id)
        return '', 204

        @conta_blueprint.route('/contas/cliente/<int:cliente_id>', methods=['GET'])
        def get_contas_by_cliente(cliente_id):
            contas = service.get_all_contas()
            contas_do_cliente = [c for c in contas if c.cliente == cliente_id]
            return jsonify(models_to_dtos(contas_do_cliente))

    return conta_blueprint