from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session 
from typing import List, Optional

from ..database import get_db 
from ..models import schemas 
from ..crud import itenscontratos as crud_itens_contratos 
from .. import security 

router = APIRouter(prefix="/itenscontratos", tags=["Itens de Contratos"])

@router.get("/", response_model=List[schemas.ItensContratos])
def read_itens_contratos_api(
    ano: Optional[int] = None, 
    db: Session = Depends(get_db) 
):
    itens_contratos = crud_itens_contratos.get_itens_contratos(db, ano=ano)
    return itens_contratos

@router.post("/", response_model=schemas.ItensContratos, status_code=status.HTTP_201_CREATED)
def create_itens_contrato_api(
    itens_contrato: schemas.ItensContratos, 
    db: Session = Depends(get_db)
):
    db_item = crud_itens_contratos.get_itens_contrato_by_id_compra(db, id_compra=itens_contrato.id_compra)
    if db_item:
        raise HTTPException(status_code=400, detail="Item de contrato com este ID de compra já existe.")
    
    return crud_itens_contratos.create_itens_contrato(db=db, itens_contrato=itens_contrato)

@router.delete("/{id_compra}", status_code=status.HTTP_204_NO_CONTENT)
def delete_itens_contrato_api(id_compra: str, db: Session = Depends(get_db)):
    success = crud_itens_contratos.delete_itens_contrato(db, id_compra=id_compra)
    if not success:
        raise HTTPException(status_code=404, detail="Item de contrato não encontrado.")
    
    return
