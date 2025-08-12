from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importações relativas para os módulos dentro do pacote 'app'
from .database import Base, engine
from .routers import (
    contratacoes,
    dashboard,
    itenscontratacoes,
    resultadoitenscontratacoes,
    contratos,
    itenscontratos,
    semlicitacao,
    itenssemlicitacao,
    licitacao,
    itenslicitacao,
    auth,
)

# Cria as tabelas no banco de dados se elas ainda não existirem.
# É crucial que isso seja feito ANTES da inicialização da aplicação FastAPI.
Base.metadata.create_all(bind=engine)

# Instância da aplicação FastAPI
app = FastAPI(title="API Compras UFCA")

# Configuração de CORS (Cross-Origin Resource Sharing)
# Permite que seu frontend (rodando em um domínio diferente) se comunique com este backend.
# Em produção, você DEVE substituir "*" por uma lista específica dos domínios do seu frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Exemplo: ["http://localhost:3000", "https://seusite.com"]
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos nas requisições
)

# Registro de todos os roteadores da sua API
app.include_router(contratacoes.router)
app.include_router(dashboard.router)
app.include_router(itenscontratacoes.router)
app.include_router(resultadoitenscontratacoes.router)
app.include_router(contratos.router)
app.include_router(itenscontratos.router)
app.include_router(semlicitacao.router)
app.include_router(itenssemlicitacao.router)
app.include_router(licitacao.router)
app.include_router(itenslicitacao.router)
app.include_router(auth.router)  # Roteador para autenticação (cadastro e login)
