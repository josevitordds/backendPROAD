# app/crud/resultadoitenscontratacoes.py
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import schemas # Importa seus esquemas Pydantic e o modelo ORM

def get_resultado_itens_contratacoes(db: Session, ano: Optional[int] = None) -> List[schemas.ResultadoItensContratacoesORM]:
    query = db.query(schemas.ResultadoItensContratacoesORM)
    return query.all()

def get_resultado_itens_contratacao_by_id(db: Session, id_compra_item: str) -> Optional[schemas.ResultadoItensContratacoesORM]:
    return db.query(schemas.ResultadoItensContratacoesORM).filter(schemas.ResultadoItensContratacoesORM.id_compra_item == id_compra_item).first()

def create_resultado_itens_contratacao(db: Session, resultado_item: schemas.ResultadoItensContratacao) -> schemas.ResultadoItensContratacoesORM:
    db_resultado_item = schemas.ResultadoItensContratacoesORM(
        id_compra_item=resultado_item.id_compra_item,
        id_compra=resultado_item.id_compra,
        data_inclusao=resultado_item.data_inclusao,
    )
    db.add(db_resultado_item)
    db.commit()
    db.refresh(db_resultado_item)
    return db_resultado_item

def delete_resultado_itens_contratacao(db: Session, id_compra_item: str) -> bool:
    db_resultado_item = db.query(schemas.ResultadoItensContratacoesORM).filter(schemas.ResultadoItensContratacoesORM.id_compra_item == id_compra_item).first()
    if db_resultado_item:
        db.delete(db_resultado_item)
        db.commit()
        return True
    return False


