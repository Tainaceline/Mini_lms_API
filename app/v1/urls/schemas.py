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
class CursosSchema(BaseModel):
     nome : str
     descricao : str
     carga_horaria : int
     usuario : int
     class config:
        from_attributes = True

class AulaSchema(BaseModel):
    titulo :str
    conteudo : str
    ordem : int
    curso_id : int
    class config:
        from_attributes = True
    
class MatriculaSchema(BaseModel):
    
    aluno_id : int
    curso_id : int
    class config:
        from_attributes = True
