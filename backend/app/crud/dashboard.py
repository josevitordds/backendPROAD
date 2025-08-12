from sqlalchemy.orm import Session
from sqlalchemy import func 
from decimal import Decimal
from ..models import schemas 

def get_dashboard_summary(db: Session) -> schemas.DashboardData:
    total_contratacoes = db.query(schemas.ContratacaoORM).count()
    total_homologado_result = db.query(
        func.sum(schemas.ResultadoItensContratacoesORM.valor_total_homologado)
    ).scalar()
    total_homologado = total_homologado_result if total_homologado_result is not None else Decimal(0)

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
