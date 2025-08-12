# app/crud/dashboard.py
from sqlalchemy.orm import Session
from sqlalchemy import func # Importe func para funções de agregação (COUNT, SUM, AVG)
from decimal import Decimal
from ..models import schemas # Importa seus esquemas Pydantic e modelos ORM

def get_dashboard_summary(db: Session) -> schemas.DashboardData:
    """
    Recupera dados sumarizados para o dashboard usando SQLAlchemy ORM.
    Inclui total de contratações, total homologado e média de economia.
    """
    # 1. Total de contratações
    total_contratacoes = db.query(schemas.ContratacaoORM).count()

    # 2. Total homologado
    # Soma de valor_total_homologado da tabela resultadoItensContratacoesPncpUfca
    total_homologado_result = db.query(
        func.sum(schemas.ResultadoItensContratacoesORM.valor_total_homologado)
    ).scalar()
    total_homologado = total_homologado_result if total_homologado_result is not None else Decimal(0)

    # 3. Média de economia
    # JOIN entre itensContratacoesPncpUfca e resultadoItensContratacoesPncpUfca
    media_economia_result = db.query(
        func.avg(
            schemas.ItensContratacoesORM.valor_total_estimado - schemas.ResultadoItensContratacoesORM.valor_total_homologado
        )
    ).join(
        schemas.ResultadoItensContratacoesORM,
        schemas.ItensContratacoesORM.id_item == schemas.ResultadoItensContratacoesORM.id_compra_item
    ).scalar()
    media_economia = media_economia_result if media_economia_result is not None else Decimal(0)

    return schemas.DashboardData(
        total_contratacoes=total_contratacoes,
        total_homologado=total_homologado,
        media_economia=media_economia
    )
