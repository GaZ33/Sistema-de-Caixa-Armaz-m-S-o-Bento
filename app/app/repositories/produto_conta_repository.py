from app.models import ProdutoConta  # Supondo que o modelo ProdutoConta esteja definido em models.py
from app import db

class SQLAlchemyProdutoContaRepository:
    def create(self, produto_conta):
        db.session.add(produto_conta)
        db.session.commit()
        return produto_conta

    def delete(self, produto_conta_id):
        produto_conta = self.get_by_id(produto_conta_id)
        if produto_conta:
            db.session.delete(produto_conta)
            db.session.commit()

    def get_all(self):
        return ProdutoConta.query.all()

    def get_by_id(self, produto_conta_id):
        return ProdutoConta.query.get(produto_conta_id)

    def update(self, produto_conta_id, data):
        produto_conta = self.get_by_id(produto_conta_id)
        if produto_conta:
            for key, value in data.items():
                setattr(produto_conta, key, value)
            db.session.commit()
        return produto_conta