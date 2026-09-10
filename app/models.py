from sqlalchemy import create_engine,Column,Enum,String,Float,ForeignKey,Boolean,Integer,Text
from sqlalchemy.orm import declarative_base


db = create_engine("sqlite:///banco.db")
Base = declarative_base()

class Usuario(Base):
    __tablename__ ="usuarios"

    id = Column('id',Integer,primary_key=True, autoincrement=True,index=True)
    nome = Column('nome',String,nullable=False)
    email = Column ('email', String,unique=True,nullable=False)
    senha = Column('senha', String, nullable=False)
    papel = Column(Enum("Aluno", "Instrutor", "Administrador"),
    nullable=False
)
    ativo = Column('ativo',Boolean)

    def __init__(self,nome,email,senha,papel,ativo=True):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.papel = papel
        self.ativo = ativo

class Curso(Base):
    __tablename__ ='cursos'
    id = Column('id',Integer,primary_key=True,autoincrement=True)
    nome = Column('nome', String,unique=True,nullable=False)
    descricao = Column("descricao",Text,nullable=False)
    carga_horaria = Column("carga_horaria", Integer,nullable=False)
    usuario = Column('usuario',ForeignKey('usuarios.id'))

    def __init__(self,nome,descricao,carga_horaria,usuario):
        self.nome =nome
        self.descricao=descricao
        self.carga_horaria=carga_horaria
        self.usuario=usuario

class Aula(Base):
    __tablename__ = "aulas"

    id = Column(Integer, primary_key=True)
    titulo = Column(String(150), nullable=False,index=True)
    conteudo = Column(Text, nullable=False)
    ordem = Column(Integer, nullable=False)

    curso_id = Column(Integer, ForeignKey("cursos.id"), nullable=False)

    def __init__(self,titulo,conteudo,ordem,curso_id):
        self.titulo = titulo
        self.conteudo =conteudo
        self.ordem=ordem
        self.curso_id = curso_id

class Matricula(Base):
    __tablename__ = "matriculas"

    id = Column(Integer, primary_key=True)

    aluno_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    curso_id = Column(Integer, ForeignKey("cursos.id"), nullable=False)

    def __init__(self,aluno_id,curso_id):
        self.aluno_id=aluno_id
        self.curso_id=curso_id