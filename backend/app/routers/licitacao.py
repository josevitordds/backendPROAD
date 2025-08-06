from fastapi import APIRouter, HTTPException
from app.database import get_connection

router = APIRouter(prefix="/licitacao", tags=["Licitações"])

@router.get("/")
def listar_licitacoes():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM licitacoesUfca")
        resultados = cursor.fetchall()
        return resultados 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar licitações: {str(e)}")
    finally:
        cursor.close()
        conn.close()
