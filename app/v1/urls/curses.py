from fastapi import APIRouter, HTTPException
from fastapi import Depends
from app.v1.urls.depends import pegar_sessao, verificar_token
from app.v1.urls.schemas import CursosSchema
from app.models import Curso, Matricula, Usuario

curses_router = APIRouter(prefix='/v1/curses',tags=['curses'])

@curses_router.get('/lista_curso')
async def curso(session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    curso = session.query(Curso).all()
    return [
        {
            "id": item.id,
            "nome": item.nome,
            "descricao": item.descricao,
            "carga_horaria": item.carga_horaria,
            "usuario": item.usuario,
        }
        for item in curso
    ]

@curses_router.get('/meus_cursos')
async def meus_cursos(session=Depends(pegar_sessao), usuario: Usuario=Depends(verificar_token)):
    if usuario.papel == "Aluno":
        cursos = (
            session.query(Curso)
            .join(Matricula, Matricula.curso_id == Curso.id)
            .filter(Matricula.aluno_id == usuario.id)
            .all()
        )
    elif usuario.papel == "Instrutor":
        cursos = session.query(Curso).filter(Curso.usuario == usuario.id).all()
    else:
        cursos = session.query(Curso).all()
    return [
        {
            "id": item.id,
            "nome": item.nome,
            "descricao": item.descricao,
            "carga_horaria": item.carga_horaria,
            "usuario": item.usuario,
        }
        for item in cursos
    ]

@curses_router.post('/{curso_id}/matricular')
async def matricular_em_curso(
    curso_id: int,
    session=Depends(pegar_sessao),
    usuario: Usuario=Depends(verificar_token),
):
    if usuario.papel != "Aluno":
        raise HTTPException(status_code=403, detail="Somente alunos podem se matricular")

    curso = session.query(Curso).filter(Curso.id == curso_id).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")

    matricula = session.query(Matricula).filter(
        Matricula.aluno_id == usuario.id,
        Matricula.curso_id == curso_id,
    ).first()
    if matricula:
        raise HTTPException(status_code=400, detail="Você já está matriculado neste curso")

    session.add(Matricula(aluno_id=usuario.id, curso_id=curso_id))
    session.commit()
    return {"Mensagem": f"Matrícula realizada no curso {curso.nome}"}
@curses_router.post('/criar_cursos')
async def criar_cursos(curso_schema: CursosSchema, session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    if usuario.papel not in {"Instrutor", "Administrador"}:
        raise HTTPException(status_code=403, detail="Somente instrutores podem criar cursos")

    curso = session.query(Curso).filter(Curso.nome == curso_schema.nome).first()
    if curso :
        raise HTTPException(status_code=400, detail='Já existe um curso com esse nome')
   
    novo_curso= Curso(nome=curso_schema.nome , descricao=curso_schema.descricao, carga_horaria=curso_schema.carga_horaria ,usuario=usuario.id)
    session.add(novo_curso)
    session.commit()
    return {'Mensagem': f'Curso {curso_schema.nome} cadastrado com sucesso'}

@curses_router.get('/lista_curso')
async def curso(session=Depends(pegar_sessao), usuario: Usuario=Depends(verificar_token)):
    cursos = session.query(Curso).all()
    return [
        {
            "id": item.id,
            "nome": item.nome,
            "descricao": item.descricao,
            "carga_horaria": item.carga_horaria,
            "usuario": item.usuario,
        }
        for item in cursos
    ]


@curses_router.get('/meus_cursos')
async def meus_cursos(session=Depends(pegar_sessao), usuario: Usuario=Depends(verificar_token)):
    if usuario.papel == "Aluno":
        cursos = (
            session.query(Curso)
            .join(Matricula, Matricula.curso_id == Curso.id)
            .filter(Matricula.aluno_id == usuario.id)
            .all()
        )
    elif usuario.papel == "Instrutor":
        cursos = session.query(Curso).filter(Curso.usuario == usuario.id).all()
    else:
        cursos = session.query(Curso).all()

    return [
        {
            "id": item.id,
            "nome": item.nome,
            "descricao": item.descricao,
            "carga_horaria": item.carga_horaria,
            "usuario": item.usuario,
        }
        for item in cursos
    ]

