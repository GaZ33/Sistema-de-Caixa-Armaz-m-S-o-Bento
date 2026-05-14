from app.models import Modulo  # Supondo que o modelo Modulo esteja definido em models.py
from app import db

class SQLAlchemyModuloRepository:
    def create(self, modulo):
        db.session.add(modulo)
        db.session.commit()
        return modulo

    def delete(self, modulo_id):
        modulo = self.get_by_id(modulo_id)
        if modulo:
            db.session.delete(modulo)
            db.session.commit()

    def get_all(self):
        return Modulo.query.all()

    def get_by_id(self, modulo_id):
        return Modulo.query.get(modulo_id)

    def update(self, modulo_id, data):
        modulo = self.get_by_id(modulo_id)
        if modulo:
            for key, value in data.items():
                setattr(modulo, key, value)
            db.session.commit()
        return modulo