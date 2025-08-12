# app/crud/licitacao.py
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import schemas # Importa seus esquemas Pydantic e o modelo ORM

def get_licitacoes(db: Session, ano: Optional[int] = None) -> List[schemas.LicitacaoORM]:
    """
    Recupera uma lista de licitações do banco de dados,
    opcionalmente filtrada por ano.
    """
    query = db.query(schemas.LicitacaoORM)
    if ano is not None:
        query = query.filter(schemas.LicitacaoORM.ano_compra == ano)
    return query.all()

def get_licitacao_by_id_compra(db: Session, id_compra: str) -> Optional[schemas.LicitacaoORM]:
    """
    Recupera uma única licitação pelo seu id_compra.
    """
    return db.query(schemas.LicitacaoORM).filter(schemas.LicitacaoORM.id_compra == id_compra).first()

def create_licitacao(db: Session, licitacao: schemas.Licitacao) -> schemas.LicitacaoORM:
    """
    Cria uma nova licitação no banco de dados.
    Recebe um Pydantic BaseModel (schemas.Licitacao) e o converte para o modelo ORM.
    """
    db_licitacao = schemas.LicitacaoORM(
        id_compra=licitacao.id_compra,
        ano_compra=licitacao.ano_compra
        # Mapeie outros campos aqui, se existirem no seu Pydantic BaseModel e ORM
    )
    db.add(db_licitacao)
    db.commit()
    db.refresh(db_licitacao)
    return db_licitacao

def delete_licitacao(db: Session, id_compra: str) -> bool:
    """
    Deleta uma licitação do banco de dados pelo id_compra.
    Retorna True se a licitação foi encontrada e deletada, False caso contrário.
    """
    db_licitacao = db.query(schemas.LicitacaoORM).filter(schemas.LicitacaoORM.id_compra == id_compra).first()
    if db_licitacao:
        db.delete(db_licitacao)
        db.commit()
        return True
    return False

# Adicione outras funções CRUD (update, etc.) aqui conforme necessário.
