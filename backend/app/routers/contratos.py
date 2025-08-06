from fastapi import APIRouter, HTTPException
from app.database import get_connection

router = APIRouter(prefix="/contratos", tags=["Contratos"])

@router.get("/")
def listar_contratos():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contratosPncpDetalhado")
        resultados = cursor.fetchall()
        return resultados  
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar contratos: {str(e)}")
    finally:
        cursor.close()
        conn.close()
