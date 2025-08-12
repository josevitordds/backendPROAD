# app/crud/itenssemlicitacao.py
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import schemas # Importa seus esquemas Pydantic e o modelo ORM

def get_itens_sem_licitacao(db: Session, ano: Optional[int] = None) -> List[schemas.ItensSemLicitacaoORM]:
    """
    Recupera uma lista de itens de compras sem licitação do banco de dados,
    opcionalmente filtrada por ano.
    """
    query = db.query(schemas.ItensSemLicitacaoORM)
    if ano is not None:
        query = query.filter(schemas.ItensSemLicitacaoORM.ano_compra == ano)
    return query.all()

def get_itens_sem_licitacao_by_id_compra(db: Session, id_compra: str) -> Optional[schemas.ItensSemLicitacaoORM]:
    """
    Recupera um único item de compra sem licitação pelo seu id_compra.
    """
    return db.query(schemas.ItensSemLicitacaoORM).filter(schemas.ItensSemLicitacaoORM.id_compra == id_compra).first()

def create_itens_sem_licitacao(db: Session, itens_sem_licitacao: schemas.ItensSemLicitacao) -> schemas.ItensSemLicitacaoORM:
    """
    Cria um novo item de compra sem licitação no banco de dados.
    Recebe um Pydantic BaseModel (schemas.ItensSemLicitacao) e o converte para o modelo ORM.
    """
    db_itens_sem_licitacao = schemas.ItensSemLicitacaoORM(
        id_compra=itens_sem_licitacao.id_compra,
        ano_compra=itens_sem_licitacao.ano_compra
        # Mapeie outros campos aqui, se existirem no seu Pydantic BaseModel e ORM
    )
    db.add(db_itens_sem_licitacao)
    db.commit()
    db.refresh(db_itens_sem_licitacao)
    return db_itens_sem_licitacao

def delete_itens_sem_licitacao(db: Session, id_compra: str) -> bool:
    """
    Deleta um item de compra sem licitação do banco de dados pelo id_compra.
    Retorna True se o item foi encontrado e deletado, False caso contrário.
    """
    db_itens_sem_licitacao = db.query(schemas.ItensSemLicitacaoORM).filter(schemas.ItensSemLicitacaoORM.id_compra == id_compra).first()
    if db_itens_sem_licitacao:
        db.delete(db_itens_sem_licitacao)
        db.commit()
        return True
    return False

# Adicione outras funções CRUD (update, etc.) aqui conforme necessário.
