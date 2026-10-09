#----------------------------------------------------------------------------------------
# Código INÁCIO

# Função de busca por peso

def search_by_weight(conexao, peso_minimo):
    cursor = conexao.cursor()
    
    sql = """
        SELECT nome, especie, raca, peso
        FROM animal
        WHERE peso > ?
        ORDER BY peso DESC;
    """
    
    cursor.execute(sql, (peso_minimo,))
    resultados = cursor.fetchall()
    cursor.close()
    
    return resultados

#----------------------------------------------------------------------------------------