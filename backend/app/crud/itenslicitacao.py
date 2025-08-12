# app/crud/itenslicitacao.py
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import schemas # Importa seus esquemas Pydantic e o modelo ORM

def get_itens_licitacao(db: Session, ano: Optional[int] = None) -> List[schemas.ItensLicitacaoORM]:
    """
    Recupera uma lista de itens de licitações do banco de dados,
    opcionalmente filtrada por ano.
    """
    query = db.query(schemas.ItensLicitacaoORM)
    if ano is not None:
        query = query.filter(schemas.ItensLicitacaoORM.ano_compra == ano)
    return query.all()

def get_itens_licitacao_by_id_compra(db: Session, id_compra: str) -> Optional[schemas.ItensLicitacaoORM]:
    """
    Recupera um único item de licitação pelo seu id_compra.
    """
    return db.query(schemas.ItensLicitacaoORM).filter(schemas.ItensLicitacaoORM.id_compra == id_compra).first()

def create_itens_licitacao(db: Session, itens_licitacao: schemas.ItensLicitacao) -> schemas.ItensLicitacaoORM:
    """
    Cria um novo item de licitação no banco de dados.
    Recebe um Pydantic BaseModel (schemas.ItensLicitacao) e o converte para o modelo ORM.
    """
    db_itens_licitacao = schemas.ItensLicitacaoORM(
        id_compra=itens_licitacao.id_compra,
        ano_compra=itens_licitacao.ano_compra
        # Mapeie outros campos aqui, se existirem no seu Pydantic BaseModel e ORM
    )
    db.add(db_itens_licitacao)
    db.commit()
    db.refresh(db_itens_licitacao)
    return db_itens_licitacao

def delete_itens_licitacao(db: Session, id_compra: str) -> bool:
    """
    Deleta um item de licitação do banco de dados pelo id_compra.
    Retorna True se o item foi encontrado e deletado, False caso contrário.
    """
    db_itens_licitacao = db.query(schemas.ItensLicitacaoORM).filter(schemas.ItensLicitacaoORM.id_compra == id_compra).first()
    if db_itens_licitacao:
        db.delete(db_itens_licitacao)
        db.commit()
        return True
    return False

# Adicione outras funções CRUD (update, etc.) aqui conforme necessário.
