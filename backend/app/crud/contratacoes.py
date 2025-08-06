from app.database import get_connection

# 🔍 READ (com filtro opcional por ano)
def get_contratacoes(ano: int = None):
    query = "SELECT id_compra, ano_compra, objeto_compra, valor_estimado FROM contratacoesPncpUfca"
    params = []
    if ano is not None:
        query += " WHERE ano_compra = %s"
        params.append(ano)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, tuple(params))
    result = cursor.fetchall()
    conn.close()

    return result


# ➕ CREATE (adicionar nova contratação)
def add_contratacao(id_compra: str, ano_compra: int, objeto_compra: str, valor_estimado: float):
    query = """
        INSERT INTO contratacoesPncpUfca (id_compra, ano_compra, objeto_compra, valor_estimado)
        VALUES (%s, %s, %s, %s)
    """

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, (id_compra, ano_compra, objeto_compra, valor_estimado))
    conn.commit()
    conn.close()


# ❌ DELETE (remover contratação por ID)
def delete_contratacao(id_compra: str):
    query = "DELETE FROM contratacoesPncpUfca WHERE id_compra = %s"

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, (id_compra,))
    conn.commit()
    conn.close()
