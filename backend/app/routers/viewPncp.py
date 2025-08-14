from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from ..models import schemas
from ..crud import viewPncp as crud_minhaview
from .. import security 

router = APIRouter(prefix="/viewPncp", tags=["Visão PNCP"]) 

@router.get("/", response_model=List[schemas.MinhaViewResponse])
def read_minha_view_api(
    ano: Optional[int] = None,
    numero_processo: Optional[str] = None, 
    descricao_tr: Optional[str] = None,    
    db: Session = Depends(get_db)
):
    dados_da_view = crud_minhaview.get_dados_da_view(
        db,
        ano=ano,
        numero_processo=numero_processo, 
        descricao_tr=descricao_tr        
    )
    return dados_da_view

@router.get("/{id_unico}", response_model=schemas.MinhaViewResponse)
def get_minha_view_by_id_api(
    id_unico: str,
    db: Session = Depends(get_db)
):
    dado = crud_minhaview.get_dado_da_view_by_id(db, id_unico=id_unico)
    if not dado:
        raise HTTPException(status_code=404, detail="Registro não encontrado na VIEW.")
    return dado
