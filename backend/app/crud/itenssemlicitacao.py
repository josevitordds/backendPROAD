from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import schemas 

def get_itens_sem_licitacao(db: Session, ano: Optional[int] = None) -> List[schemas.ItensSemLicitacaoORM]:
    query = db.query(schemas.ItensSemLicitacaoORM)
    if ano is not None:
        query = query.filter(schemas.ItensSemLicitacaoORM.ano_compra == ano)
    return query.all()

def get_itens_sem_licitacao_by_id_compra(db: Session, id_compra: str) -> Optional[schemas.ItensSemLicitacaoORM]:
    return db.query(schemas.ItensSemLicitacaoORM).filter(schemas.ItensSemLicitacaoORM.id_compra == id_compra).first()

def create_itens_sem_licitacao(db: Session, itens_sem_licitacao: schemas.ItensSemLicitacao) -> schemas.ItensSemLicitacaoORM:
    db_itens_sem_licitacao = schemas.ItensSemLicitacaoORM(
        id_compra=itens_sem_licitacao.id_compra,
        ano_compra=itens_sem_licitacao.ano_compra
    )
    db.add(db_itens_sem_licitacao)
    db.commit()
    db.refresh(db_itens_sem_licitacao)
    return db_itens_sem_licitacao

def delete_itens_sem_licitacao(db: Session, id_compra: str) -> bool:
    db_itens_sem_licitacao = db.query(schemas.ItensSemLicitacaoORM).filter(schemas.ItensSemLicitacaoORM.id_compra == id_compra).first()
    if db_itens_sem_licitacao:
        db.delete(db_itens_sem_licitacao)
        db.commit()
        return True
    return False


