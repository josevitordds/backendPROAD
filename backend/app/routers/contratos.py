# app/routers/contratos.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session # Importe Session para tipagem
from typing import List, Optional

# Importações relativas para o seu projeto
from ..database import get_db # Importa a dependência do DB (SQLAlchemy Session)
from ..models import schemas # Seus esquemas Pydantic e modelos ORM
from ..crud import contratos as crud_contratos # Importa as funções CRUD refatoradas
from .. import security # Para proteger as rotas com autenticação

router = APIRouter(prefix="/contratos", tags=["Contratos"])

# Rota para listar contratos
@router.get("/", response_model=List[schemas.Contratos])
# Exemplo de proteção de rota: apenas usuários autenticados podem acessar
# @router.get("/", response_model=List[schemas.Contratos], dependencies=[Depends(security.get_current_active_user)])
def read_contratos_api(
    ano: Optional[int] = None, # Parâmetro opcional para filtrar por ano
    db: Session = Depends(get_db) # Injeta a sessão do banco de dados
):
    """
    Retorna uma lista de contratos, opcionalmente filtrados por ano.
    """
    # Usa a função CRUD refatorada que interage com o SQLAlchemy
    contratos = crud_contratos.get_contratos(db, ano=ano)
    return contratos

# Rota para criar um novo contrato
@router.post("/", response_model=schemas.Contratos, status_code=status.HTTP_201_CREATED)
# Exemplo de proteção de rota
# @router.post("/", response_model=schemas.Contratos, status_code=status.HTTP_201_CREATED, dependencies=[Depends(security.get_current_active_user)])
def create_contrato_api(
    contrato: schemas.Contratos, # Recebe o esquema Pydantic de entrada
    db: Session = Depends(get_db)
):
    """
    Cria um novo contrato no banco de dados.
    """
    # Verifica se já existe um contrato com o mesmo número
    db_contrato = crud_contratos.get_contrato_by_numero(db, numero_contrato=contrato.numero_contrato)
    if db_contrato:
        raise HTTPException(status_code=400, detail="Contrato com este número já existe.")
    
    return crud_contratos.create_contrato(db=db, contrato=contrato)

# Rota para deletar um contrato
@router.delete("/{numero_contrato}", status_code=status.HTTP_204_NO_CONTENT)
# Exemplo de proteção de rota
# @router.delete("/{numero_contrato}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(security.get_current_active_user)])
def delete_contrato_api(numero_contrato: str, db: Session = Depends(get_db)):
    """
    Deleta um contrato existente pelo número.
    """
    success = crud_contratos.delete_contrato(db, numero_contrato=numero_contrato)
    if not success:
        raise HTTPException(status_code=404, detail="Contrato não encontrado.")
    
    # Para status 204 (No Content), não se deve retornar um corpo de resposta.
    return
