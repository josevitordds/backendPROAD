from fastapi import APIRouter, HTTPException
from app.database import get_connection

router = APIRouter(prefix="/contratacoes", tags=["Contratações"])

@router.get("/")
def listar_contratacoes():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contratacoesPncpUfca")
        resultados = cursor.fetchall()
        return resultados  
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar contratações: {str(e)}")
    finally:
        cursor.close()
        conn.close()
