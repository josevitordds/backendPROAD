# app/routers/semlicitacao.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session # Importe Session para tipagem
from typing import List, Optional

# Importações relativas para o seu projeto
from ..database import get_db # Importa a dependência do DB (SQLAlchemy Session)
from ..models import schemas # Seus esquemas Pydantic e modelos ORM
from ..crud import semlicitacao as crud_sem_licitacao # Importa as funções CRUD refatoradas
from .. import security # Para proteger as rotas com autenticação (opcional)

router = APIRouter(prefix="/semlicitacao", tags=["Compras Sem Licitação"])

# Rota para listar compras sem licitação
@router.get("/", response_model=List[schemas.SemLicitacao])
# Exemplo de proteção de rota: apenas usuários autenticados podem acessar
# @router.get("/", response_model=List[schemas.SemLicitacao], dependencies=[Depends(security.get_current_active_user)])
def read_sem_licitacao_api(
    ano: Optional[int] = None, # Parâmetro opcional para filtrar por ano
    db: Session = Depends(get_db) # Injeta a sessão do banco de dados
):
    """
    Retorna uma lista de compras sem licitação, opcionalmente filtradas por ano.
    """
    # Usa a função CRUD refatorada que interage com o SQLAlchemy
    resultados = crud_sem_licitacao.get_sem_licitacao(db, ano=ano)
    return resultados

# Rota para criar uma nova compra sem licitação
@router.post("/", response_model=schemas.SemLicitacao, status_code=status.HTTP_201_CREATED)
# Exemplo de proteção de rota
# @router.post("/", response_model=schemas.SemLicitacao, status_code=status.HTTP_201_CREATED, dependencies=[Depends(security.get_current_active_user)])
def create_sem_licitacao_api(
    sem_licitacao: schemas.SemLicitacao, # Recebe o esquema Pydantic de entrada
    db: Session = Depends(get_db)
):
    """
    Cria uma nova compra sem licitação no banco de dados.
    """
    # Verifica se já existe uma compra sem licitação com o mesmo ID (assumindo id_compra como identificador único)
    db_item = crud_sem_licitacao.get_sem_licitacao_by_id_compra(db, id_compra=sem_licitacao.id_compra)
    if db_item:
        raise HTTPException(status_code=400, detail="Compra sem licitação com este ID já existe.")
    
    return crud_sem_licitacao.create_sem_licitacao(db=db, sem_licitacao=sem_licitacao)

# Rota para deletar uma compra sem licitação
@router.delete("/{id_compra}", status_code=status.HTTP_204_NO_CONTENT)
# Exemplo de proteção de rota
# @router.delete("/{id_compra}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(security.get_current_active_user)])
def delete_sem_licitacao_api(id_compra: str, db: Session = Depends(get_db)):
    """
    Deleta uma compra sem licitação existente pelo ID de compra.
    """
    success = crud_sem_licitacao.delete_sem_licitacao(db, id_compra=id_compra)
    if not success:
        raise HTTPException(status_code=404, detail="Compra sem licitação não encontrada.")
    
    # Para status 204 (No Content), não se deve retornar um corpo de resposta.
    return
