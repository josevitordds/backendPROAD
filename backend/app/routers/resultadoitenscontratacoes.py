# app/routers/resultadoitenscontratacoes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session # Importe Session para tipagem
from typing import List, Optional
from datetime import date # Importe date se for usado no Pydantic BaseModel de ResultadoItensContratacao

# Importações relativas para o seu projeto
from ..database import get_db # Importa a dependência do DB (SQLAlchemy Session)
from ..models import schemas # Seus esquemas Pydantic e modelos ORM
from ..crud import resultadoitenscontratacoes as crud_resultado_itens_contratacoes # Importa as funções CRUD refatoradas
from .. import security # Para proteger as rotas com autenticação (opcional)

router = APIRouter(prefix="/resultadoitenscontratacoes", tags=["Resultado Itens Contratações"])

# Rota para listar resultados de itens de contratações
@router.get("/", response_model=List[schemas.ResultadoItensContratacao])
# Exemplo de proteção de rota: apenas usuários autenticados podem acessar
# @router.get("/", response_model=List[schemas.ResultadoItensContratacao], dependencies=[Depends(security.get_current_active_user)])
def read_resultado_itens_contratacoes_api(
    ano: Optional[int] = None, # Parâmetro opcional para filtrar por ano (se existir no ORM)
    db: Session = Depends(get_db) # Injeta a sessão do banco de dados
):
    """
    Retorna uma lista de resultados de itens de contratações, opcionalmente filtrados por ano.
    """
    # Usa a função CRUD refatorada que interage com o SQLAlchemy
    # A função CRUD que você me forneceu para resultadoitenscontratacoes.py tem um parâmetro 'ano',
    # mas a query dentro dela está comentada. Se 'ano_compra' existir na tabela e no ORM,
    # essa filtragem funcionará.
    resultados = crud_resultado_itens_contratacoes.get_resultado_itens_contratacoes(db, ano=ano)
    return resultados

# Rota para criar um novo resultado de item de contratação
@router.post("/", response_model=schemas.ResultadoItensContratacao, status_code=status.HTTP_201_CREATED)
# Exemplo de proteção de rota
# @router.post("/", response_model=schemas.ResultadoItensContratacao, status_code=status.HTTP_201_CREATED, dependencies=[Depends(security.get_current_active_user)])
def create_resultado_itens_contratacao_api(
    resultado_item: schemas.ResultadoItensContratacao, # Recebe o esquema Pydantic de entrada
    db: Session = Depends(get_db)
):
    """
    Cria um novo resultado de item de contratação no banco de dados.
    """
    # Verifica se já existe um resultado com o mesmo ID (assumindo id_compra_item como identificador único)
    db_item = crud_resultado_itens_contratacoes.get_resultado_itens_contratacao_by_id(db, id_compra_item=resultado_item.id_compra_item)
    if db_item:
        raise HTTPException(status_code=400, detail="Resultado de item de contratação com este ID já existe.")
    
    return crud_resultado_itens_contratacoes.create_resultado_itens_contratacao(db=db, resultado_item=resultado_item)

# Rota para deletar um resultado de item de contratação
@router.delete("/{id_compra_item}", status_code=status.HTTP_204_NO_CONTENT)
# Exemplo de proteção de rota
# @router.delete("/{id_compra_item}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(security.get_current_active_user)])
def delete_resultado_itens_contratacao_api(id_compra_item: str, db: Session = Depends(get_db)):
    """
    Deleta um resultado de item de contratação existente pelo ID de compra do item.
    """
    success = crud_resultado_itens_contratacoes.delete_resultado_itens_contratacao(db, id_compra_item=id_compra_item)
    if not success:
        raise HTTPException(status_code=404, detail="Resultado de item de contratação não encontrado.")
    
    # Para status 204 (No Content), não se deve retornar um corpo de resposta.
    return
