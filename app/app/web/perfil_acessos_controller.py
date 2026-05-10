from flask import Blueprint, jsonify, request
from app.services.perfil_acessos_service import PerfilAcessosService
from app.models import PerfilAcessos

perfil_acessos_blueprint = Blueprint('perfil_acessos', __name__)

def create_perfil_acessos_controller(service: PerfilAcessosService):
    @perfil_acessos_blueprint.route('/perfil_acessos', methods=['POST'])
    def create_perfil_acessos():
        data = request.json
        perfil_acessos = PerfilAcessos(**data)
        created_perfil_acessos = service.create_perfil_acessos(perfil_acessos)
        return jsonify(created_perfil_acessos), 201

    @perfil_acessos_blueprint.route('/perfil_acessos', methods=['GET'])
    def get_perfis_acessos():
        perfis_acessos = service.get_all_perfis_acessos()
        return jsonify([perfil_acessos for perfil_acessos in perfis_acessos])

    @perfil_acessos_blueprint.route('/perfil_acessos/<int:perfil_acessos_id>', methods=['GET'])
    def get_perfil_acessos(perfil_acessos_id):
        perfil_acessos = service.get_perfil_acessos_by_id(perfil_acessos_id)
        return jsonify(perfil_acessos)

    @perfil_acessos_blueprint.route('/perfil_acessos/<int:perfil_acessos_id>', methods=['PUT'])
    def update_perfil_acessos(perfil_acessos_id):
        data = request.json
        perfil_acessos = PerfilAcessos(idperfilAcessos=perfil_acessos_id, **data)
        updated_perfil_acessos = service.update_perfil_acessos(perfil_acessos)
        return jsonify(updated_perfil_acessos)

    @perfil_acessos_blueprint.route('/perfil_acessos/<int:perfil_acessos_id>', methods=['DELETE'])
    def delete_perfil_acessos(perfil_acessos_id):
        service.delete_perfil_acessos(perfil_acessos_id)
        return '', 204

    return perfil_acessos_blueprint