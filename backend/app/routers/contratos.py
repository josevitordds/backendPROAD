from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session 
from typing import List, Optional

from ..database import get_db 
from ..models import schemas 
from ..crud import contratos as crud_contratos
from .. import security 

router = APIRouter(prefix="/contratos", tags=["Contratos"])

@router.get("/", response_model=List[schemas.Contratos])
def read_contratos_api(
    ano: Optional[int] = None, 
    db: Session = Depends(get_db) 
):
    contratos = crud_contratos.get_contratos(db, ano=ano)
    return contratos

@router.post("/", response_model=schemas.Contratos, status_code=status.HTTP_201_CREATED)
def create_contrato_api(
    contrato: schemas.Contratos,
    db: Session = Depends(get_db)
):
    db_contrato = crud_contratos.get_contrato_by_numero(db, numero_contrato=contrato.numero_contrato)
    if db_contrato:
        raise HTTPException(status_code=400, detail="Contrato com este número já existe.")
    
    return crud_contratos.create_contrato(db=db, contrato=contrato)

@router.delete("/{numero_contrato}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contrato_api(numero_contrato: str, db: Session = Depends(get_db)):
    success = crud_contratos.delete_contrato(db, numero_contrato=numero_contrato)
    if not success:
        raise HTTPException(status_code=404, detail="Contrato não encontrado.")
    
    return
