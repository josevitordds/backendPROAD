from fastapi import APIRouter, HTTPException
from app.database import get_connection

router = APIRouter(prefix="/itenscontratos", tags=["Itens de Contratos"])

@router.get("/")
def listar_itens_contratos():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM itensContratoPncpUfca")
        resultados = cursor.fetchall()
        return resultados  
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar itens de contratos: {str(e)}")
    finally:
        cursor.close()
        conn.close()
