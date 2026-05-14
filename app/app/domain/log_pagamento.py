from pydantic import BaseModel
from typing import Optional

class LogPagamento(BaseModel):
    id: Optional[int] = None
    forma_pagamento: Optional[str] = None
    valor_pago: float
    data_pagamento: Optional[str] = None
    conta_id: int