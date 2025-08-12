from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import schemas 

def get_itens_licitacao(db: Session, ano: Optional[int] = None) -> List[schemas.ItensLicitacaoORM]:
    query = db.query(schemas.ItensLicitacaoORM)
    if ano is not None:
        query = query.filter(schemas.ItensLicitacaoORM.ano_compra == ano)
    return query.all()

def get_itens_licitacao_by_id_compra(db: Session, id_compra: str) -> Optional[schemas.ItensLicitacaoORM]:
    return db.query(schemas.ItensLicitacaoORM).filter(schemas.ItensLicitacaoORM.id_compra == id_compra).first()

def create_itens_licitacao(db: Session, itens_licitacao: schemas.ItensLicitacao) -> schemas.ItensLicitacaoORM:
    db_itens_licitacao = schemas.ItensLicitacaoORM(
        id_compra=itens_licitacao.id_compra,
        ano_compra=itens_licitacao.ano_compra
    )
    db.add(db_itens_licitacao)
    db.commit()
    db.refresh(db_itens_licitacao)
    return db_itens_licitacao

def delete_itens_licitacao(db: Session, id_compra: str) -> bool:
    db_itens_licitacao = db.query(schemas.ItensLicitacaoORM).filter(schemas.ItensLicitacaoORM.id_compra == id_compra).first()
    if db_itens_licitacao:
        db.delete(db_itens_licitacao)
        db.commit()
        return True
    return False


