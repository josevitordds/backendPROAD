# app/models/schemas.py
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import date

# Importa a Base do seu arquivo database.py para os modelos SQLAlchemy
from ..database import Base
# Importa tipos de coluna do SQLAlchemy e 'func' para funções de agregação
from sqlalchemy import Column, Integer, String, DECIMAL, Date, Boolean, func

# ----------------------------------------------------------------------
# Modelos SQLAlchemy para as tabelas do banco de dados (ORM)
# ----------------------------------------------------------------------
class User(Base):
    """
    Modelo SQLAlchemy para a tabela 'users' no banco de dados.
    Define a estrutura dos usuários que serão armazenados.
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(80), unique=True, index=True, nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    hashed_password = Column(String(120), nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"

class ContratacaoORM(Base):
    """
    Modelo SQLAlchemy para a tabela 'contratacoesPncpUfca' no banco de dados.
    Mapeia as colunas da tabela para atributos Python.
    """
    __tablename__ = "contratacoesPncpUfca"
    id_compra = Column(String(255), primary_key=True, index=True)
    ano_compra = Column(Integer, nullable=False)
    objeto_compra = Column(String(1024), nullable=False)
    valor_estimado = Column(DECIMAL(18, 2), nullable=True)

class ContratosORM(Base):
    """
    Modelo SQLAlchemy para a tabela 'contratosPncpDetalhado' no banco de dados.
    """
    __tablename__ = "contratosPncpDetalhado"
    numero_contrato = Column(String(255), primary_key=True, index=True)
    id_compra = Column(String(255), nullable=False)
    ano_compra = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<Contrato(numero_contrato='{self.numero_contrato}', id_compra='{self.id_compra}')>"

class ItensContratacoesORM(Base):
    """
    Modelo SQLAlchemy para a tabela 'itensContratacoesPncpUfca' no banco de dados.
    """
    __tablename__ = "itensContratacoesPncpUfca"
    id_item = Column(String(255), primary_key=True, index=True)
    id_compra = Column(String(255), nullable=False)
    ano_compra = Column(Integer, nullable=False)
    descricao_item = Column(String(1024), nullable=True)
    quantidade_item = Column(DECIMAL(18, 2), nullable=True)
    valor_unitario_estimado = Column(DECIMAL(18, 2), nullable=True)
    valor_total_estimado = Column(DECIMAL(18, 2), nullable=True)

    def __repr__(self):
        return f"<ItemContratacao(id_item='{self.id_item}', descricao_item='{self.descricao_item}')>"

class ItensContratoORM(Base):
    """
    Modelo SQLAlchemy para a tabela 'itensContratoPncpUfca' no banco de dados.
    """
    __tablename__ = "itensContratoPncpUfca"
    id_compra = Column(String(255), primary_key=True, index=True)
    ano_compra = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<ItemContrato(id_compra='{self.id_compra}', ano_compra={self.ano_compra})>"

class ItensLicitacaoORM(Base):
    """
    Modelo SQLAlchemy para a tabela 'itensLicitacoesUfca' no banco de dados.
    """
    __tablename__ = "itensLicitacoesUfca"
    id_compra = Column(String(255), primary_key=True, index=True)
    ano_compra = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<ItemLicitacao(id_compra='{self.id_compra}', ano_compra={self.ano_compra})>"

class SemLicitacaoORM(Base):
    """
    Modelo SQLAlchemy para a tabela 'compraSemLicitacaoPncp' no banco de dados.
    """
    __tablename__ = "compraSemLicitacaoPncp"
    id_compra = Column(String(255), primary_key=True, index=True)
    ano_compra = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<SemLicitacao(id_compra='{self.id_compra}', ano_compra={self.ano_compra})>"

class ItensSemLicitacaoORM(Base): # <--- ESTA É A CLASSE QUE ESTAVA FALTANDO OU COM PROBLEMA
    """
    Modelo SQLAlchemy para a tabela 'itensCompraSemLicitacaoPncp' no banco de dados.
    Mapeia as colunas da tabela para atributos Python.
    """
    __tablename__ = "itensCompraSemLicitacaoPncp"
    id_compra = Column(String(255), primary_key=True, index=True) # Assumindo id_compra como PK
    ano_compra = Column(Integer, nullable=True) # Ajuste a nulidade conforme seu DB

    def __repr__(self):
        return f"<ItemSemLicitacao(id_compra='{self.id_compra}', ano_compra={self.ano_compra})>"


class ResultadoItensContratacoesORM(Base):
    """
    Modelo SQLAlchemy para a tabela 'resultadoItensContratacoesPncpUfca' no banco de dados.
    """
    __tablename__ = "resultadoItensContratacoesPncpUfca"
    id_compra_item = Column(String(255), primary_key=True, index=True)
    id_compra = Column(String(255), nullable=False)
    data_inclusao = Column(Date, nullable=True)
    quantidade_homologada = Column(Integer, nullable=True)
    valor_unitario_homologado = Column(DECIMAL(18, 2), nullable=True)
    valor_total_homologado = Column(DECIMAL(18, 2), nullable=True)

    def __repr__(self):
        return f"<ResultadoItemContratacao(id_compra_item='{self.id_compra_item}', id_compra='{self.id_compra}')>"

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

class TokenData(BaseModel):
    email: Optional[str] = None

# ----------------------------------------------------------------------
# Seus outros esquemas Pydantic existentes para dados da PROAD
# ----------------------------------------------------------------------
class Contratacao(BaseModel):
    id_compra: str
    ano_compra: int
    objeto_compra: str
    valor_estimado: Optional[Decimal]

    class Config:
        from_attributes = True


class ItemContratacao(BaseModel):
    id_compra_item: str
    id_compra: str
    id_contratacao_pncp: Optional[str]
    codigo_unidade_orgao: Optional[int]
    cnpj_orgao: Optional[str]
    numero_item_pncp: Optional[int]
    numero_item_compra: Optional[int]
    numero_grupo: Optional[int]
    descricao_resumida: Optional[str]
    material_ou_servico: Optional[str]
    nome_material_ou_servico: Optional[str]
    codigo_classe: Optional[int]
    codigo_grupo: Optional[int]
    codigo_item_catalogo: Optional[int]
    descricao_detalhada: Optional[str]
    unidade_medida: Optional[str]
    orcamento_sigiloso: Optional[bool]
    item_categoria_id: Optional[int]
    item_categoria_nome: Optional[str]
    criterio_julgamento_id: Optional[int]
    criterio_julgamento_nome: Optional[str]
    situacao_compra_item: Optional[str]
    situacao_compra_item_nome: Optional[str]
    tipo_beneficio: Optional[str]
    tipo_beneficio_nome: Optional[str]
    incentivo_produtivo_basico: Optional[bool]
    quantidade: Optional[Decimal]
    valor_unitario_estimado: Optional[Decimal]
    valor_total_estimado: Optional[Decimal]
    tem_resultado: Optional[bool]
    codigo_fornecedor: Optional[str]
    nome_fornecedor: Optional[str]
    quantidade_resultado: Optional[Decimal]
    valor_unitario_resultado: Optional[Decimal]
    valor_total_resultado: Optional[Decimal]
    data_inclusao: Optional[date]
    data_atualizacao: Optional[date]
    data_resultado: Optional[date]
    margem_preferencia_normal: Optional[bool]
    percentual_margem_preferencia_normal: Optional[Decimal]
    margem_preferencia_adicional: Optional[bool]
    percentual_margem_preferencia_adicional: Optional[Decimal]
    codigo_ncm: Optional[str]
    descricao_ncm: Optional[str]
    numero_controle_pncp_compra: Optional[str]
    
    class Config:
        from_attributes = True


class ResultadoItensContratacao(BaseModel):
    id_compra_item: str
    id_compra: str
    quantidade_homologada: Optional[int]
    valor_unitario_homologado: Optional[Decimal]
    valor_total_homologado: Optional[Decimal]
    data_inclusao: Optional[date]

    class Config:
        from_attributes = True


class Contratos(BaseModel):
    numero_contrato: str
    id_compra: str
    ano_compra: Optional[int]

    class Config:
        from_attributes = True


class ItensContratos(BaseModel):
    id_compra: str
    ano_compra: Optional[int]

    class Config:
        from_attributes = True


class SemLicitacao(BaseModel):
    id_compra: str
    ano_compra: Optional[int]

    class Config:
        from_attributes = True


class ItensSemLicitacao(BaseModel):
    id_compra: str
    ano_compra: Optional[int]

    class Config:
        from_attributes = True


class Licitacao(BaseModel):
    id_compra: str
    ano_compra: Optional[int]

    class Config:
        from_attributes = True


class ItensLicitacao(BaseModel):
    id_compra: str
    ano_compra: Optional[int]

    class Config:
        from_attributes = True

class DashboardData(BaseModel):
    total_contratacoes: int
    total_homologado: Decimal
    media_economia: Decimal

    class Config:
        from_attributes = True
