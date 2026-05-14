from app.repositories.log_pagamento_repository import LogPagamentoRepository
from app.models import LogPagamento
from app.core.exceptions import NotFoundException

class LogPagamentoService:
    def __init__(self, repository: LogPagamentoRepository):
        self.repository = repository

    def create_log_pagamento(self, log_pagamento: LogPagamento) -> LogPagamento:
        return self.repository.create(log_pagamento)

    def get_all_logs_pagamento(self):
        return self.repository.get_all()

    def get_log_pagamento_by_id(self, log_pagamento_id: int) -> LogPagamento:
        log_pagamento = self.repository.get_by_id(log_pagamento_id)
        if not log_pagamento:
            raise NotFoundException(f"LogPagamento with id {log_pagamento_id} not found.")
        return log_pagamento

    def update_log_pagamento(self, log_pagamento: LogPagamento) -> LogPagamento:
        return self.repository.update(log_pagamento)

    def delete_log_pagamento(self, log_pagamento_id: int):
        self.repository.delete(log_pagamento_id)