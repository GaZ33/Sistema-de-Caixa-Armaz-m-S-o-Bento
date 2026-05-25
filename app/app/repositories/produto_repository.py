from app.models import Produto  # Supondo que o modelo Produto esteja definido em models.py
from app import db

class SQLAlchemyProdutoRepository:
    def create(self, produto):
        db.session.add(produto)
        db.session.commit()
        return produto

    def delete(self, produto_id):
        produto = self.get_by_id(produto_id)
        if produto:
            db.session.delete(produto)
            db.session.commit()

    def get_all(self):
        return Produto.query.all()

    def get_by_id(self, produto_id):
        return db.session.get(Produto, produto_id)

    def update(self, produto_id, data):
        produto = self.get_by_id(produto_id)
        if produto:
            for key, value in data.items():
                setattr(produto, key, value)
            db.session.commit()
        return produto

    def buscar(self, query):
        return Produto.query.filter((Produto.nome.ilike(f"%{query}%")) | (Produto.codigo.ilike(f"%{query}%"))).all()