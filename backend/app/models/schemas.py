from pydantic import BaseModel
from typing import Optional, List
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
    
    id_compra_item = Column(String(50), primary_key=True, index=True)
    id_compra = Column(String(50), nullable=False)
    id_contratacao_pncp = Column(String(50))
    codigo_unidade_orgao = Column(Integer)
    cnpj_orgao = Column(String(20))
    numero_item_pncp = Column(Integer)
    numero_item_compra = Column(Integer)
    numero_grupo = Column(Integer)
    descricao_resumida = Column(String) 
    material_ou_servico = Column(String(1))
    nome_material_ou_servico = Column(String(100))
    codigo_classe = Column(Integer)
    codigo_grupo = Column(Integer)
    codigo_item_catalogo = Column(Integer)
    descricao_detalhada = Column(String) 
    unidade_medida = Column(String(50))
    orcamento_sigiloso = Column(Boolean)
    item_categoria_id = Column(Integer)
    item_categoria_nome = Column(String(100))
    criterio_julgamento_id = Column(Integer)
    criterio_julgamento_nome = Column(String(100))
    situacao_compra_item = Column(String(50))
    situacao_compra_item_nome = Column(String(100))
    tipo_beneficio = Column(String(50))
    tipo_beneficio_nome = Column(String(100))
    incentivo_produtivo_basico = Column(Boolean)
    quantidade = Column(DECIMAL(15, 2))
    valor_unitario_estimado = Column(DECIMAL(15, 2))
    valor_total_estimado = Column(DECIMAL(15, 2)) 
    tem_resultado = Column(Boolean)
    codigo_fornecedor = Column(String(50))
    nome_fornecedor = Column(String(255))
    quantidade_resultado = Column(DECIMAL(15, 2))
    valor_unitario_resultado = Column(DECIMAL(15, 2))
    valor_total_resultado = Column(DECIMAL(15, 2))
    data_inclusao = Column(Date)
    data_atualizacao = Column(Date)
    data_resultado = Column(Date)
    margem_preferencia_normal = Column(Boolean)
    percentual_margem_preferencia_normal = Column(DECIMAL(5, 2))
    margem_preferencia_adicional = Column(Boolean)
    percentual_margem_preferencia_adicional = Column(DECIMAL(5, 2))
    codigo_ncm = Column(String(20))
    descricao_ncm = Column(String)
    numero_controle_pncp_compra = Column(String(50))
    quantidade_ufca = Column(DECIMAL(15, 2))

    def __repr__(self):
        return f"<ItemContratacao(id_compra_item='{self.id_compra_item}', id_compra='{self.id_compra}')>"

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

    id_compra = Column(String(50), primary_key=True)
    numero_item_compra = Column(Integer, primary_key=True)
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
    cnpj_fornecedor = Column(String(50), nullable=True)
    codigo_fornecedor = Column(String(50), nullable=True)
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
        return f"<viewPncp(id='{self.id_compra}', item={self.numero_item_compra})>"

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
    processo: Optional[str] = None
    modalidade_nome: Optional[str] = None
    numero_compra: Optional[str] = None
    objeto_compra: Optional[str] = None
    descricao_resumida: Optional[str] = None
    unidade_medida: Optional[str] = None
    quantidade_resultado: Optional[Decimal] = None
    quantidade_ufca: Optional[Decimal] = None
    valor_total_resultado: Optional[Decimal] = None
    valor_unitario_estimado: Optional[Decimal] = None
    valor_unitario_resultado: Optional[Decimal] = None
    valor_planejamento: Optional[Decimal] = None
    valor_total_homologado: Optional[Decimal] = None
    nome_fornecedor: Optional[str] = None
    numero_item_compra: Optional[int] = None
    cnpj_fornecedor: Optional[str] = None
    codigo_fornecedor: Optional[str] = None
    ni_fornecedor: Optional[str] = None
    objeto_resumido: Optional[str] = None
    objeto_TR: Optional[str] = None
    demandante: Optional[str] = None
    situacao_compra_item_nome: Optional[str] = None
    nome_material_ou_servico: Optional[str] = None
    ano_compra: Optional[int] = None
    valor_estimado: Optional[Decimal] = None
    valor_homologado: Optional[Decimal] = None
    descricao_detalhada: Optional[str] = None

    class Config:
        from_attributes = True

class MinhaViewUpdate(BaseModel):
    processo: Optional[str] = None
    modalidade_nome: Optional[str] = None
    numero_compra: Optional[str] = None
    objeto_compra: Optional[str] = None
    descricao_resumida: Optional[str] = None
    unidade_medida: Optional[str] = None
    quantidade_resultado: Optional[Decimal] = None
    quantidade_ufca: Optional[Decimal] = None
    valor_total_resultado: Optional[Decimal] = None
    valor_unitario_estimado: Optional[Decimal] = None
    valor_unitario_resultado: Optional[Decimal] = None
    valor_planejamento: Optional[Decimal] = None
    valor_total_homologado: Optional[Decimal] = None
    nome_fornecedor: Optional[str] = None
    numero_item_compra: Optional[int] = None
    cnpj_fornecedor: Optional[str] = None
    codigo_fornecedor: Optional[str] = None
    ni_fornecedor: Optional[str] = None
    objeto_resumido: Optional[str] = None
    objeto_TR: Optional[str] = None
    demandante: Optional[str] = None
    situacao_compra_item_nome: Optional[str] = None
    nome_material_ou_servico: Optional[str] = None
    ano_compra: Optional[int] = None
    valor_estimado: Optional[Decimal] = None
    valor_homologado: Optional[Decimal] = None
    descricao_detalhada: Optional[str] = None

    class Config:
        from_attributes = True
