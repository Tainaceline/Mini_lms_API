from fastapi import Depends
from sqlalchemy.orm import sessionmaker
from app.models import db

def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally : 
        session.close()