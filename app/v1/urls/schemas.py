from pydantic import BaseModel
from typing import Optional


class UsuarioSchema(BaseModel):
    nome : str
    senha : str
    email : str
    papel : str
    ativo : Optional[bool]

    class config:
        from_attributes = True
class LoginSchema (BaseModel):
    email : str
    senha : str


    class config:
        from_attributes = True