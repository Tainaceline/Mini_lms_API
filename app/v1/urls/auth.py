
from fastapi import APIRouter,HTTPException,Depends
from datetime import datetime,timedelta,timezone
from jose import jwt,JWTError
from main import ACCES_TOKEN_EXPIRE_MINUTES, SECRET_KEY,ALGORITHM

from app.models import Usuario
from app.v1.urls.schemas import LoginSchema
from app.v1.urls.depends import pegar_sessao
from app.v1.urls.users import criar_conta

def criar_token(id_usuario,tipo_token: str):
    duracao_token = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_expiracao = datetime.now(timezone.utc) + duracao_token

    dic_info = {'sub':str(id_usuario), 'exp': data_expiracao}
    jwt_codificado = jwt.encode(dic_info,SECRET_KEY,ALGORITHM)
    return jwt_codificado

def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return False

    elif not bcrypt_context.verify(senha, usuario.senha):
        return False

    return usuario

auth_router = APIRouter(prefix='/v1/auth',tags=['auth'])

auth_router.post('/login')
async def login(login_schema :LoginSchema, session = Depends(pegar_sessao)):
     usuario= session.query(Usuario).filter(Usuario.email == login_schema.email).first()
     autenticar_usuario(login.email,login.senha,session)
     if not usuario :
        raise HTTPException(status_code= 401, detail='email ou senha incorretos')
     else:
        acess_token = criar_conta(usuario.id, "access",)
        refresh_token = criar_token(usuario.id,"refresh",duracao_token=timedelta(days=7))
        return{'acess_token' :acess_token, 'token_type' : 'Berrer', "refresh_token": refresh_token}
        
@auth_router.get('/refresh')
async def use_refresh(usuario : Usuario = Depends(verificar_token)):
    acess_token= criar_token(usuario.id,"access",timedel(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"acess_token": acess_token,"token_type " : "Berrer"}
   

