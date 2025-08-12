# app/crud/itenscontratos.py
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import schemas # Importa seus esquemas Pydantic e o modelo ORM

def get_itens_contratos(db: Session, ano: Optional[int] = None) -> List[schemas.ItensContratoORM]:
    """
    Recupera uma lista de itens de contratos do banco de dados,
    opcionalmente filtrada por ano.
    """
    query = db.query(schemas.ItensContratoORM)
    if ano is not None:
        query = query.filter(schemas.ItensContratoORM.ano_compra == ano)
    return query.all()

def get_itens_contrato_by_id_compra(db: Session, id_compra: str) -> Optional[schemas.ItensContratoORM]:
    """
    Recupera um único item de contrato pelo seu id_compra.
    """
    return db.query(schemas.ItensContratoORM).filter(schemas.ItensContratoORM.id_compra == id_compra).first()

def create_itens_contrato(db: Session, itens_contrato: schemas.ItensContratos) -> schemas.ItensContratoORM:
    """
    Cria um novo item de contrato no banco de dados.
    Recebe um Pydantic BaseModel (schemas.ItensContratos) e o converte para o modelo ORM.
    """
    db_itens_contrato = schemas.ItensContratoORM(
        id_compra=itens_contrato.id_compra,
        ano_compra=itens_contrato.ano_compra
        # Mapeie outros campos aqui, se existirem no seu Pydantic BaseModel e ORM
    )
    db.add(db_itens_contrato)
    db.commit()
    db.refresh(db_itens_contrato)
    return db_itens_contrato

def delete_itens_contrato(db: Session, id_compra: str) -> bool:
    """
    Deleta um item de contrato do banco de dados pelo id_compra.
    Retorna True se o item foi encontrado e deletado, False caso contrário.
    """
    db_itens_contrato = db.query(schemas.ItensContratoORM).filter(schemas.ItensContratoORM.id_compra == id_compra).first()
    if db_itens_contrato:
        db.delete(db_itens_contrato)
        db.commit()
        return True
    return False

# Adicione outras funções CRUD (update, etc.) aqui conforme necessário.
