from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import schemas 

def get_itens_contratacoes(db: Session, ano: Optional[int] = None) -> List[schemas.ItensContratacoesORM]:
    query = db.query(schemas.ItensContratacoesORM)
    if ano is not None:
        query = query.filter(schemas.ItensContratacoesORM.ano_compra == ano)
    return query.all()

def get_itens_contratacao_by_id(db: Session, id_item: str) -> Optional[schemas.ItensContratacoesORM]:
    return db.query(schemas.ItensContratacoesORM).filter(schemas.ItensContratacoesORM.id_item == id_item).first()

def create_itens_contratacao(db: Session, item_contratacao: schemas.ItemContratacao) -> schemas.ItensContratacoesORM:
    db_item_contratacao = schemas.ItensContratacoesORM(
        id_item=item_contratacao.id_compra_item, 
        id_compra=item_contratacao.id_compra,
        ano_compra=item_contratacao.ano_compra,
        descricao_item=item_contratacao.descricao_item,
        quantidade_item=item_contratacao.quantidade_item,
        valor_unitario_estimado=item_contratacao.valor_unitario_estimado
    )
    db.add(db_item_contratacao)
    db.commit()
    db.refresh(db_item_contratacao)
    return db_item_contratacao

def delete_itens_contratacao(db: Session, id_item: str) -> bool:
    db_item_contratacao = db.query(schemas.ItensContratacoesORM).filter(schemas.ItensContratacoesORM.id_item == id_item).first()
    if db_item_contratacao:
        db.delete(db_item_contratacao)
        db.commit()
        return True
    return False


