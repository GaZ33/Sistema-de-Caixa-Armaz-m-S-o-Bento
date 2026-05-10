from pydantic import BaseModel
from typing import Optional

class ProdutoConta(BaseModel):
    id: Optional[int] = None
    conta_id: int
    produto_id: int
    quantidade: float
    preco_unitario: float
    subtotal: float