from abc import ABC, abstractmethod
from typing import List
from app.models import Conta 
from app import db

class SQLAlchemyContaRepository:
    def create(self, conta):
        db.session.add(conta)
        db.session.commit()
        return conta

    def delete(self, conta_id):
        conta = self.get_by_id(conta_id)
        if conta:
            db.session.delete(conta)
            db.session.commit()

    def get_all(self):
        return Conta.query.all()

    def get_by_id(self, conta_id):
        return Conta.query.get(conta_id)

    def update(self, conta_id, data):
        conta = self.get_by_id(conta_id)
        if conta:
            for key, value in data.items():
                setattr(conta, key, value)
            db.session.commit()
        return conta