from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import schemas

def get_sem_licitacao(db: Session, ano: Optional[int] = None) -> List[schemas.SemLicitacaoORM]:
    query = db.query(schemas.SemLicitacaoORM)
    if ano is not None:
        query = query.filter(schemas.SemLicitacaoORM.ano_compra == ano)
    return query.all()

def get_sem_licitacao_by_id_compra(db: Session, id_compra: str) -> Optional[schemas.SemLicitacaoORM]:
    return db.query(schemas.SemLicitacaoORM).filter(schemas.SemLicitacaoORM.id_compra == id_compra).first()

def create_sem_licitacao(db: Session, sem_licitacao: schemas.SemLicitacao) -> schemas.SemLicitacaoORM:
    db_sem_licitacao = schemas.SemLicitacaoORM(
        id_compra=sem_licitacao.id_compra,
        ano_compra=sem_licitacao.ano_compra
        
    )
    db.add(db_sem_licitacao)
    db.commit()
    db.refresh(db_sem_licitacao)
    return db_sem_licitacao

def delete_sem_licitacao(db: Session, id_compra: str) -> bool:
    db_sem_licitacao = db.query(schemas.SemLicitacaoORM).filter(schemas.SemLicitacaoORM.id_compra == id_compra).first()
    if db_sem_licitacao:
        db.delete(db_sem_licitacao)
        db.commit()
        return True
    return False


