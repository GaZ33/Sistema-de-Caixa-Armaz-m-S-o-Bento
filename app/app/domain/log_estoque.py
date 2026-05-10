from pydantic import BaseModel
from typing import Optional

class LogEstoque(BaseModel):
    id: Optional[int] = None
    estoque_id: int
    movimentacao: Optional[str] = None
    quantidade: Optional[float] = None
    motivo: Optional[str] = None