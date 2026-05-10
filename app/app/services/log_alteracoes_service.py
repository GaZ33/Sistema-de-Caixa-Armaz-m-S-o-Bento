from app.repositories.log_alteracoes_repository import LogAlteracoesRepository
from app.models import LogAlteracoes
from app.core.exceptions import NotFoundException

class LogAlteracoesService:
    def __init__(self, repository: LogAlteracoesRepository):
        self.repository = repository

    def create_log_alteracao(self, log_alteracao: LogAlteracoes) -> LogAlteracoes:
        return self.repository.create(log_alteracao)

    def get_all_logs_alteracoes(self):
        return self.repository.get_all()

    def get_log_alteracao_by_id(self, log_alteracao_id: int) -> LogAlteracoes:
        log_alteracao = self.repository.get_by_id(log_alteracao_id)
        if not log_alteracao:
            raise NotFoundException(f"LogAlteracoes with id {log_alteracao_id} not found.")
        return log_alteracao

    def update_log_alteracao(self, log_alteracao: LogAlteracoes) -> LogAlteracoes:
        return self.repository.update(log_alteracao)

    def delete_log_alteracao(self, log_alteracao_id: int):
        self.repository.delete(log_alteracao_id)