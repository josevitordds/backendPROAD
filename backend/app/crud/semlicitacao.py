# app/crud/semlicitacao.py
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import schemas # Importa seus esquemas Pydantic e o modelo ORM

def get_sem_licitacao(db: Session, ano: Optional[int] = None) -> List[schemas.SemLicitacaoORM]:
    """
    Recupera uma lista de compras sem licitação do banco de dados,
    opcionalmente filtrada por ano.
    """
    query = db.query(schemas.SemLicitacaoORM)
    if ano is not None:
        query = query.filter(schemas.SemLicitacaoORM.ano_compra == ano)
    return query.all()

def get_sem_licitacao_by_id_compra(db: Session, id_compra: str) -> Optional[schemas.SemLicitacaoORM]:
    """
    Recupera uma única compra sem licitação pelo seu id_compra.
    """
    return db.query(schemas.SemLicitacaoORM).filter(schemas.SemLicitacaoORM.id_compra == id_compra).first()

def create_sem_licitacao(db: Session, sem_licitacao: schemas.SemLicitacao) -> schemas.SemLicitacaoORM:
    """
    Cria uma nova compra sem licitação no banco de dados.
    Recebe um Pydantic BaseModel (schemas.SemLicitacao) e o converte para o modelo ORM.
    """
    db_sem_licitacao = schemas.SemLicitacaoORM(
        id_compra=sem_licitacao.id_compra,
        ano_compra=sem_licitacao.ano_compra
        # Mapeie outros campos aqui, se existirem no seu Pydantic BaseModel e ORM
    )
    db.add(db_sem_licitacao)
    db.commit()
    db.refresh(db_sem_licitacao)
    return db_sem_licitacao

def delete_sem_licitacao(db: Session, id_compra: str) -> bool:
    """
    Deleta uma compra sem licitação do banco de dados pelo id_compra.
    Retorna True se o item foi encontrado e deletado, False caso contrário.
    """
    db_sem_licitacao = db.query(schemas.SemLicitacaoORM).filter(schemas.SemLicitacaoORM.id_compra == id_compra).first()
    if db_sem_licitacao:
        db.delete(db_sem_licitacao)
        db.commit()
        return True
    return False

# Adicione outras funções CRUD (update, etc.) aqui conforme necessário.
