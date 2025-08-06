from app.database import get_connection

def get_resultado_itens_contratacoes(ano: int = None):
    query = """
        SELECT 
            id_compra_item, id_compra,data_inclusao 
        FROM 
            resultadoItensContratacoesPncpUfca
    """
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
