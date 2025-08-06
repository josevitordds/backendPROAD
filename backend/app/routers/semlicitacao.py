from fastapi import APIRouter, HTTPException
from app.database import get_connection

router = APIRouter(prefix="/semlicitacao", tags=["sem licitações"])

@router.get("/")
def listar_contratacoes():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM compraSemLicitacaoPncp")
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"erro ao buscar os dados: {str(e)}")
    finally:
        cursor.close()
        conn.close()

