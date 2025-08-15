from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session 
from typing import List, Optional
from datetime import date 

from ..database import get_db 
from ..models import schemas 
from ..crud import resultadoitenscontratacoes as crud_resultado_itens_contratacoes 
from .. import security 

router = APIRouter(prefix="/resultadoitenscontratacoes", tags=["Resultado Itens Contratações"])
@router.get("/", response_model=List[schemas.ResultadoItensContratacao])
def read_resultado_itens_contratacoes_api(
    ano: Optional[int] = None, 
    db: Session = Depends(get_db) 
):
    resultados = crud_resultado_itens_contratacoes.get_resultado_itens_contratacoes(db, ano=ano)
    return resultados


@router.post("/", response_model=schemas.ResultadoItensContratacao, status_code=status.HTTP_201_CREATED)
def create_resultado_itens_contratacao_api(
    resultado_item: schemas.ResultadoItensContratacao, 
    db: Session = Depends(get_db)
):
    db_item = crud_resultado_itens_contratacoes.get_resultado_itens_contratacao_by_id(db, id_compra_item=resultado_item.id_compra_item)
    if db_item:
        raise HTTPException(status_code=400, detail="Resultado de item de contratação com este ID já existe.")
    
    return crud_resultado_itens_contratacoes.create_resultado_itens_contratacao(db=db, resultado_item=resultado_item)

@router.delete("/{id_compra_item}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resultado_itens_contratacao_api(id_compra_item: str, db: Session = Depends(get_db)):
    success = crud_resultado_itens_contratacoes.delete_resultado_itens_contratacao(db, id_compra_item=id_compra_item)
    if not success:
        raise HTTPException(status_code=404, detail="Resultado de item de contratação não encontrado.")

    return
