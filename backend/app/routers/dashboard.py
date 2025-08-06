from fastapi import APIRouter
from app.database import get_connection

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("/")
def dashboard_info():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)  # IMPORTANTE: para receber dicts

    # Total de contratações
    cursor.execute("SELECT COUNT(*) AS total FROM contratacoesPncpUfca")
    row = cursor.fetchone()
    total_contratacoes = row["total"] if row and row["total"] is not None else 0

    # Total homologado
    cursor.execute("SELECT SUM(valor_total_homologado) AS total FROM resultadoItensContratacoesPncpUfca")
    row = cursor.fetchone()
    total_homologado = float(row["total"]) if row and row["total"] is not None else 0.0

    # Média de economia
    cursor.execute("""
        SELECT ROUND(AVG(i.valor_total_estimado - r.valor_total_homologado), 2) AS media
        FROM itensContratacoesPncpUfca i
        JOIN resultadoItensContratacoesPncpUfca r ON i.id_compra_item = r.id_compra_item
    """)
    row = cursor.fetchone()
    media_economia = float(row["media"]) if row and row["media"] is not None else 0.0

    conn.close()

    return {
        "total_contratacoes": total_contratacoes,
        "total_homologado": total_homologado,
        "media_economia": media_economia
    }
