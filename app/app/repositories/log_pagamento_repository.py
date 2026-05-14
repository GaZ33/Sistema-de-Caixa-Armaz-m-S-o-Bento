from abc import ABC, abstractmethod
from typing import List
from app.models import LogPagamento
from app import db

class LogPagamentoRepository(ABC):
    @abstractmethod
    def create(self, log_pagamento: LogPagamento) -> LogPagamento:
        pass

    @abstractmethod
    def get_all(self) -> List[LogPagamento]:
        pass

    @abstractmethod
    def get_by_id(self, log_pagamento_id: int) -> LogPagamento:
        pass

    @abstractmethod
    def update(self, log_pagamento: LogPagamento) -> LogPagamento:
        pass

    @abstractmethod
    def delete(self, log_pagamento_id: int) -> None:
        pass

class SQLAlchemyLogPagamentoRepository(LogPagamentoRepository):
    def create(self, log_pagamento):
        db.session.add(log_pagamento)
        db.session.commit()
        return log_pagamento

    def delete(self, log_pagamento_id):
        log_pagamento = self.get_by_id(log_pagamento_id)
        if log_pagamento:
            db.session.delete(log_pagamento)
            db.session.commit()

    def get_all(self):
        return LogPagamento.query.all()

    def get_by_id(self, log_pagamento_id):
        return LogPagamento.query.get(log_pagamento_id)

    def update(self, log_pagamento_id, data):
        log_pagamento = self.get_by_id(log_pagamento_id)
        if log_pagamento:
            for key, value in data.items():
                setattr(log_pagamento, key, value)
            db.session.commit()
        return log_pagamento