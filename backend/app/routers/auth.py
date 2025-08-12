# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

# Importações relativas para os módulos da sua aplicação
from .. import crud, models, security
from ..database import get_db
from ..config import settings

router = APIRouter(prefix="/auth", tags=["Autenticação"])

# Rota para o cadastro de usuários
@router.post("/register", response_model=models.schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: models.schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint para registrar um novo usuário.
    Verifica se o email ou nome de usuário já existem antes de criar.
    """
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
    """
    Endpoint para login de usuário e obtenção de token JWT.
    Espera 'username' (email) e 'password' no corpo da requisição (form-urlencoded).
    """
    user = crud.auth.get_user_by_email(db, email=form_data.username) # Busca o usuário pelo email
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        # Se o usuário não existe ou a senha está incorreta, lança uma exceção 401
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Se as credenciais estiverem corretas, cria um token de acesso JWT
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    # Retorna o token JWT
    return {"access_token": access_token, "token_type": "bearer"}

# Exemplo de rota protegida que requer um token JWT
@router.get("/protected_data", response_model=models.schemas.UserResponse)
async def read_protected_data(current_user: models.schemas.UserResponse = Depends(security.get_current_active_user)):
    """
    Exemplo de rota protegida que só pode ser acessada com um token JWT válido.
    Retorna os dados do usuário autenticado.
    """
    return current_user
