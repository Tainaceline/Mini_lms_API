from fastapi import APIRouter, HTTPException
from fastapi import Depends
from app.v1.urls.depends import pegar_sessao, verificar_token
from app.v1.urls.schemas import CursosSchema
from app.models import Curso, Usuario

curses_router = APIRouter(prefix='/v1/curses',tags=['curses'])

@curses_router.get('/lista_curso')
async def curso(session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    curso = session.query(Curso).all()
    if not curso:
       raise HTTPException(status_code=404,detail="Nenhum curso cadastrado" )
    return curso
@curses_router.post('/criar_cursos')
async def criar_cursos(curso_schema: CursosSchema, session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    curso = session.query(Curso).filter(Curso.nome == curso_schema.nome).first()
    if curso :
        raise HTTPException(status_code=400, detail='Já existe um curso com esse nome')
   
    novo_curso= Curso(nome=curso_schema.nome , descricao=curso_schema.descricao, carga_horaria=curso_schema.carga_horaria ,usuario=curso_schema.usuario)
    session.add(novo_curso)
    session.commit()
    return {'Mensagem': f'Curso {curso_schema.nome} cadastrado com sucesso'}

@curses_router.post('/editar/{id}')
async def editar_curso(id: int, curso_schema: CursosSchema, session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    curso = session.query(Curso).filter(Curso.id == curso_schema.id).first()

    if not curso :
        raise HTTPException(status_code=404, detail='Usuário não encontrado')
    
        
    curso.nome = curso_schema.nome
    curso.descricao = curso_schema.descricao
    curso.carga_horaria = curso_schema.carga_horaria
    
    session.commit()
    return {'Mensagem' : " Atualização Realizada com sucesso"}
@curses_router.get('/buscar_cursos/{id}')
async def buscar_cursos(id: int, session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    curso = session.query(Curso).filter(Curso.id == id).first()
    if curso :
        return {'Mensagem': f"Curso {curso.id} : Nome : {curso.nome}, encontrado com sucesso"}
    else :
        raise HTTPException(status_code=404, detail='Curso não encontrado')

@curses_router.post('/deletar/{id}')
async def deletar_cursos(id: int, session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    curso = session.query(Curso).filter(Curso.id == id).first()
    if not curso:
        raise HTTPException(status_code=404,detail='Não existe Usuário')
    session.delete(curso)
    session.commit
    return {'Mensagem': 'Curso deletado com sucesso'}
    
