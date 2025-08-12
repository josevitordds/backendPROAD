# app/crud/itenscontratacoes.py
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import schemas # Importa seus esquemas Pydantic e o modelo ORM

def get_itens_contratacoes(db: Session, ano: Optional[int] = None) -> List[schemas.ItensContratacoesORM]:
    """
    Recupera uma lista de itens de contratações do banco de dados,
    opcionalmente filtrada por ano.
    """
    query = db.query(schemas.ItensContratacoesORM)
    if ano is not None:
        query = query.filter(schemas.ItensContratacoesORM.ano_compra == ano)
    return query.all()

def get_itens_contratacao_by_id(db: Session, id_item: str) -> Optional[schemas.ItensContratacoesORM]:
    """
    Recupera um único item de contratação pelo seu id_item.
    """
    return db.query(schemas.ItensContratacoesORM).filter(schemas.ItensContratacoesORM.id_item == id_item).first()

def create_itens_contratacao(db: Session, item_contratacao: schemas.ItemContratacao) -> schemas.ItensContratacoesORM:
    """
    Cria um novo item de contratação no banco de dados.
    Recebe um Pydantic BaseModel (schemas.ItemContratacao) e o converte para o modelo ORM.
    """
    db_item_contratacao = schemas.ItensContratacoesORM(
        id_item=item_contratacao.id_compra_item, # Supondo que 'id_compra_item' do Pydantic mapeia para 'id_item' no ORM
        id_compra=item_contratacao.id_compra,
        ano_compra=item_contratacao.ano_compra,
        descricao_item=item_contratacao.descricao_item,
        quantidade_item=item_contratacao.quantidade_item,
        valor_unitario_estimado=item_contratacao.valor_unitario_estimado
        # Mapeie outros campos aqui, se existirem no seu Pydantic BaseModel e ORM
    )
    db.add(db_item_contratacao)
    db.commit()
    db.refresh(db_item_contratacao)
    return db_item_contratacao

def delete_itens_contratacao(db: Session, id_item: str) -> bool:
    """
    Deleta um item de contratação do banco de dados pelo id_item.
    Retorna True se o item foi encontrado e deletado, False caso contrário.
    """
    db_item_contratacao = db.query(schemas.ItensContratacoesORM).filter(schemas.ItensContratacoesORM.id_item == id_item).first()
    if db_item_contratacao:
        db.delete(db_item_contratacao)
        db.commit()
        return True
    return False

# Adicione outras funções CRUD (update, etc.) aqui conforme necessário.
