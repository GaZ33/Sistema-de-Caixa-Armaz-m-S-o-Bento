from app.models import LogEstoque  # Supondo que o modelo LogEstoque esteja definido em models.py
from app import db

class SQLAlchemyLogEstoqueRepository:
    def create(self, log_estoque):
        db.session.add(log_estoque)
        db.session.commit()
        return log_estoque

    def delete(self, log_estoque_id):
        log_estoque = self.get_by_id(log_estoque_id)
        if log_estoque:
            db.session.delete(log_estoque)
            db.session.commit()

    def get_all(self):
        return LogEstoque.query.all()

    def get_by_id(self, log_estoque_id):
        return LogEstoque.query.get(log_estoque_id)

    def update(self, log_estoque_id, data):
        log_estoque = self.get_by_id(log_estoque_id)
        if log_estoque:
            for key, value in data.items():
                setattr(log_estoque, key, value)
            db.session.commit()
        return log_estoque