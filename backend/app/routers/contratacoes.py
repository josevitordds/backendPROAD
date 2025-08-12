# app/routers/contratacoes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

# Importações relativas para o seu projeto
from ..database import get_db # Importa a dependência do DB (SQLAlchemy Session)
from ..models import schemas # Seus esquemas Pydantic e modelos ORM
from ..crud import contratacoes as crud_contratacoes # Importa as funções CRUD refatoradas
from .. import security # Para proteger as rotas com autenticação

router = APIRouter(prefix="/contratacoes", tags=["Contratações"])

# Rota para listar contratações
@router.get("/", response_model=List[schemas.Contratacao])
# Exemplo de proteção de rota: apenas usuários autenticados podem acessar
# @router.get("/", response_model=List[schemas.Contratacao], dependencies=[Depends(security.get_current_active_user)])
def read_contratacoes_api(
    ano: Optional[int] = None,
    db: Session = Depends(get_db) # Injeta a sessão do banco de dados
):
    """
    Retorna uma lista de contratações, opcionalmente filtradas por ano.
    """
    # Usa a função CRUD refatorada que interage com o SQLAlchemy
    contratacoes = crud_contratacoes.get_contratacoes(db, ano=ano)
    return contratacoes

# Rota para criar uma nova contratação
@router.post("/", response_model=schemas.Contratacao, status_code=status.HTTP_201_CREATED)
# Exemplo de proteção de rota
# @router.post("/", response_model=schemas.Contratacao, status_code=status.HTTP_201_CREATED, dependencies=[Depends(security.get_current_active_user)])
def create_contratacao_api(
    contratacao: schemas.Contratacao, # Recebe o esquema Pydantic de entrada
    db: Session = Depends(get_db)
):
    """
    Cria uma nova contratação no banco de dados.
    """
    db_contratacao = crud_contratacoes.get_contratacao_by_id(db, id_compra=contratacao.id_compra)
    if db_contratacao:
        raise HTTPException(status_code=400, detail="Contratação com este ID já existe.")
    
    return crud_contratacoes.create_contratacao(db=db, contratacao=contratacao)

# Rota para deletar uma contratação
@router.delete("/{id_compra}", status_code=status.HTTP_204_NO_CONTENT)
# Exemplo de proteção de rota
# @router.delete("/{id_compra}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(security.get_current_active_user)])
def delete_contratacao_api(id_compra: str, db: Session = Depends(get_db)):
    """
    Deleta uma contratação existente pelo ID.
    """
    success = crud_contratacoes.delete_contratacao(db, id_compra=id_compra)
    if not success:
        raise HTTPException(status_code=404, detail="Contratação não encontrada.")
    
    return # Retorna 204 No Content, que não precisa de corpo.
