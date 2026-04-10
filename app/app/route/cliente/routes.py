from flask import render_template, redirect, url_for, request, session, flash, Blueprint, jsonify, abort, send_from_directory, current_app
from app import app


cliente_blp = Blueprint('cliente', __name__, url_prefix='/cliente')

# Retornando a página de clientes
@cliente_blp.route('/index.html')
def index():
    return render_template('clientes/index.html')

# Rota para listagem de clientes
@cliente_blp.route('/', methods=['GET'])
def list_clientes():
    return jsonify({"message": "Lista de clientes"}), 200

# Rota para busca de cliente por ID
@cliente_blp.route('/<int:id>', methods=['GET'])
def get_cliente(id):
    return jsonify({"message": f"Detalhes do cliente {id}"}), 200

# Rota para criação de cliente
@cliente_blp.route('/', methods=['POST'])
def create():
    return jsonify({"message": "Cliente criado com sucesso!"}), 201

# Rota para atualização de cliente
@cliente_blp.route('/<int:id>', methods=['PUT'])
def update(id):
    return jsonify({"message": f"Cliente {id} atualizado com sucesso!"}), 200

# Rota para deleção de cliente
@cliente_blp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    return jsonify({"message": f"Cliente {id} deletado com sucesso!"}), 200

