# app/models/schemas.py (parte relevante)
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import date

# Importa a Base do seu arquivo database.py para os modelos SQLAlchemy
from ..database import Base
from sqlalchemy import Column, Integer, String, DECIMAL, Date, Boolean

# ----------------------------------------------------------------------
# Modelos SQLAlchemy para as tabelas do banco de dados
# ----------------------------------------------------------------------
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(80), unique=True, index=True, nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    hashed_password = Column(String(120), nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"

# NOVO: Modelo SQLAlchemy para Contratacao
class ContratacaoORM(Base): # Renomeado para evitar conflito com Pydantic BaseModel
    __tablename__ = "contratacoesPncpUfca" # Nome da sua tabela no banco de dados

    id_compra = Column(String(255), primary_key=True, index=True)
    ano_compra = Column(Integer, nullable=False)
    objeto_compra = Column(String(1024), nullable=False)
    valor_estimado = Column(DECIMAL(18, 2), nullable=True) # Exemplo de DECIMAL

    # Adicione outras colunas da sua tabela 'contratacoesPncpUfca' aqui,
    # caso você precise mapeá-las para interagir com elas via ORM.
    # Ex:
    # data_publicacao = Column(Date, nullable=True)

# ----------------------------------------------------------------------
# Esquemas Pydantic para Autenticação (Input/Output da API)
# ----------------------------------------------------------------------
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

# ----------------------------------------------------------------------
# Seus outros esquemas Pydantic existentes para dados da PROAD
# ----------------------------------------------------------------------
class Contratacao(BaseModel): # Este é o Pydantic BaseModel, usado para validar a entrada/saída da API
    id_compra: str
    ano_compra: int
    objeto_compra: str
    valor_estimado: Optional[Decimal]

# ... (todos os seus outros esquemas Pydantic como ItemContratacao, ResultadoItensContratacao, etc.) ...
# Certifique-se de que todos os Pydantic BaseModels para suas tabelas
# estejam aqui, e que se precisar de modelos ORM para eles,
# você os defina como ContratacaoORM acima.
