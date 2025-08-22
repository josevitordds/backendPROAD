from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from ..models import schemas
from ..crud import viewPncp as crud_minhaview
from .. import security 

# Assumindo que você tenha um schema de usuário para a dependência de segurança
# from ..models.schemas import User 

router = APIRouter(prefix="/viewPncp", tags=["Visão PNCP"]) 

@router.get("/", response_model=List[schemas.MinhaViewResponse])
def read_minha_view_api(
    ano: Optional[int] = None,
    numero_processo: Optional[str] = None, 
    descricao_tr: Optional[str] = None,    
    db: Session = Depends(get_db),
    # Descomente a linha abaixo se a leitura também precisar de autenticação
    # current_user: schemas.User = Depends(security.get_current_active_user)
):
    """
    Lê os dados da view com filtros opcionais.
    """
    dados_da_view = crud_minhaview.get_dados_da_view(
        db,
        ano=ano,
        numero_processo=numero_processo, 
        descricao_tr=descricao_tr      
    )
    return dados_da_view

@router.get("/{id_compra}", response_model=schemas.MinhaViewResponse)
def get_minha_view_by_id_api(
    id_compra: str,
    db: Session = Depends(get_db)
    # current_user: schemas.User = Depends(security.get_current_active_user)
):
    """
    Busca um registro específico pelo seu id_compra.
    """
    dado = crud_minhaview.get_dado_da_view_by_id(db, id_unico=id_compra)
    if not dado:
        raise HTTPException(status_code=404, detail="Registro não encontrado na VIEW.")
    return dado

@router.put("/{id_compra}", response_model=schemas.MinhaViewResponse)
def update_view_data(
    id_compra: str, 
    dado_update: schemas.MinhaViewUpdate, 
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(security.get_current_active_user) 
):
    db_dado = crud_minhaview.update_dado_da_view(db=db, id_compra=id_compra, dado_update=dado_update)
    if db_dado is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro não encontrado para atualização")
    return db_dado

@router.delete("/{id_compra}", response_model=schemas.MinhaViewResponse)
def delete_view_data(
    id_compra: str,
    numero_item_compra: int = Query(..., description="O número do item específico a ser deletado"),
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(security.get_current_active_user)
):
    db_dado = crud_minhaview.delete_dado_da_view(
        db=db, 
        id_compra=id_compra, 
        numero_item_compra=numero_item_compra
    )
    
    if db_dado is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item não encontrado para deleção")
        

    return db_dado
