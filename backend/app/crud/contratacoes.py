from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import schemas 

def get_contratacoes(db: Session, ano: Optional[int] = None) -> List[schemas.ContratacaoORM]:
    query = db.query(schemas.ContratacaoORM)
    if ano is not None:
        query = query.filter(schemas.ContratacaoORM.ano_compra == ano)
    return query.all()

def get_contratacao_by_id(db: Session, id_compra: str) -> Optional[schemas.ContratacaoORM]:
    return db.query(schemas.ContratacaoORM).filter(schemas.ContratacaoORM.id_compra == id_compra).first()

def create_contratacao(db: Session, contratacao: schemas.Contratacao) -> schemas.ContratacaoORM:
    db_contratacao = schemas.ContratacaoORM(
        id_compra=contratacao.id_compra,
        ano_compra=contratacao.ano_compra,
        objeto_compra=contratacao.objeto_compra,
        valor_estimado=contratacao.valor_estimado
    )
    db.add(db_contratacao)
    db.commit() 
    db.refresh(db_contratacao) 
    return db_contratacao

def delete_contratacao(db: Session, id_compra: str) -> bool:
    db_contratacao = db.query(schemas.ContratacaoORM).filter(schemas.ContratacaoORM.id_compra == id_compra).first()
    if db_contratacao:
        db.delete(db_contratacao)
        db.commit()
        return True
    return False

