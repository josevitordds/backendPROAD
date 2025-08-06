from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importação das rotas
from app.routers import (
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
)

# Instância da aplicação
app = FastAPI(title="API Compras UFCA")

# Configuração de CORS (libera acesso de qualquer origem)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, troque por ["https://seusite.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro das rotas
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
