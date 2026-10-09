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

# Função de listagem de consulta por veterinário

def list_by_vet(conexao, id_vet):
    cursor = conexao.cursor()
    
    sql = """
        SELECT c.data_de_atendimento, c.motivo, c.diagnostico, a.nome AS nome_animal
        FROM consulta AS c
        JOIN animal AS a ON c.id_animal = a.id_animal
        WHERE c.id_veterinario = ?
        ORDER BY c.data_de_atendimento DESC;
    """
    
    cursor.execute(sql, (id_vet,))
    resultados = cursor.fetchall()
    cursor.close()
    
    return resultados
    
# Função para calcular o total de consutlas

def consultas_por_clinica(conexao):
    cursor = conexao.cursor()
    
    sql = """
        SELECT cl.id_clinica, cl.nome, COUNT(c.id_consulta) AS total_consultas
        FROM clinica AS cl
        LEFT JOIN consulta AS c ON cl.id_clinica = c.id_clinica
        GROUP BY cl.id_clinica, cl.nome
        ORDER BY total_consultas DESC;
    """
    
    cursor.execute(sql)
    resultados = cursor.fetchall()
    cursor.close()
    
    return resultados
    
#----------------------------------------------------------------------------------------