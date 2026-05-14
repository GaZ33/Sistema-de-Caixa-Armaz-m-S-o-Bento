from app.models import PerfilAcessos  # Supondo que o modelo PerfilAcessos esteja definido em models.py
from app import db

class SQLAlchemyPerfilAcessosRepository:
    def create(self, perfil_acessos):
        db.session.add(perfil_acessos)
        db.session.commit()
        return perfil_acessos

    def delete(self, perfil_acessos_id):
        perfil_acessos = self.get_by_id(perfil_acessos_id)
        if perfil_acessos:
            db.session.delete(perfil_acessos)
            db.session.commit()

    def get_all(self):
        return PerfilAcessos.query.all()

    def get_by_id(self, perfil_acessos_id):
        return PerfilAcessos.query.get(perfil_acessos_id)

    def update(self, perfil_acessos_id, data):
        perfil_acessos = self.get_by_id(perfil_acessos_id)
        if perfil_acessos:
            for key, value in data.items():
                setattr(perfil_acessos, key, value)
            db.session.commit()
        return perfil_acessos