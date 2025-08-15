from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session 
from typing import List, Optional

from ..database import get_db 
from ..models import schemas 
from ..crud import semlicitacao as crud_sem_licitacao 
from .. import security

router = APIRouter(prefix="/semlicitacao", tags=["Compras Sem Licitação"])

@router.get("/", response_model=List[schemas.SemLicitacao])
def read_sem_licitacao_api(
    ano: Optional[int] = None, 
    db: Session = Depends(get_db) 
):
    resultados = crud_sem_licitacao.get_sem_licitacao(db, ano=ano)
    return resultados

@router.post("/", response_model=schemas.SemLicitacao, status_code=status.HTTP_201_CREATED)
def create_sem_licitacao_api(
    sem_licitacao: schemas.SemLicitacao, 
    db: Session = Depends(get_db)
):
    db_item = crud_sem_licitacao.get_sem_licitacao_by_id_compra(db, id_compra=sem_licitacao.id_compra)
    if db_item:
        raise HTTPException(status_code=400, detail="Compra sem licitação com este ID já existe.")
    
    return crud_sem_licitacao.create_sem_licitacao(db=db, sem_licitacao=sem_licitacao)


@router.delete("/{id_compra}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sem_licitacao_api(id_compra: str, db: Session = Depends(get_db)):
    success = crud_sem_licitacao.delete_sem_licitacao(db, id_compra=id_compra)
    if not success:
        raise HTTPException(status_code=404, detail="Compra sem licitação não encontrada.")
    
    return
