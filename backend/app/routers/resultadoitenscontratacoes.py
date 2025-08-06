from fastapi import APIRouter, HTTPException
from app.database import get_connection

router = APIRouter(prefix="/resultadoitenscontratacoes", tags=["Resultado contratações"])

@router.get("/")
def listar_resultado_itens_contratacoes():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM resultadoitenscontratacoesPncpUfca")
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar os dados:{str(e)}")
    finally:
        cursor.close()
        conn.close()

