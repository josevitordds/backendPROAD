# app/crud/auth.py
from sqlalchemy.orm import Session
from ..models import schemas
from ..security import get_password_hash # get_password_hash é importado aqui

def get_user_by_email(db: Session, email: str):
    """
    Busca um usuário no banco de dados pelo email.
    """
    return db.query(schemas.User).filter(schemas.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    """
    Busca um usuário no banco de dados pelo nome de usuário.
    Esta função é usada para verificar a unicidade do username no cadastro.
    """
    return db.query(schemas.User).filter(schemas.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    """
    Cria um novo usuário no banco de dados.
    A senha é hashed antes de ser salva.
    """
    hashed_password = get_password_hash(user.password)
    db_user = schemas.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user) # Atualiza o objeto para incluir o ID gerado pelo banco de dados
    return db_user
