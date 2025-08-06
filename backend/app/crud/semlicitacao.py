from app.database import get_connection

def get_contratos(ano: int = None):
    query = "SELECT id_compra, ano_compra FROM compraSemLicitacaoPncp"
    params = []
    if ano:
        query += " WHERE ano_compra = %s"
        params.append(ano)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, tuple(params))
    result = cursor.fetchall()
    conn.close()

    return result
