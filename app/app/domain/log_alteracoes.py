from pydantic import BaseModel
from typing import Optional

class LogAlteracoes(BaseModel):
    id: Optional[int] = None
    usuario_id: int
    tabela_afetada: Optional[str] = None
    acao: str
    valor_antigo: Optional[str] = None
    valor_novo: Optional[str] = None
    data_evento: str