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
