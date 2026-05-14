from pydantic import BaseModel
from typing import Optional

class Estoque(BaseModel):
    id: Optional[int] = None
    produto_id: int
    quantidade_atual: float
    quantidade_minima: Optional[float] = None
    data_alteracao: Optional[str] = None