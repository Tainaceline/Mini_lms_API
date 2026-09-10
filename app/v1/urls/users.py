from fastapi import APIRouter,HTTPException
from fastapi import Depends
from app.v1.urls.schemas import UsuarioSchema
from app.v1.urls.depends import pegar_sessao
from app.models import Usuario
user_router = APIRouter(prefix='/v1/user',tags=['user'])

@user_router.get('/')
async def usuarios (session= Depends(pegar_sessao)):
    usuario = session.query(Usuario).all()
    return {'mensagem' : 'Esses são todos os registros de usuários'}

@user_router.post('/criar_conta')
async def criar_conta(usuario_schema : UsuarioSchema, session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()

    if usuario :
        raise HTTPException (status_code=400 , detail="Já existe um Usuario com esse email")
    else :
        novo_usuario = Usuario(usuario_schema
        .nome,usuario_schema.email, usuario_schema.senha, usuario_schema.papel, usuario_schema.ativo)
        session.add(novo_usuario)
        session.commit()
        return {"Mensagem": f"Usuário: {usuario_schema.nome} cadastrado(a) com sucesso"}

@user_router.get('/{id}')
async def buscar_usuario(id : int, session = Depends(pegar_sessao)):
    
    usuario = session.query(Usuario).filter(Usuario.id == id).first()
    if not usuario :
        raise HTTPException(status_code=400, detail= 'Usuário não encontrado')
    return {'mensagem': f'Usuário achado com sucesso, {usuario.nome}'}

@user_router.put("/editar/{id}")
async def editar_usuario(id: int, usario_schema : UsuarioSchema ,session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(
            status_code=404,
            detail='Usuário não encontrado'
        )
    usuario.nome = usario_schema.nome
    usuario.email = usuario_schema.email
    usuario.senha = usuario_schema.senha
    usuario.ativo = usuario_schema.papel
    usuario.papel = usuario_schema.ativo
    session.commit()
    return {'Mensagem' : " Atualização Realizada com sucesso"}

@user_router.delete('/deletar/{id}')
async def deletar_usuario(id: int, session=Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404,detail='Não existe Usuário')
    session.delete(usuario)
    session.commit()
    return {'Mensagem': 'Usuário deletado com sucesso'}