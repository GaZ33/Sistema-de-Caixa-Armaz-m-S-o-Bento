from abc import ABC, abstractmethod
from typing import List
from app.models import LogAlteracoes
from app import db

class LogAlteracoesRepository(ABC):
    @abstractmethod
    def create(self, log_alteracao: LogAlteracoes) -> LogAlteracoes:
        pass

    @abstractmethod
    def get_all(self) -> List[LogAlteracoes]:
        pass

    @abstractmethod
    def get_by_id(self, log_alteracao_id: int) -> LogAlteracoes:
        pass

    @abstractmethod
    def update(self, log_alteracao: LogAlteracoes) -> LogAlteracoes:
        pass

    @abstractmethod
    def delete(self, log_alteracao_id: int) -> None:
        pass

class SQLAlchemyLogAlteracoesRepository(LogAlteracoesRepository):
    def create(self, log_alteracoes):
        db.session.add(log_alteracoes)
        db.session.commit()
        return log_alteracoes

    def delete(self, log_alteracoes_id):
        log_alteracoes = self.get_by_id(log_alteracoes_id)
        if log_alteracoes:
            db.session.delete(log_alteracoes)
            db.session.commit()

    def get_all(self):
        return LogAlteracoes.query.all()

    def get_by_id(self, log_alteracoes_id):
        return LogAlteracoes.query.get(log_alteracoes_id)

    def update(self, log_alteracoes_id, data):
        log_alteracoes = self.get_by_id(log_alteracoes_id)
        if log_alteracoes:
            for key, value in data.items():
                setattr(log_alteracoes, key, value)
            db.session.commit()
        return log_alteracoes