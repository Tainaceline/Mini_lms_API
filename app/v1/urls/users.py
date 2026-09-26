from fastapi import APIRouter, HTTPException, Depends
from app.v1.urls.schemas import UsuarioSchema
from app.v1.urls.depends import pegar_sessao, verificar_token
from app.models import Usuario
from main import bcrypt_context

user_router = APIRouter(prefix='/v1/user',tags=['user'])

@user_router.get('/')
async def usuarios(
    session=Depends(pegar_sessao),
    usuario_atual: Usuario = Depends(verificar_token),
):
    if usuario_atual.papel != "Administrador":
        raise HTTPException(status_code=403, detail="Acesso permitido apenas para administradores")

    registros = session.query(Usuario).all()
    return [
        {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "papel": usuario.papel,
            "ativo": usuario.ativo,
        }
        for usuario in registros
    ]

@user_router.post('/criar_conta')
async def criar_conta(usuario_schema : UsuarioSchema, session = Depends(pegar_sessao)):
    if usuario_schema.papel != "Aluno":
        raise HTTPException(status_code=403, detail="O cadastro público é permitido apenas para alunos")

    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()

    if usuario :
        raise HTTPException (status_code=400 , detail="Já existe um Usuario com esse email")
    else :
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(nome =usuario_schema.nome,email=usuario_schema.email,senha = senha_criptografada, papel=usuario_schema.papel,ativo= usuario_schema.ativo)
        session.add(novo_usuario)
        session.commit()
        return {"Mensagem": f"Usuário: {usuario_schema.nome} cadastrado(a) com sucesso"}

@user_router.post('/admin/criar')
async def criar_usuario_admin(
    usuario_schema: UsuarioSchema,
    session=Depends(pegar_sessao),
    usuario_atual: Usuario=Depends(verificar_token),
):
    if usuario_atual.papel != "Administrador":
        raise HTTPException(status_code=403, detail="Acesso permitido apenas para administradores")

    usuario_existente = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Já existe um usuário com esse email")

    novo_usuario = Usuario(
        nome=usuario_schema.nome,
        email=usuario_schema.email,
        senha=bcrypt_context.hash(usuario_schema.senha),
        papel=usuario_schema.papel,
        ativo=usuario_schema.ativo,
    )
    session.add(novo_usuario)
    session.commit()
    return {"Mensagem": f"Usuário {usuario_schema.nome} criado com sucesso"}

@user_router.get('/{id}')
async def buscar_usuario(
    id: int,
    session=Depends(pegar_sessao),
    usuario_atual: Usuario=Depends(verificar_token),
):
    if usuario_atual.papel != "Administrador":
        raise HTTPException(status_code=403, detail="Acesso permitido apenas para administradores")
    
    usuario = session.query(Usuario).filter(Usuario.id == id).first()
    if not usuario :
        raise HTTPException(status_code=400, detail= 'Usuário não encontrado')
    return {'mensagem': f'Usuário achado com sucesso, {usuario.nome}'}

@user_router.put("/editar/{id}")
async def editar_usuario(
    id: int,
    usuario_schema: UsuarioSchema,
    session=Depends(pegar_sessao),
    usuario_atual: Usuario=Depends(verificar_token),
):
    if usuario_atual.papel != "Administrador":
        raise HTTPException(status_code=403, detail="Acesso permitido apenas para administradores")

    usuario = session.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(
            status_code=404,
            detail='Usuário não encontrado'
        )
    usuario.nome = usuario_schema.nome
    usuario.email = usuario_schema.email
    usuario.senha = bcrypt_context.hash(usuario_schema.senha)
    usuario.papel = usuario_schema.papel
    usuario.ativo = usuario_schema.ativo
    session.commit()
    return {'Mensagem' : " Atualização Realizada com sucesso"}

@user_router.delete('/deletar/{id}')
async def deletar_usuario(
    id: int,
    session=Depends(pegar_sessao),
    usuario_atual: Usuario=Depends(verificar_token),
):
    if usuario_atual.papel != "Administrador":
        raise HTTPException(status_code=403, detail="Acesso permitido apenas para administradores")

    usuario = session.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404,detail='Não existe Usuário')
    session.delete(usuario)
    session.commit()
    return {'Mensagem': 'Usuário deletado com sucesso'}