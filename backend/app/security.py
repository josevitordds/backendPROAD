from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session 

from .config import settings 
from .database import get_db 
from .models import schemas 


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Dependência assíncrona para extrair e validar o token JWT.
    Retorna o objeto User do banco de dados se o token for válido.
    """
    from .crud import auth as crud_auth 

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        email: str = payload.get("sub") 
        if email is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(email=email) 
    except JWTError:
        raise credentials_exception
    
    user = crud_auth.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
    """
    Dependência que verifica se o usuário retornado por get_current_user está 'ativo'.
    Você pode adicionar lógica aqui para verificar o status 'is_active' do usuário,
    se o seu modelo User tiver esse campo.
    """
    # Exemplo: Se o seu modelo User tivesse um campo 'is_active'
    # if not current_user.is_active:
    #     raise HTTPException(status_code=400, detail="Usuário inativo")
    return current_user
