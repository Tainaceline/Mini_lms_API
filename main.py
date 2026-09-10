from fastapi import FastAPI

app = FastAPI()

from app.v1.urls.users import user_router
from app.v1.urls.auth import auth_router

app.include_router(user_router)
app.include_router(auth_router)
