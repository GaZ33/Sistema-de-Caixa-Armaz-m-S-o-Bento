from flask import Blueprint, jsonify, redirect, render_template, request, url_for, flash
from flask_login import current_user, login_required, login_user, logout_user

from app.services.user_service import UserService


def create_auth_controller(user_service: UserService):
    auth_blueprint = Blueprint('auth', __name__)

    @auth_blueprint.route('/login', methods=['GET'])
    def login_page():
        if current_user.is_authenticated:
            return redirect(url_for('pages.home'))

        return render_template('login/index.html')

    @auth_blueprint.route('/login', methods=['POST'])
    def login_submit():
        payload = request.get_json(silent=True) or request.form
        identifier = (payload.get('identifier') or '').strip()
        senha = payload.get('senha') or ''
        next_url = request.args.get('next')

        user = user_service.authenticate_user(identifier=identifier, senha=senha)
        if not user:
            message = 'Credenciais invalidas. Verifique usuario/email e senha.'

            if request.is_json:
                return jsonify({'error': message}), 401

            flash(message, 'error')
            return render_template('login/index.html'), 401

        login_user(user)

        if request.is_json:
            return jsonify({'message': 'Login realizado com sucesso.', 'user': user.to_dict()})

        return redirect(next_url or url_for('pages.home'))

    @auth_blueprint.route('/logout', methods=['POST'])
    @login_required
    def logout():
        logout_user()

        if request.is_json:
            return jsonify({'message': 'Logout realizado com sucesso.'})

        return redirect(url_for('auth.login_page'))

    @auth_blueprint.route('/api/session', methods=['GET'])
    def session_info():
        if current_user.is_authenticated:
            return jsonify({'authenticated': True, 'user': current_user.to_dict()})

        return jsonify({'authenticated': False, 'user': None}), 401

    return auth_blueprint
