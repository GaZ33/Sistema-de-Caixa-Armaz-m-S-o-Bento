from app.repositories.conta_repository import SQLAlchemyContaRepository
from app.models import Conta
from app.core.exceptions import NotFoundException

class ContaService:
    def __init__(self, repository: SQLAlchemyContaRepository):
        self.repository = repository

    def create_conta(self, conta: Conta) -> Conta:
        return self.repository.create(conta)

    def get_all_contas(self):
        return self.repository.get_all()

    def get_conta_by_id(self, conta_id: int) -> Conta:
        conta = self.repository.get_by_id(conta_id)
        if not conta:
            raise NotFoundException(f"Conta with id {conta_id} not found.")
        return conta

    def update_conta(self, conta_id: int, data: dict) -> Conta:
        return self.repository.update(conta_id, data)

    def delete_conta(self, conta_id: int):
        self.repository.delete(conta_id)