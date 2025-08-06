from app.database import get_connection

def get_itens_contratacoes(ano: int = None):
    query = """
        SELECT 
            id_item, id_compra, ano_compra, descricao_item, quantidade_item, valor_unitario_estimado
        FROM 
            itensContratacoesPncpUfca
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
