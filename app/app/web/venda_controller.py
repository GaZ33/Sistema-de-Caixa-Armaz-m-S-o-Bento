from datetime import UTC, datetime

from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from app import db
from app.models import Conta, Produto, ProdutoConta
from app.web.dto import model_to_dto, models_to_dtos

venda_blueprint = Blueprint('venda', __name__)


@venda_blueprint.route('/venda/finalizar', methods=['POST'])
@login_required
def finalizar_venda():
    payload = request.get_json(silent=True) or {}
    carrinho = payload.get('carrinho') or []
    forma_pagamento = payload.get('forma_pagamento')
    cliente_id = payload.get('cliente_id')

    if not carrinho:
        return jsonify({'error': 'Carrinho vazio.'}), 400

    itens_validos = []
    total = 0.0

    for item in carrinho:
        produto_id = item.get('id')
        quantidade = float(item.get('qtd') or 0)
        produto = db.session.get(Produto, produto_id)

        if not produto:
            return jsonify({'error': f'Produto {produto_id} nao encontrado.'}), 404

        preco_unitario = float(produto.preco_unidade)
        subtotal = preco_unitario * quantidade
        total += subtotal
        itens_validos.append((produto, quantidade, preco_unitario, subtotal))

    itens_criados = []

    try:
        pendurar = payload.get('pendurar', False)
        conta = Conta(
            funcionario=current_user.id,
            cliente=cliente_id,
            data_criacao=datetime.now(UTC),
            data_fechamento=None if pendurar else datetime.now(UTC),
            status='aberta' if pendurar else 'fechada',
            valor_total=total,
        )
        db.session.add(conta)
        db.session.flush()

        for produto, quantidade, preco_unitario, subtotal in itens_validos:
            produto_conta = ProdutoConta(
                conta_id=conta.id,
                produto_id=produto.id,
                quantidade=quantidade,
                preco_unitario=preco_unitario,
                subtotal=subtotal,
            )
            db.session.add(produto_conta)
            itens_criados.append(produto_conta)

        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return jsonify({
        'message': 'Venda finalizada com sucesso.',
        'conta': model_to_dto(conta),
        'itens': models_to_dtos(itens_criados),
        'forma_pagamento': forma_pagamento,
    }), 201
