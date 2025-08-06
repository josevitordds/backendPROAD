from fastapi import APIRouter, HTTPException
from app.database import get_connection

router = APIRouter(prefix="/itenscontratacoes", tags=["Itens de Contratações"])

@router.get("/")
def listar_itens_contratacoes():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM itensContratacoesPncpUfca")
        resultados = cursor.fetchall()
        return resultados 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar itens de contratações: {str(e)}")
    finally:
        cursor.close()
        conn.close()
