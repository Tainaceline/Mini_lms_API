from fastapi import FastAPI
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth2_schema = OAuth2PasswordBearer(tokenUrl='/v1/auth/login_form')


from app.v1.urls.users import user_router
from app.v1.urls.auth import auth_router
from app.v1.urls.curses import curses_router

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(curses_router)
