from fastapi import APIRouter, Depends, HTTPException

from app.models import Aula, Curso, Usuario
from app.v1.urls.depends import pegar_sessao, verificar_token
from app.v1.urls.schemas import AulaSchema

aulas_router = APIRouter(prefix="/v1/aulas", tags=["aulas"])


@aulas_router.get("/")
async def listar_aulas(
    session=Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token),
):
    if usuario.papel != "Administrador":
        raise HTTPException(status_code=403, detail="Acesso permitido apenas para administradores")

    aulas = session.query(Aula).order_by(Aula.curso_id, Aula.ordem).all()
    return [
        {
            "id": aula.id,
            "titulo": aula.titulo,
            "conteudo": aula.conteudo,
            "ordem": aula.ordem,
            "curso_id": aula.curso_id,
        }
        for aula in aulas
    ]


@aulas_router.post("/")
async def criar_aula(
    aula_schema: AulaSchema,
    session=Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token),
):
    if usuario.papel != "Administrador":
        raise HTTPException(status_code=403, detail="Acesso permitido apenas para administradores")

    curso = session.query(Curso).filter(Curso.id == aula_schema.curso_id).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")

    aula = Aula(
        titulo=aula_schema.titulo,
        conteudo=aula_schema.conteudo,
        ordem=aula_schema.ordem,
        curso_id=aula_schema.curso_id,
    )
    session.add(aula)
    session.commit()
    return {"Mensagem": f"Aula {aula.titulo} criada com sucesso"}