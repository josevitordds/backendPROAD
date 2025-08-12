from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Compras UFCA")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

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
app.include_router(auth.router)  
