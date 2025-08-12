# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Classe de configurações da aplicação, carregando variáveis de ambiente.
    As variáveis de ambiente DEVEM ser definidas em um arquivo .env na raiz do projeto.
    """
    # Deixe os valores padrão como placeholders ou vazios para variáveis que vêm do .env
    SECRET_KEY: str # Não defina um valor padrão seguro aqui, ele deve vir do .env
    ALGORITHM: str = "HS256" # Pode manter um padrão se for fixo, ou deixar sem padrão
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 # Pode manter um padrão se for fixo, ou deixar sem padrão
    DATABASE_URL: str # Não defina a URL do DB aqui, ela deve vir do .env
    
    class Config:
        env_file = ".env" 
        # Isso garante que as variáveis do .env serão carregadas e substituirão os padrões
        # se elas forem definidas no .env.

settings = Settings()
