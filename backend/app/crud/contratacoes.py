# app/crud/contratacoes.py
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import schemas # Importa seus esquemas Pydantic e o modelo ORM

def get_contratacoes(db: Session, ano: Optional[int] = None) -> List[schemas.ContratacaoORM]:
    """
    Recupera uma lista de contratações do banco de dados,
    opcionalmente filtrada por ano.
    """
    query = db.query(schemas.ContratacaoORM)
    if ano is not None:
        query = query.filter(schemas.ContratacaoORM.ano_compra == ano)
    return query.all()

def get_contratacao_by_id(db: Session, id_compra: str) -> Optional[schemas.ContratacaoORM]:
    """
    Recupera uma única contratação pelo seu id_compra.
    """
    return db.query(schemas.ContratacaoORM).filter(schemas.ContratacaoORM.id_compra == id_compra).first()

def create_contratacao(db: Session, contratacao: schemas.Contratacao) -> schemas.ContratacaoORM:
    """
    Cria uma nova contratação no banco de dados.
    Recebe um Pydantic BaseModel (schemas.Contratacao) e o converte para o modelo ORM.
    """
    db_contratacao = schemas.ContratacaoORM(
        id_compra=contratacao.id_compra,
        ano_compra=contratacao.ano_compra,
        objeto_compra=contratacao.objeto_compra,
        valor_estimado=contratacao.valor_estimado
        # Adicione outros campos aqui, se houver, mapeando-os do Pydantic BaseModel para o ORM
    )
    db.add(db_contratacao)
    db.commit() # Salva as alterações no banco de dados
    db.refresh(db_contratacao) # Atualiza o objeto para obter qualquer valor gerado pelo DB (ex: ID)
    return db_contratacao

def delete_contratacao(db: Session, id_compra: str) -> bool:
    """
    Deleta uma contratação do banco de dados pelo id_compra.
    Retorna True se a contratação foi encontrada e deletada, False caso contrário.
    """
    db_contratacao = db.query(schemas.ContratacaoORM).filter(schemas.ContratacaoORM.id_compra == id_compra).first()
    if db_contratacao:
        db.delete(db_contratacao)
        db.commit()
        return True
    return False

# Adicione outras funções CRUD (update, etc.) aqui conforme necessário.
