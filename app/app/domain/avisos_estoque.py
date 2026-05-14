from pydantic import BaseModel
from typing import Optional

class AvisosEstoque(BaseModel):
    id: Optional[int] = None
    estoque_id: int
    descricao: Optional[str] = None
    status: Optional[str] = None