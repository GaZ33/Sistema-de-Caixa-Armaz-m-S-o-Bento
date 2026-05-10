from flask import Blueprint, jsonify, request
from app.services.conta_service import ContaService
from app.models import Conta

conta_blueprint = Blueprint('conta', __name__)

def create_conta_controller(service: ContaService):
    @conta_blueprint.route('/contas', methods=['POST'])
    def create_conta():
        data = request.json
        conta = Conta(**data)
        created_conta = service.create_conta(conta)
        return jsonify(created_conta), 201

    @conta_blueprint.route('/contas', methods=['GET'])
    def get_contas():
        contas = service.get_all_contas()
        return jsonify([conta for conta in contas])

    @conta_blueprint.route('/contas/<int:conta_id>', methods=['GET'])
    def get_conta(conta_id):
        conta = service.get_conta_by_id(conta_id)
        return jsonify(conta)

    @conta_blueprint.route('/contas/<int:conta_id>', methods=['PUT'])
    def update_conta(conta_id):
        data = request.json
        conta = Conta(id=conta_id, **data)
        updated_conta = service.update_conta(conta)
        return jsonify(updated_conta)

    @conta_blueprint.route('/contas/<int:conta_id>', methods=['DELETE'])
    def delete_conta(conta_id):
        service.delete_conta(conta_id)
        return '', 204

    return conta_blueprint