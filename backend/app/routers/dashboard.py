# app/routers/dashboard.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session # Importe Session para tipagem
from typing import Optional

# Importações relativas para o seu projeto
from ..database import get_db # Importa a dependência do DB (SQLAlchemy Session)
from ..models import schemas # Seus esquemas Pydantic e modelos ORM
from ..crud import dashboard as crud_dashboard # Importa as funções CRUD do dashboard
from .. import security # Para proteger as rotas com autenticação (opcional)

router = APIRouter(prefix="/dashboard", tags=["Dashboard"]) # Prefix adjusted to /dashboard

# Rota para obter dados do dashboard
@router.get("/", response_model=schemas.DashboardData)
# Exemplo de proteção de rota: apenas usuários autenticados podem acessar
# @router.get("/", response_model=schemas.DashboardData, dependencies=[Depends(security.get_current_active_user)])
def get_dashboard_data_api(
    db: Session = Depends(get_db) # Injeta a sessão do banco de dados
):
    """
    Retorna os dados sumarizados para o dashboard.
    """
    # Usa a função CRUD refatorada que interage com o SQLAlchemy
    dashboard_data = crud_dashboard.get_dashboard_summary(db)
    return dashboard_data

# Adicione outras rotas específicas do dashboard aqui, se necessário.
