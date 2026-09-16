from fastapi import Depends,HTTPException
from sqlalchemy.orm import sessionmaker
from app.models import db,Usuario
from config import SECRET_KEY, ALGORITHM
from jose import jwt,JWTError

from main import oauth2_schema


def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally : 
        session.close()

def verificar_token(token: str = Depends(oauth2_schema), session = Depends(pegar_sessao)):
    try:
        dic_infor = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id_usuario = dic_info.get('sub')
        tipo_token = dic_info.get("type")
        if not id_usuario:
            raise HTTPException(status_code=401,detail="Token inválido")

    except JWTError :
        raise HTTPException(status_code=401, detail='Acesso negado')

    usuario = session.query(Usuario).filter(Usuario.id == int(id_usuario)).first()

    if not usuario:

        raise HTTPException(
            status_code=401,
            detail="Usuário inválido"
        )

    return usuario