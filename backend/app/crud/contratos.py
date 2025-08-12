# app/crud/contratos.py
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import schemas # Importa seus esquemas Pydantic e o modelo ORM

def get_contratos(db: Session, ano: Optional[int] = None) -> List[schemas.ContratosORM]:
    """
    Recupera uma lista de contratos do banco de dados,
    opcionalmente filtrada por ano.
    """
    query = db.query(schemas.ContratosORM)
    if ano is not None:
        query = query.filter(schemas.ContratosORM.ano_compra == ano)
    return query.all()

def get_contrato_by_numero(db: Session, numero_contrato: str) -> Optional[schemas.ContratosORM]:
    """
    Recupera um único contrato pelo seu numero_contrato.
    """
    return db.query(schemas.ContratosORM).filter(schemas.ContratosORM.numero_contrato == numero_contrato).first()

def create_contrato(db: Session, contrato: schemas.Contratos) -> schemas.ContratosORM:
    """
    Cria um novo contrato no banco de dados.
    Recebe um Pydantic BaseModel (schemas.Contratos) e o converte para o modelo ORM.
    """
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
    """
    Deleta um contrato do banco de dados pelo numero_contrato.
    Retorna True se o contrato foi encontrado e deletado, False caso contrário.
    """
    db_contrato = db.query(schemas.ContratosORM).filter(schemas.ContratosORM.numero_contrato == numero_contrato).first()
    if db_contrato:
        db.delete(db_contrato)
        db.commit()
        return True
    return False

