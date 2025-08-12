from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db 
from ..models import schemas 
from ..crud import contratacoes as crud_contratacoes 
from .. import security 

router = APIRouter(prefix="/contratacoes", tags=["Contratações"])

@router.get("/", response_model=List[schemas.Contratacao])

def read_contratacoes_api(
    ano: Optional[int] = None,
    db: Session = Depends(get_db) 
):
    contratacoes = crud_contratacoes.get_contratacoes(db, ano=ano)
    return contratacoes

@router.post("/", response_model=schemas.Contratacao, status_code=status.HTTP_201_CREATED)
# Exemplo de proteção de rota
# @router.post("/", response_model=schemas.Contratacao, status_code=status.HTTP_201_CREATED, dependencies=[Depends(security.get_current_active_user)])
def create_contratacao_api(
    contratacao: schemas.Contratacao,
    db: Session = Depends(get_db)
):
    db_contratacao = crud_contratacoes.get_contratacao_by_id(db, id_compra=contratacao.id_compra)
    if db_contratacao:
        raise HTTPException(status_code=400, detail="Contratação com este ID já existe.")
    
    return crud_contratacoes.create_contratacao(db=db, contratacao=contratacao)

@router.delete("/{id_compra}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contratacao_api(id_compra: str, db: Session = Depends(get_db)):
    success = crud_contratacoes.delete_contratacao(db, id_compra=id_compra)
    if not success:
        raise HTTPException(status_code=404, detail="Contratação não encontrada.")
    
    return 
