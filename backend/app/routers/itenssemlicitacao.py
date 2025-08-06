from fastapi import APIRouter, HTTPException
from app.database import get_connection

router = APIRouter(prefix="/itenssemlicitacao", tags=["Itens Sem Licitação"])

@router.get("/")
def listar_itens_sem_licitacao():
    """
    Retorna todos os itens da tabela itensCompraSemLicitacaoPncp como dicionários.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM itensCompraSemLicitacaoPncp")
        resultados = cursor.fetchall()
        return resultados  # Lista de dicionários
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar itens sem licitação: {str(e)}")
    finally:
        cursor.close()
        conn.close()
