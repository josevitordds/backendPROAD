# app/crud/resultadoitenscontratacoes.py
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import schemas # Importa seus esquemas Pydantic e o modelo ORM

def get_resultado_itens_contratacoes(db: Session, ano: Optional[int] = None) -> List[schemas.ResultadoItensContratacoesORM]:
    """
    Recupera uma lista de resultados de itens de contratações do banco de dados.
    A query original filtrava por 'ano_compra', mas esta coluna não estava na SELECT.
    Se 'ano_compra' for uma coluna existente na tabela e você quiser filtrar por ela,
    certifique-se de adicioná-la ao Modelo ORM (ResultadoItensContratacoesORM).
    """
    query = db.query(schemas.ResultadoItensContratacoesORM)
    # Se 'ano_compra' existir no modelo ORM e na tabela, descomente a linha abaixo:
    # if ano is not None:
    #    query = query.filter(schemas.ResultadoItensContratacoesORM.ano_compra == ano)
    return query.all()

def get_resultado_itens_contratacao_by_id(db: Session, id_compra_item: str) -> Optional[schemas.ResultadoItensContratacoesORM]:
    """
    Recupera um único resultado de item de contratação pelo seu id_compra_item.
    """
    return db.query(schemas.ResultadoItensContratacoesORM).filter(schemas.ResultadoItensContratacoesORM.id_compra_item == id_compra_item).first()

def create_resultado_itens_contratacao(db: Session, resultado_item: schemas.ResultadoItensContratacao) -> schemas.ResultadoItensContratacoesORM:
    """
    Cria um novo resultado de item de contratação no banco de dados.
    Recebe um Pydantic BaseModel (schemas.ResultadoItensContratacao) e o converte para o modelo ORM.
    """
    db_resultado_item = schemas.ResultadoItensContratacoesORM(
        id_compra_item=resultado_item.id_compra_item,
        id_compra=resultado_item.id_compra,
        data_inclusao=resultado_item.data_inclusao,
        # Mapeie outros campos aqui, se existirem no seu Pydantic BaseModel e ORM
        # ex: quantidade_homologada=resultado_item.quantidade_homologada
        # ex: valor_unitario_homologado=resultado_item.valor_unitario_homologado
        # ex: valor_total_homologado=resultado_item.valor_total_homologado
    )
    db.add(db_resultado_item)
    db.commit()
    db.refresh(db_resultado_item)
    return db_resultado_item

def delete_resultado_itens_contratacao(db: Session, id_compra_item: str) -> bool:
    """
    Deleta um resultado de item de contratação do banco de dados pelo id_compra_item.
    Retorna True se o item foi encontrado e deletado, False caso contrário.
    """
    db_resultado_item = db.query(schemas.ResultadoItensContratacoesORM).filter(schemas.ResultadoItensContratacoesORM.id_compra_item == id_compra_item).first()
    if db_resultado_item:
        db.delete(db_resultado_item)
        db.commit()
        return True
    return False

# Adicione outras funções CRUD (update, etc.) aqui conforme necessário.
