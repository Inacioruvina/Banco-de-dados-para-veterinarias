# ----------------------------------------------------------------------------------------
# operations.py  |  Funções de consulta (DQL) via pyodbc
# Todas usam marcador '?' para parametrização (padrão pyodbc / prevenção SQL Injection).
# ----------------------------------------------------------------------------------------


# ── 1. Busca por peso mínimo ───────────────────────────────────────────
def buscar_animais_por_peso(conexao, peso_minimo):
    """Retorna animais com peso maior que 'peso_minimo'."""
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


# Alias retrocompatível
search_by_weight = buscar_animais_por_peso


# ── 2. Consultas por veterinário ───────────────────────────────────────
def list_by_vet(conexao, id_vet):
    """Lista consultas realizadas por um veterinário (INNER JOIN)."""
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


# ── 3. Total de consultas por clínica (COUNT + GROUP BY) ───────────────
def consultas_por_clinica(conexao):
    """Conta consultas agrupadas por clínica (LEFT JOIN + COUNT + GROUP BY)."""
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


# ── 4. Animais vacinados com determinada vacina (SUB QUERY) ────────────
def find_vaccined_animals(conexao, nome_vacina):
    """Busca animais vacinados com uma vacina específica (IN + subconsulta)."""
    cursor = conexao.cursor()

    sql = """
        SELECT nome, especie
        FROM animal
        WHERE id_animal IN (
            SELECT id_animal
            FROM cartao_vacina
            WHERE nome_vacina = ?
        )
    """

    cursor.execute(sql, (nome_vacina,))
    resultados = cursor.fetchall()
    cursor.close()

    return resultados


# ── 5. Lista unificada de contatos (UNION) ─────────────────────────────
def unified_contact_list(conexao):
    """Une nomes e telefones de clientes e veterinários (UNION)."""
    cursor = conexao.cursor()

    sql = """
        SELECT nome, telefone
        FROM cliente
        UNION
        SELECT nome, telefone
        FROM veterinario
        ORDER BY nome ASC;
    """

    cursor.execute(sql)
    resultados = cursor.fetchall()
    cursor.close()

    return resultados


# ── 6. Animais por faixa de peso (BETWEEN) ─────────────────────────────
def buscar_animais_faixa_peso(conexao, peso_min, peso_max):
    """Retorna animais dentro de uma faixa de peso (BETWEEN)."""
    cursor = conexao.cursor()

    sql = """
        SELECT nome, especie, peso
        FROM animal
        WHERE peso BETWEEN ? AND ?
        ORDER BY peso ASC;
    """

    cursor.execute(sql, (peso_min, peso_max))
    resultados = cursor.fetchall()
    cursor.close()

    return resultados


# ── 7. Peso total por cliente (SUM + GROUP BY) ─────────────────────────
def peso_total_por_cliente(conexao):
    """Soma do peso total dos animais de cada cliente (SUM + GROUP BY)."""
    cursor = conexao.cursor()

    sql = """
        SELECT c.nome AS nome_cliente, SUM(a.peso) AS peso_total_animais
        FROM cliente AS c
        JOIN animal AS a ON c.id_cliente = a.id_cliente
        GROUP BY c.id_cliente, c.nome
        ORDER BY peso_total_animais DESC;
    """

    cursor.execute(sql)
    resultados = cursor.fetchall()
    cursor.close()

    return resultados


# ── 8. Espécies distintas atendidas (DISTINCT) ─────────────────────────
def listar_especies_atendidas(conexao):
    """Lista espécies distintas que já tiveram consulta (DISTINCT)."""
    cursor = conexao.cursor()

    sql = """
        SELECT DISTINCT a.especie
        FROM animal AS a
        JOIN consulta AS c ON c.id_animal = a.id_animal
        ORDER BY a.especie ASC;
    """

    cursor.execute(sql)
    resultados = cursor.fetchall()
    cursor.close()

    return resultados

# ----------------------------------------------------------------------------------------