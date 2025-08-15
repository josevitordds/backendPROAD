from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import date

from ..database import Base
from sqlalchemy import Column, Integer, String, DECIMAL, Date, Boolean, func

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(80), unique=True, index=True, nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    hashed_password = Column(String(120), nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"

class ContratacaoORM(Base):
    __tablename__ = "contratacoesPncpUfca"
    id_compra = Column(String(255), primary_key=True, index=True)
    ano_compra = Column(Integer, nullable=False)
    objeto_compra = Column(String(1024), nullable=False)
    valor_estimado = Column(DECIMAL(18, 2), nullable=True)

class ContratosORM(Base):
    __tablename__ = "contratosPncpDetalhado"
    numero_contrato = Column(String(255), primary_key=True, index=True)
    id_compra = Column(String(255), nullable=False)
    ano_compra = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<Contrato(numero_contrato='{self.numero_contrato}', id_compra='{self.id_compra}')>"

class ItensContratacoesORM(Base):
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
    __tablename__ = "itensContratoPncpUfca"
    id_compra = Column(String(255), primary_key=True, index=True)
    ano_compra = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<ItemContrato(id_compra='{self.id_compra}', ano_compra={self.ano_compra})>"

class LicitacaoORM(Base):
    __tablename__ = "licitacoesUfca"
    id_compra = Column(String(255), primary_key=True, index=True)
    ano_compra = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<Licitacao(id_compra='{self.id_compra}', ano_compra={self.ano_compra})>"

class ItensLicitacaoORM(Base):
    __tablename__ = "itensLicitacoesUfca"
    id_compra = Column(String(255), primary_key=True, index=True)
    ano_compra = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<ItemLicitacao(id_compra='{self.id_compra}', ano_compra={self.ano_compra})>"

class SemLicitacaoORM(Base):
    __tablename__ = "compraSemLicitacaoPncp"
    id_compra = Column(String(255), primary_key=True, index=True)
    ano_compra = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<SemLicitacao(id_compra='{self.id_compra}', ano_compra={self.ano_compra})>"

class ItensSemLicitacaoORM(Base):
    __tablename__ = "itensCompraSemLicitacaoPncp"
    id_compra = Column(String(255), primary_key=True, index=True) 
    ano_compra = Column(Integer, nullable=True) 

    def __repr__(self):
        return f"<ItemSemLicitacao(id_compra='{self.id_compra}', ano_compra={self.ano_compra})>"


class ResultadoItensContratacoesORM(Base):
    __tablename__ = "resultadoItensContratacoesPncpUfca"
    id_compra_item = Column(String(255), primary_key=True, index=True)
    id_compra = Column(String(255), nullable=False)
    data_inclusao = Column(Date, nullable=True)
    quantidade_homologada = Column(Integer, nullable=True)
    valor_unitario_homologado = Column(DECIMAL(18, 2), nullable=True)
    valor_total_homologado = Column(DECIMAL(18, 2), nullable=True)

    def __repr__(self):
        return f"<ResultadoItemContratacao(id_compra_item='{self.id_compra_item}', id_compra='{self.id_compra}')>"

class MinhaViewORM(Base):
    __tablename__ = "vw_pncpUFCApainel" 
    __table_args__ = {'extend_existing': True} 

    
    id_compra = Column(String(50), primary_key=True, index=True)
    processo = Column(String(100),  nullable=True)
    modalidade_nome = Column(String(100),  nullable=True)
    numero_compra = Column(String(50), nullable=True)
    objeto_compra = Column(String(5000), nullable=True)
    descricao_resumida = Column(String(5000), nullable=True)
    unidade_medida = Column(String(50), nullable=True)
    quantidade_resultado = Column(DECIMAL(15,2), nullable=True)
    quantidade_ufca = Column(DECIMAL(15,2), nullable=True)
    valor_total_resultado = Column(DECIMAL(15,2), nullable=True)
    valor_unitario_estimado = Column(DECIMAL(15,2), nullable=True)
    valor_unitario_resultado = Column(DECIMAL(15,2), nullable=True)
    valor_planejamento = Column(DECIMAL(15,2), nullable=True)
    valor_total_homologado = Column(DECIMAL(15,2), nullable=True)
    nome_fornecedor = Column(String(255), nullable=True)
    numero_item_compra = Column(Integer, nullable=True)
    ni_fornecedor = Column(String(50), nullable=True)
    objeto_resumido = Column(String(5000), nullable=True)
    objeto_TR = Column(String(5000), nullable=True)
    demandante = Column(String(255), nullable=True)
    situacao_compra_item_nome = Column(String(50), nullable=True)
    nome_material_ou_servico = Column(String(50), nullable=True)
    ano_compra = Column(Integer, nullable=True)
    valor_estimado = Column(DECIMAL(15,2), nullable=True)
    valor_homologado = Column(DECIMAL(15,2), nullable=True)
    descricao_detalhada = Column(String(5000), nullable=True)
    
    

    def __repr__(self):
        return f"<viewPncp(id='{self.id_compra}', ano={self.ano_compra})>"

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserResponse(BaseModel): 
    id: int
    username: str
    email: str
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    username: str

class TokenData(BaseModel):
    email: Optional[str] = None

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

class MinhaViewResponse(BaseModel):
    id_compra: str
    processo: str | None = None
    modalidade_nome: str | None = None
    numero_compra: str | None = None
    objeto_compra: str | None = None
    descricao_resumida: str | None = None
    unidade_medida: str | None = None
    quantidade_resultado: Decimal | None = None
    quantidade_ufca: Decimal | None = None
    valor_total_resultado: Decimal | None = None
    valor_unitario_estimado: Decimal | None = None
    valor_unitario_resultado: Decimal | None = None
    valor_planejamento: Decimal | None = None
    valor_total_homologado: Decimal | None = None
    nome_fornecedor: str | None = None
    numero_item_compra: int | None = None
    cnpj_fornecedor: str | None = None
    codigo_fornecedor: str | None = None
    ni_fornecedor: str | None = None
    objeto_resumido: str | None = None
    objeto_TR: str | None = None
    demandante: str | None = None
    situacao_compra_item_nome: str | None = None
    nome_material_ou_servico: str | None = None
    ano_compra: int | None = None
    valor_estimado: Decimal | None = None

    valor_homologado: Decimal | None = None
    descricao_detalhada: str | None = None

    class Config:
        from_attributes = True

