from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import schemas 

def get_contratos(db: Session, ano: Optional[int] = None) -> List[schemas.ContratosORM]:
    query = db.query(schemas.ContratosORM)
    if ano is not None:
        query = query.filter(schemas.ContratosORM.ano_compra == ano)
    return query.all()

def get_contrato_by_numero(db: Session, numero_contrato: str) -> Optional[schemas.ContratosORM]:
    return db.query(schemas.ContratosORM).filter(schemas.ContratosORM.numero_contrato == numero_contrato).first()

def create_contrato(db: Session, contrato: schemas.Contratos) -> schemas.ContratosORM:
    db_contrato = schemas.ContratosORM(
        numero_contrato=contrato.numero_contrato,
        id_compra=contrato.id_compra,
        ano_compra=contrato.ano_compra
    )
    db.add(db_contrato)
    db.commit() 
    db.refresh(db_contrato) 
    return db_contrato

def delete_contrato(db: Session, numero_contrato: str) -> bool:
    db_contrato = db.query(schemas.ContratosORM).filter(schemas.ContratosORM.numero_contrato == numero_contrato).first()
    if db_contrato:
        db.delete(db_contrato)
        db.commit()
        return True
    return False

