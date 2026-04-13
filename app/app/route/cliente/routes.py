from flask import render_template, request, Blueprint, jsonify
from app import app, db
from app.models import Cliente

cliente_blp = Blueprint('cliente', __name__, url_prefix='/cliente')


# Retornando a página de clientes
@cliente_blp.route('/index.html')
def index():
    return render_template('clientes/index.html')


# Rota para listagem de clientes
@cliente_blp.route('/', methods=['GET'])
def list_clientes():
    clientes = Cliente.query.all()
    return jsonify({
        "message": "Lista de clientes",
        "clientes": [c.to_dict() for c in clientes]
    }), 200


# Rota para busca de cliente por ID
@cliente_blp.route('/<int:id>', methods=['GET'])
def get_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    return jsonify(cliente.to_dict()), 200


# Rota para criação de cliente
@cliente_blp.route('/', methods=['POST'])
def create():
    data = request.get_json()

    if not data:
        return jsonify({"message": "Dados inválidos"}), 400

    novo_cliente = Cliente(
        Nome=data.get('Nome'),
        CPF=data.get('CPF'),
        Telefone=data.get('Telefone'),
        Email=data.get('Email')
    )

    db.session.add(novo_cliente)
    db.session.commit()

    return jsonify({
        "message": "Cliente criado com sucesso!",
        "cliente": novo_cliente.to_dict()
    }), 201


# Rota para atualização de cliente
@cliente_blp.route('/<int:id>', methods=['PUT'])
def update(id):
    cliente = Cliente.query.get_or_404(id)
    data = request.get_json()

    if not data:
        return jsonify({"message": "Dados inválidos"}), 400

    if 'Nome' in data:
        cliente.Nome = data['Nome']
    if 'CPF' in data:
        cliente.CPF = data['CPF']
    if 'Telefone' in data:
        cliente.Telefone = data['Telefone']
    if 'Email' in data:
        cliente.Email = data['Email']

    db.session.commit()

    return jsonify({
        "message": "Cliente atualizado com sucesso!",
        "cliente": cliente.to_dict()
    }), 200


# Rota para deleção de cliente
@cliente_blp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({"message": f"Cliente {id} deletado com sucesso!"}), 200