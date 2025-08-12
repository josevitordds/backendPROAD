# app/routers/licitacao.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session # Importe Session para tipagem
from typing import List, Optional

# Importações relativas para o seu projeto
from ..database import get_db # Importa a dependência do DB (SQLAlchemy Session)
from ..models import schemas # Seus esquemas Pydantic e modelos ORM
from ..crud import licitacao as crud_licitacao # Importa as funções CRUD refatoradas
from .. import security # Para proteger as rotas com autenticação (opcional)

router = APIRouter(prefix="/licitacao", tags=["Licitações"])

# Rota para listar licitações
@router.get("/", response_model=List[schemas.Licitacao])
# Exemplo de proteção de rota: apenas usuários autenticados podem acessar
# @router.get("/", response_model=List[schemas.Licitacao], dependencies=[Depends(security.get_current_active_user)])
def read_licitacoes_api(
    ano: Optional[int] = None, # Parâmetro opcional para filtrar por ano
    db: Session = Depends(get_db) # Injeta a sessão do banco de dados
):
    """
    Retorna uma lista de licitações, opcionalmente filtradas por ano.
    """
    # Usa a função CRUD refatorada que interage com o SQLAlchemy
    licitacoes = crud_licitacao.get_licitacoes(db, ano=ano)
    return licitacoes

# Rota para criar uma nova licitação
@router.post("/", response_model=schemas.Licitacao, status_code=status.HTTP_201_CREATED)
# Exemplo de proteção de rota
# @router.post("/", response_model=schemas.Licitacao, status_code=status.HTTP_201_CREATED, dependencies=[Depends(security.get_current_active_user)])
def create_licitacao_api(
    licitacao: schemas.Licitacao, # Recebe o esquema Pydantic de entrada
    db: Session = Depends(get_db)
):
    """
    Cria uma nova licitação no banco de dados.
    """
    # Verifica se já existe uma licitação com o mesmo ID (assumindo id_compra como identificador único)
    db_licitacao = crud_licitacao.get_licitacao_by_id_compra(db, id_compra=licitacao.id_compra)
    if db_licitacao:
        raise HTTPException(status_code=400, detail="Licitação com este ID já existe.")
    
    return crud_licitacao.create_licitacao(db=db, licitacao=licitacao)

# Rota para deletar uma licitação
@router.delete("/{id_compra}", status_code=status.HTTP_204_NO_CONTENT)
# Exemplo de proteção de rota
# @router.delete("/{id_compra}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(security.get_current_active_user)])
def delete_licitacao_api(id_compra: str, db: Session = Depends(get_db)):
    """
    Deleta uma licitação existente pelo ID de compra.
    """
    success = crud_licitacao.delete_licitacao(db, id_compra=id_compra)
    if not success:
        raise HTTPException(status_code=404, detail="Licitação não encontrada.")
    
    # Para status 204 (No Content), não se deve retornar um corpo de resposta.
    return
