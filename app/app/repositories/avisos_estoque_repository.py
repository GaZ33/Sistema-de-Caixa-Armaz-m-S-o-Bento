from app.models import AvisosEstoque  # Supondo que o modelo AvisosEstoque esteja definido em models.py
from app import db

class SQLAlchemyAvisosEstoqueRepository:
    def create(self, avisos_estoque):
        db.session.add(avisos_estoque)
        db.session.commit()
        return avisos_estoque

    def delete(self, avisos_estoque_id):
        avisos_estoque = self.get_by_id(avisos_estoque_id)
        if avisos_estoque:
            db.session.delete(avisos_estoque)
            db.session.commit()

    def get_all(self):
        return AvisosEstoque.query.all()

    def get_by_id(self, avisos_estoque_id):
        return AvisosEstoque.query.get(avisos_estoque_id)

    def update(self, avisos_estoque_id, data):
        avisos_estoque = self.get_by_id(avisos_estoque_id)
        if avisos_estoque:
            for key, value in data.items():
                setattr(avisos_estoque, key, value)
            db.session.commit()
        return avisos_estoque