from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import date

class Contratacao(BaseModel):
    id_compra: str
    ano_compra: int
    objeto_compra: str
    valor_estimado: Optional[Decimal]

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

class ResultadoItensContratacao(BaseModel):
    id_compra_item: str
    id_compra: str
    quantidade_homologada: Optional[int]
    valor_unitario_homologado: Optional[Decimal]
    valor_total_homologado: Optional[Decimal]

class Contratos(BaseModel):
    numero_contrato: str
    id_compra: str

class ItensContratos(BaseModel):
    id_compra: str

class SemLicitacao(BaseModel):
    id_compra: str

class ItensSemLicitacao(BaseModel):
    id_compra: str

class Licitacao(BaseModel):
    id_compra: str

class ItensLicitacao(BaseModel):
    id_compra: str