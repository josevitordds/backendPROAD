# routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import crud, models, security
from ..database import get_db
from datetime import timedelta
from ..config import settings

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/register", response_model=models.schemas.UserResponse)
def register_user(user: models.schemas.UserCreate, db: Session = Depends(get_db)):
    db_user_email = crud.auth.get_user_by_email(db, email=user.email)
    if db_user_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email já cadastrado"
        )
    
    db_user_username = crud.auth.get_user_by_username(db, username=user.username)
    if db_user_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Nome de usuário já existe"
        )
    
    new_user = crud.auth.create_user(db=db, user=user)
    return new_user

# Endpoint de Login
@router.post("/token", response_model=models.schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.auth.get_user_by_email(db, email=form_data.username) 
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}