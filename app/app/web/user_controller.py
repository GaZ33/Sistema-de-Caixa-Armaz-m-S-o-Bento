from flask import Blueprint, jsonify, request
from app.services.user_service import UserService
from app.core.exceptions import NotFoundException, ValidationException
from app.web.dto import model_to_dto, models_to_dtos

user_blueprint = Blueprint('user', __name__)

def create_user_controller(service: UserService):
    @user_blueprint.route('/users', methods=['POST'])
    def create_user():
        try:
            data = request.get_json(silent=True) or {}
            created_user = service.create_user(data)
            return jsonify(model_to_dto(created_user)), 201
        except ValidationException as ex:
            return jsonify({'error': str(ex)}), 400

    @user_blueprint.route('/users', methods=['GET'])
    def get_users():
        users = service.get_all_users()
        return jsonify(models_to_dtos(users))

    @user_blueprint.route('/users/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        try:
            user = service.get_user_by_id(user_id)
            return jsonify(model_to_dto(user))
        except NotFoundException as ex:
            return jsonify({'error': str(ex)}), 404

    @user_blueprint.route('/users/<int:user_id>', methods=['PUT'])
    def update_user(user_id):
        try:
            data = request.get_json(silent=True) or {}
            updated_user = service.update_user(user_id, data)
            return jsonify(model_to_dto(updated_user))
        except NotFoundException as ex:
            return jsonify({'error': str(ex)}), 404
        except ValidationException as ex:
            return jsonify({'error': str(ex)}), 400

    @user_blueprint.route('/users/<int:user_id>', methods=['DELETE'])
    def delete_user(user_id):
        try:
            service.delete_user(user_id)
            return '', 204
        except NotFoundException as ex:
            return jsonify({'error': str(ex)}), 404

    return user_blueprint