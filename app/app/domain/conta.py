from pydantic import BaseModel
from typing import Optional

class Conta(BaseModel):
    id: Optional[int] = None
    funcionario: int
    cliente: Optional[int] = None
    data_criacao: str
    data_alteracao: Optional[str] = None
    data_fechamento: Optional[str] = None
    status: str
    valor_total: float