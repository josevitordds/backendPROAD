from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import schemas 

def get_licitacoes(db: Session, ano: Optional[int] = None) -> List[schemas.LicitacaoORM]:
    query = db.query(schemas.LicitacaoORM)
    if ano is not None:
        query = query.filter(schemas.LicitacaoORM.ano_compra == ano)
    return query.all()

def get_licitacao_by_id_compra(db: Session, id_compra: str) -> Optional[schemas.LicitacaoORM]:
    return db.query(schemas.LicitacaoORM).filter(schemas.LicitacaoORM.id_compra == id_compra).first()

def create_licitacao(db: Session, licitacao: schemas.Licitacao) -> schemas.LicitacaoORM:
    db_licitacao = schemas.LicitacaoORM(
        id_compra=licitacao.id_compra,
        ano_compra=licitacao.ano_compra
    )
    db.add(db_licitacao)
    db.commit()
    db.refresh(db_licitacao)
    return db_licitacao

def delete_licitacao(db: Session, id_compra: str) -> bool:
    db_licitacao = db.query(schemas.LicitacaoORM).filter(schemas.LicitacaoORM.id_compra == id_compra).first()
    if db_licitacao:
        db.delete(db_licitacao)
        db.commit()
        return True
    return False

