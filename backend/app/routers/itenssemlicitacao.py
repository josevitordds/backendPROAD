# app/routers/itenssemlicitacao.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session # Importe Session para tipagem
from typing import List, Optional

# Importações relativas para o seu projeto
from ..database import get_db # Importa a dependência do DB (SQLAlchemy Session)
from ..models import schemas # Seus esquemas Pydantic e modelos ORM
from ..crud import itenssemlicitacao as crud_itens_sem_licitacao # Importa as funções CRUD refatoradas
from .. import security # Para proteger as rotas com autenticação (opcional)

router = APIRouter(prefix="/itenssemlicitacao", tags=["Itens Sem Licitação"])

# Rota para listar itens sem licitação
@router.get("/", response_model=List[schemas.ItensSemLicitacao])
# Exemplo de proteção de rota: apenas usuários autenticados podem acessar
# @router.get("/", response_model=List[schemas.ItensSemLicitacao], dependencies=[Depends(security.get_current_active_user)])
def read_itens_sem_licitacao_api(
    ano: Optional[int] = None, # Parâmetro opcional para filtrar por ano
    db: Session = Depends(get_db) # Injeta a sessão do banco de dados
):
    """
    Retorna uma lista de itens de compra sem licitação, opcionalmente filtrados por ano.
    """
    # Usa a função CRUD refatorada que interage com o SQLAlchemy
    itens_sem_licitacao = crud_itens_sem_licitacao.get_itens_sem_licitacao(db, ano=ano)
    return itens_sem_licitacao

# Rota para criar um novo item sem licitação
@router.post("/", response_model=schemas.ItensSemLicitacao, status_code=status.HTTP_201_CREATED)
# Exemplo de proteção de rota
# @router.post("/", response_model=schemas.ItensSemLicitacao, status_code=status.HTTP_201_CREATED, dependencies=[Depends(security.get_current_active_user)])
def create_itens_sem_licitacao_api(
    itens_sem_licitacao: schemas.ItensSemLicitacao, # Recebe o esquema Pydantic de entrada
    db: Session = Depends(get_db)
):
    """
    Cria um novo item de compra sem licitação no banco de dados.
    """
    # Verifica se já existe um item com o mesmo ID (assumindo id_compra como identificador único)
    db_item = crud_itens_sem_licitacao.get_itens_sem_licitacao_by_id_compra(db, id_compra=itens_sem_licitacao.id_compra)
    if db_item:
        raise HTTPException(status_code=400, detail="Item de compra sem licitação com este ID já existe.")
    
    return crud_itens_sem_licitacao.create_itens_sem_licitacao(db=db, itens_sem_licitacao=itens_sem_licitacao)

# Rota para deletar um item sem licitação
@router.delete("/{id_compra}", status_code=status.HTTP_204_NO_CONTENT)
# Exemplo de proteção de rota
# @router.delete("/{id_compra}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(security.get_current_active_user)])
def delete_itens_sem_licitacao_api(id_compra: str, db: Session = Depends(get_db)):
    """
    Deleta um item de compra sem licitação existente pelo ID de compra.
    """
    success = crud_itens_sem_licitacao.delete_itens_sem_licitacao(db, id_compra=id_compra)
    if not success:
        raise HTTPException(status_code=404, detail="Item de compra sem licitação não encontrado.")
    
    # Para status 204 (No Content), não se deve retornar um corpo de resposta.
    return
