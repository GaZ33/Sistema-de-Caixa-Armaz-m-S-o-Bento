from flask import Blueprint, jsonify, request
from app.app.services.user_service import UserService
from app.app.domain.user import User

user_blueprint = Blueprint('user', __name__)

def create_user_controller(service: UserService):
    @user_blueprint.route('/users', methods=['POST'])
    def create_user():
        data = request.json
        user = User(**data)
        created_user = service.create_user(user)
        return jsonify(created_user.model_dump()), 201

    @user_blueprint.route('/users', methods=['GET'])
    def get_users():
        users = service.get_all_users()
        return jsonify([user.model_dump() for user in users])

    @user_blueprint.route('/users/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        user = service.get_user_by_id(user_id)
        return jsonify(user.model_dump())

    @user_blueprint.route('/users/<int:user_id>', methods=['PUT'])
    def update_user(user_id):
        data = request.json
        user = User(id=user_id, **data)
        updated_user = service.update_user(user)
        return jsonify(updated_user.model_dump())

    @user_blueprint.route('/users/<int:user_id>', methods=['DELETE'])
    def delete_user(user_id):
        service.delete_user(user_id)
        return '', 204

    return user_blueprint