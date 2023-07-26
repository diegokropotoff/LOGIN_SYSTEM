from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

USUARIO = 'root'
SENHA = ''
HOST = 'localhost'
BANCO = 'aulaspythonfull'
PORT = 3306

CONN = f"mysql+pymysql://{USUARIO}:{SENHA}@{HOST}:{PORT}/{BANCO}"

engine = create_engine(CONN, echo=False)
Session = sessionmaker(bind=engine)


Base = declarative_base()


class Pessoa(Base):
    __tablename__ = 'Pessoa'
    id = Column(Integer, primary_key=True)
    nome = Column(String(50))
    email = Column(String(30))
    senha = Column(String(100))

Base.metadata.create_all(engine)