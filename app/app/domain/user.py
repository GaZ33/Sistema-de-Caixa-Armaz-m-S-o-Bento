from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    id: Optional[int] = None
    perfil_id: int
    nome: str
    sobrenome: Optional[str] = None
    email: Optional[EmailStr] = None
    cpf: Optional[str] = None
    senha: str
    salt: str
    username: str
    data_criacao: Optional[str] = None
    data_alteracao: Optional[str] = None
    telefone: Optional[str] = None