# app/routers/itenscontratos.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session # Importe Session para tipagem
from typing import List, Optional

# Importações relativas para o seu projeto
from ..database import get_db # Importa a dependência do DB (SQLAlchemy Session)
from ..models import schemas # Seus esquemas Pydantic e modelos ORM
from ..crud import itenscontratos as crud_itens_contratos # Importa as funções CRUD refatoradas
from .. import security # Para proteger as rotas com autenticação (opcional)

router = APIRouter(prefix="/itenscontratos", tags=["Itens de Contratos"])

# Rota para listar itens de contratos
@router.get("/", response_model=List[schemas.ItensContratos])
# Exemplo de proteção de rota: apenas usuários autenticados podem acessar
# @router.get("/", response_model=List[schemas.ItensContratos], dependencies=[Depends(security.get_current_active_user)])
def read_itens_contratos_api(
    ano: Optional[int] = None, # Parâmetro opcional para filtrar por ano
    db: Session = Depends(get_db) # Injeta a sessão do banco de dados
):
    """
    Retorna uma lista de itens de contratos, opcionalmente filtrados por ano.
    """
    # Usa a função CRUD refatorada que interage com o SQLAlchemy
    itens_contratos = crud_itens_contratos.get_itens_contratos(db, ano=ano)
    return itens_contratos

# Rota para criar um novo item de contrato
@router.post("/", response_model=schemas.ItensContratos, status_code=status.HTTP_201_CREATED)
# Exemplo de proteção de rota
# @router.post("/", response_model=schemas.ItensContratos, status_code=status.HTTP_201_CREATED, dependencies=[Depends(security.get_current_active_user)])
def create_itens_contrato_api(
    itens_contrato: schemas.ItensContratos, # Recebe o esquema Pydantic de entrada
    db: Session = Depends(get_db)
):
    """
    Cria um novo item de contrato no banco de dados.
    """
    # Verifica se já existe um item de contrato com o mesmo ID (assumindo id_compra como identificador único)
    db_item = crud_itens_contratos.get_itens_contrato_by_id_compra(db, id_compra=itens_contrato.id_compra)
    if db_item:
        raise HTTPException(status_code=400, detail="Item de contrato com este ID de compra já existe.")
    
    return crud_itens_contratos.create_itens_contrato(db=db, itens_contrato=itens_contrato)

# Rota para deletar um item de contrato
@router.delete("/{id_compra}", status_code=status.HTTP_204_NO_CONTENT)
# Exemplo de proteção de rota
# @router.delete("/{id_compra}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(security.get_current_active_user)])
def delete_itens_contrato_api(id_compra: str, db: Session = Depends(get_db)):
    """
    Deleta um item de contrato existente pelo ID de compra.
    """
    success = crud_itens_contratos.delete_itens_contrato(db, id_compra=id_compra)
    if not success:
        raise HTTPException(status_code=404, detail="Item de contrato não encontrado.")
    
    # Para status 204 (No Content), não se deve retornar um corpo de resposta.
    return
