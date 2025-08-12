# app/crud/itenscontratos.py
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import schemas # Importa seus esquemas Pydantic e o modelo ORM

def get_itens_contratos(db: Session, ano: Optional[int] = None) -> List[schemas.ItensContratoORM]:
    query = db.query(schemas.ItensContratoORM)
    if ano is not None:
        query = query.filter(schemas.ItensContratoORM.ano_compra == ano)
    return query.all()

def get_itens_contrato_by_id_compra(db: Session, id_compra: str) -> Optional[schemas.ItensContratoORM]:
    return db.query(schemas.ItensContratoORM).filter(schemas.ItensContratoORM.id_compra == id_compra).first()

def create_itens_contrato(db: Session, itens_contrato: schemas.ItensContratos) -> schemas.ItensContratoORM:
    db_itens_contrato = schemas.ItensContratoORM(
        id_compra=itens_contrato.id_compra,
        ano_compra=itens_contrato.ano_compra
    )
    db.add(db_itens_contrato)
    db.commit()
    db.refresh(db_itens_contrato)
    return db_itens_contrato

def delete_itens_contrato(db: Session, id_compra: str) -> bool:
    db_itens_contrato = db.query(schemas.ItensContratoORM).filter(schemas.ItensContratoORM.id_compra == id_compra).first()
    if db_itens_contrato:
        db.delete(db_itens_contrato)
        db.commit()
        return True
    return False


