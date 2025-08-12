# app/routers/itenscontratacoes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session # Importe Session para tipagem
from typing import List, Optional

# Importações relativas para o seu projeto
from ..database import get_db # Importa a dependência do DB (SQLAlchemy Session)
from ..models import schemas # Seus esquemas Pydantic e modelos ORM
from ..crud import itenscontratacoes as crud_itens_contratacoes # Importa as funções CRUD refatoradas
from .. import security # Para proteger as rotas com autenticação (opcional)

router = APIRouter(prefix="/itenscontratacoes", tags=["Itens de Contratações"])

# Rota para listar itens de contratações
@router.get("/", response_model=List[schemas.ItemContratacao])
# Exemplo de proteção de rota: apenas usuários autenticados podem acessar
# @router.get("/", response_model=List[schemas.ItemContratacao], dependencies=[Depends(security.get_current_active_user)])
def read_itens_contratacoes_api(
    ano: Optional[int] = None, # Parâmetro opcional para filtrar por ano
    db: Session = Depends(get_db) # Injeta a sessão do banco de dados
):
    """
    Retorna uma lista de itens de contratações, opcionalmente filtradas por ano.
    """
    # Usa a função CRUD refatorada que interage com o SQLAlchemy
    itens_contratacoes = crud_itens_contratacoes.get_itens_contratacoes(db, ano=ano)
    return itens_contratacoes

# Rota para criar um novo item de contratação
@router.post("/", response_model=schemas.ItemContratacao, status_code=status.HTTP_201_CREATED)
# Exemplo de proteção de rota
# @router.post("/", response_model=schemas.ItemContratacao, status_code=status.HTTP_201_CREATED, dependencies=[Depends(security.get_current_active_user)])
def create_itens_contratacao_api(
    item_contratacao: schemas.ItemContratacao, # Recebe o esquema Pydantic de entrada
    db: Session = Depends(get_db)
):
    """
    Cria um novo item de contratação no banco de dados.
    """
    # Verifica se já existe um item de contratação com o mesmo ID
    db_item = crud_itens_contratacoes.get_itens_contratacao_by_id(db, id_item=item_contratacao.id_compra_item)
    if db_item:
        raise HTTPException(status_code=400, detail="Item de contratação com este ID já existe.")
    
    return crud_itens_contratacoes.create_itens_contratacao(db=db, item_contratacao=item_contratacao)

# Rota para deletar um item de contratação
@router.delete("/{id_item}", status_code=status.HTTP_204_NO_CONTENT)
# Exemplo de proteção de rota
# @router.delete("/{id_item}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(security.get_current_active_user)])
def delete_itens_contratacao_api(id_item: str, db: Session = Depends(get_db)):
    """
    Deleta um item de contratação existente pelo ID.
    """
    success = crud_itens_contratacoes.delete_itens_contratacao(db, id_item=id_item)
    if not success:
        raise HTTPException(status_code=404, detail="Item de contratação não encontrado.")
    
    # Para status 204 (No Content), não se deve retornar um corpo de resposta.
    return
