# app/routers/itenslicitacao.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session # Importe Session para tipagem
from typing import List, Optional

# Importações relativas para o seu projeto
from ..database import get_db # Importa a dependência do DB (SQLAlchemy Session)
from ..models import schemas # Seus esquemas Pydantic e modelos ORM
from ..crud import itenslicitacao as crud_itens_licitacao # Importa as funções CRUD refatoradas
from .. import security # Para proteger as rotas com autenticação (opcional)

router = APIRouter(prefix="/itenslicitacao", tags=["Itens de Licitação"])

# Rota para listar itens de licitação
@router.get("/", response_model=List[schemas.ItensLicitacao])
# Exemplo de proteção de rota: apenas usuários autenticados podem acessar
# @router.get("/", response_model=List[schemas.ItensLicitacao], dependencies=[Depends(security.get_current_active_user)])
def read_itens_licitacao_api(
    ano: Optional[int] = None, # Parâmetro opcional para filtrar por ano
    db: Session = Depends(get_db) # Injeta a sessão do banco de dados
):
    """
    Retorna uma lista de itens de licitação, opcionalmente filtrados por ano.
    """
    # Usa a função CRUD refatorada que interage com o SQLAlchemy
    itens_licitacao = crud_itens_licitacao.get_licitacoes(db, ano=ano) # Note: a função é get_licitacoes no seu CRUD
    return itens_licitacao

# Rota para criar um novo item de licitação
@router.post("/", response_model=schemas.ItensLicitacao, status_code=status.HTTP_201_CREATED)
# Exemplo de proteção de rota
# @router.post("/", response_model=schemas.ItensLicitacao, status_code=status.HTTP_201_CREATED, dependencies=[Depends(security.get_current_active_user)])
def create_itens_licitacao_api(
    itens_licitacao: schemas.ItensLicitacao, # Recebe o esquema Pydantic de entrada
    db: Session = Depends(get_db)
):
    """
    Cria um novo item de licitação no banco de dados.
    """
    # Verifica se já existe um item de licitação com o mesmo ID (assumindo id_compra como identificador único)
    db_item = crud_itens_licitacao.get_itens_licitacao_by_id_compra(db, id_compra=itens_licitacao.id_compra)
    if db_item:
        raise HTTPException(status_code=400, detail="Item de licitação com este ID de compra já existe.")
    
    return crud_itens_licitacao.create_itens_licitacao(db=db, itens_licitacao=itens_licitacao)

# Rota para deletar um item de licitação
@router.delete("/{id_compra}", status_code=status.HTTP_204_NO_CONTENT)
# Exemplo de proteção de rota
# @router.delete("/{id_compra}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(security.get_current_active_user)])
def delete_itens_licitacao_api(id_compra: str, db: Session = Depends(get_db)):
    """
    Deleta um item de licitação existente pelo ID de compra.
    """
    success = crud_itens_licitacao.delete_itens_licitacao(db, id_compra=id_compra)
    if not success:
        raise HTTPException(status_code=404, detail="Item de licitação não encontrado.")
    
    # Para status 204 (No Content), não se deve retornar um corpo de resposta.
    return
