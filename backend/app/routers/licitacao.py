from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session 
from typing import List, Optional

from ..database import get_db 
from ..models import schemas 
from ..crud import licitacao as crud_licitacao 
from .. import security 

router = APIRouter(prefix="/licitacao", tags=["Licitações"])

@router.get("/", response_model=List[schemas.Licitacao])
def read_licitacoes_api(
    ano: Optional[int] = None, 
    db: Session = Depends(get_db) 
):
    licitacoes = crud_licitacao.get_licitacoes(db, ano=ano)
    return licitacoes

@router.post("/", response_model=schemas.Licitacao, status_code=status.HTTP_201_CREATED)
def create_licitacao_api(
    licitacao: schemas.Licitacao, 
    db: Session = Depends(get_db)
):
    db_licitacao = crud_licitacao.get_licitacao_by_id_compra(db, id_compra=licitacao.id_compra)
    if db_licitacao:
        raise HTTPException(status_code=400, detail="Licitação com este ID já existe.")
    
    return crud_licitacao.create_licitacao(db=db, licitacao=licitacao)

@router.delete("/{id_compra}", status_code=status.HTTP_204_NO_CONTENT)
def delete_licitacao_api(id_compra: str, db: Session = Depends(get_db)):
    success = crud_licitacao.delete_licitacao(db, id_compra=id_compra)
    if not success:
        raise HTTPException(status_code=404, detail="Licitação não encontrada.")
    return
