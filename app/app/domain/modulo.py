from pydantic import BaseModel
from typing import Optional

class Modulo(BaseModel):
    idmodulo: Optional[int] = None
    nome: str
    codigo: str