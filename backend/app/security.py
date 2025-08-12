# app/security.py
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session # Para tipar a sessão do banco de dados

# Importações relativas para os módulos da sua aplicação
from .config import settings # Para acessar a chave secreta e tempo de expiração do token
from .database import get_db # Para obter a sessão do banco de dados
from .models import schemas # Seus esquemas Pydantic, incluindo User e TokenData

# REMOVIDO: 'from .crud import auth as crud_auth' daqui para evitar importação circular.
# A importação será feita DENTRO da função get_current_user.

# ----------------------------------------------------------------------
# Configuração de Hash de Senha (bcrypt)
# ----------------------------------------------------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ----------------------------------------------------------------------
# Configuração de OAuth2 para JWT (Bearer Token)
# ----------------------------------------------------------------------
# tokenUrl="auth/token" aponta para o endpoint de login onde o cliente envia as credenciais
# e espera receber um token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# ----------------------------------------------------------------------
# Funções de Hash e Verificação de Senha
# ----------------------------------------------------------------------
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se uma senha em texto puro corresponde a um hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Cria um hash seguro para uma senha."""
    return pwd_context.hash(password)

# ----------------------------------------------------------------------
# Funções de Criação e Validação de Tokens JWT
# ----------------------------------------------------------------------
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Cria um token de acesso JWT com um payload e um tempo de expiração.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Define um tempo de expiração padrão se não for fornecido nas settings
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# ----------------------------------------------------------------------
# Dependências para Obter o Usuário Atual Autenticado
# ----------------------------------------------------------------------
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Dependência assíncrona para extrair e validar o token JWT.
    Retorna o objeto User do banco de dados se o token for válido.
    """
    # IMPORTANTE: A importação de 'crud_auth' é feita AQUI dentro da função,
    # não no nível superior do módulo. Isso quebra a importação circular.
    from .crud import auth as crud_auth 

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decodifica o token usando a chave secreta e o algoritmo
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        # O 'sub' (subject) do token JWT normalmente guarda o identificador do usuário (email ou ID)
        email: str = payload.get("sub") 
        if email is None:
            raise credentials_exception
        
        # Usa o esquema TokenData para validar o payload (opcional, mas boa prática)
        token_data = schemas.TokenData(email=email) 
    except JWTError:
        # Captura erros de JWT (token inválido, expirado, etc.)
        raise credentials_exception
    
    # Busca o usuário no banco de dados usando o email do token
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
