from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session 
from typing import List, Optional

from ..database import get_db 
from ..models import schemas 
from ..crud import itenscontratacoes as crud_itens_contratacoes 
from .. import security 

router = APIRouter(prefix="/itenscontratacoes", tags=["Itens de Contratações"])

@router.get("/", response_model=List[schemas.ItemContratacao])
def read_itens_contratacoes_api(
    ano: Optional[int] = None, 
    db: Session = Depends(get_db) 
):
    itens_contratacoes = crud_itens_contratacoes.get_itens_contratacoes(db, ano=ano)
    return itens_contratacoes

@router.post("/", response_model=schemas.ItemContratacao, status_code=status.HTTP_201_CREATED)
def create_itens_contratacao_api(
    item_contratacao: schemas.ItemContratacao, 
    db: Session = Depends(get_db)
):
    db_item = crud_itens_contratacoes.get_itens_contratacao_by_id(db, id_item=item_contratacao.id_compra_item)
    if db_item:
        raise HTTPException(status_code=400, detail="Item de contratação com este ID já existe.")
    
    return crud_itens_contratacoes.create_itens_contratacao(db=db, item_contratacao=item_contratacao)

@router.delete("/{id_item}", status_code=status.HTTP_204_NO_CONTENT)
def delete_itens_contratacao_api(id_item: str, db: Session = Depends(get_db)):
    success = crud_itens_contratacoes.delete_itens_contratacao(db, id_item=id_item)
    if not success:
        raise HTTPException(status_code=404, detail="Item de contratação não encontrado.")
    
    return
