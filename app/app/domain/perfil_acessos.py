from pydantic import BaseModel
from typing import Optional

class PerfilAcessos(BaseModel):
    idperfilAcessos: Optional[int] = None
    alterar: Optional[bool] = None
    excluir: Optional[bool] = None
    inserir: Optional[bool] = None
    ler: Optional[bool] = None
    modulo_idmodulo: int
    perfil_id: int