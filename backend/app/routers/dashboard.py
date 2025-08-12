from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session 
from typing import Optional

from ..database import get_db 
from ..models import schemas 
from ..crud import dashboard as crud_dashboard 
from .. import security 

router = APIRouter(prefix="/dashboard", tags=["Dashboard"]) 

@router.get("/", response_model=schemas.DashboardData)
def get_dashboard_data_api(
    db: Session = Depends(get_db) 
):
    dashboard_data = crud_dashboard.get_dashboard_summary(db)
    return dashboard_data


