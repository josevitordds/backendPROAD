# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Importa as configurações do seu arquivo config.py
from .config import settings

# A URL do banco de dados agora vem das suas configurações
DATABASE_URL = settings.DATABASE_URL

# Cria a engine do banco de dados.
# connect_args={"check_same_thread": False} é útil para SQLite,
# mas não faz mal em MySQL e pode ser mantido.
engine = create_engine(DATABASE_URL)

# Cria a classe de sessão local do banco de dados.
# Esta é a base para as sessões que você usará para interagir com o DB.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para os modelos do SQLAlchemy.
# Seus modelos de tabela (como o 'User' em schemas.py) devem herdar desta Base.
Base = declarative_base()

# Dependência para obter a sessão do banco de dados (para uso nas rotas do FastAPI)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        # Garante que a sessão do banco de dados seja fechada após o uso
        db.close()
