from app.models import Estoque  # Supondo que o modelo Estoque esteja definido em models.py
from app import db

class SQLAlchemyEstoqueRepository:
    def create(self, estoque):
        db.session.add(estoque)
        db.session.commit()
        return estoque

    def delete(self, estoque_id):
        estoque = self.get_by_id(estoque_id)
        if estoque:
            db.session.delete(estoque)
            db.session.commit()

    def get_all(self):
        return Estoque.query.all()

    def get_by_id(self, estoque_id):
        return Estoque.query.get(estoque_id)

    def update(self, estoque_id, data):
        estoque = self.get_by_id(estoque_id)
        if estoque:
            for key, value in data.items():
                setattr(estoque, key, value)
            db.session.commit()
        return estoque