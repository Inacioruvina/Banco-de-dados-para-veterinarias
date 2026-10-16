-- =============================================================================
-- queries.sql  |  Exemplos de consultas SQL (16 cláusulas exigidas)
-- Banco de dados: veterinaria_db (PostgreSQL)
-- =============================================================================

-- ─────────────────────────────────────────────────────────────────────────────
-- 1. INNER JOIN
--    Junção entre consulta, animal e veterinario para listar
--    os atendimentos realizados.
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    c.horario,
    c.diagnostico,
    a.nome AS nome_animal,
    v.nome AS nome_veterinario
FROM consulta AS c
INNER JOIN animal AS a ON c.id_animal = a.id_animal
INNER JOIN veterinario AS v ON c.id_veterinario = v.id_veterinario;


-- ─────────────────────────────────────────────────────────────────────────────
-- 2. OUTER JOIN (LEFT OUTER JOIN)
--    Lista todos os animais, incluindo aqueles que nunca consultaram.
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    a.nome AS animal,
    a.especie,
    c.data_de_atendimento,
    c.motivo
FROM animal AS a
LEFT OUTER JOIN consulta AS c ON a.id_animal = c.id_animal;


-- ─────────────────────────────────────────────────────────────────────────────
-- 3. NATURAL JOIN
--    Junção natural entre animal e prontuario (pela coluna id_animal em comum).
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    a.nome AS animal,
    a.especie,
    p.historico_saude,
    p.alergias
FROM animal AS a
NATURAL JOIN prontuario AS p;


-- ─────────────────────────────────────────────────────────────────────────────
-- 4. INTERSECT (INTERSECTION)
--    Animais que possuem consulta E também possuem vacina registrada.
-- ─────────────────────────────────────────────────────────────────────────────
SELECT id_animal
FROM consulta
INTERSECT
SELECT id_animal
FROM cartao_vacina;


-- ─────────────────────────────────────────────────────────────────────────────
-- 5. CHECK
--    Demonstrado no schema (ddl_schema.sql). Exemplos aplicados:
--      - chk_animal_especie: especie IN ('Cão','Cao','Gato','Ave',...)
--      - chk_animal_peso:    peso > 0
--      - chk_animal_sexo:    sexo IN ('M','F','Macho','Fêmea','Femea')
--      - chk_vacina_dose:    numero_da_dose > 0
--    Consulta que lista as constraints CHECK ativas no banco:
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    conname         AS nome_constraint,
    conrelid::regclass AS tabela,
    pg_get_constraintdef(oid) AS definicao
FROM pg_constraint
WHERE contype = 'c'
  AND connamespace = 'public'::regnamespace
ORDER BY conrelid::regclass::text, conname;


-- ─────────────────────────────────────────────────────────────────────────────
-- 6. LIKE
--    Busca animais cujo nome começa com a letra 'L'.
-- ─────────────────────────────────────────────────────────────────────────────
SELECT nome, especie, raca
FROM animal
WHERE nome LIKE 'L%';


-- ─────────────────────────────────────────────────────────────────────────────
-- 7. BETWEEN
--    Relatório de animais na faixa de peso de 5 a 30 kg.
-- ─────────────────────────────────────────────────────────────────────────────
SELECT nome, especie, peso
FROM animal
WHERE peso BETWEEN 5 AND 30
ORDER BY peso ASC;


-- ─────────────────────────────────────────────────────────────────────────────
-- 8. TRIGGER
--    Definida no arquivo sql/automation.sql:
--      - Função: fn_atualizar_prontuario_vacina()
--      - Trigger: trg_atualiza_prontuario_vacina
--    Ação: ao inserir uma vacina em cartao_vacina, o trigger concatena
--    o nome da vacina ao campo historico_saude do prontuario do animal.
--    Consulta para verificar que o trigger existe:
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    tgname       AS nome_trigger,
    tgrelid::regclass AS tabela,
    proname      AS funcao
FROM pg_trigger t
JOIN pg_proc p ON t.tgfoid = p.oid
WHERE NOT tgisinternal
ORDER BY tgname;


-- ─────────────────────────────────────────────────────────────────────────────
-- 9. DISTINCT
--    Lista de espécies distintas que já foram atendidas em consulta.
-- ─────────────────────────────────────────────────────────────────────────────
SELECT DISTINCT a.especie
FROM animal AS a
JOIN consulta AS c ON c.id_animal = a.id_animal
ORDER BY a.especie ASC;


-- ─────────────────────────────────────────────────────────────────────────────
-- 10. ASSERTION (nota explicativa)
--    O padrão SQL define ASSERTION como restrições globais ao schema.
--    O PostgreSQL NÃO implementa CREATE ASSERTION.
--    A alternativa equivalente são constraints CHECK em nível de tabela
--    (seção 5 acima) e triggers (seção 8 acima) para validações complexas.
--    Exemplo conceitual (sintaxe padrão SQL, NÃO suportada pelo PostgreSQL):
--
--    CREATE ASSERTION chk_peso_positivo
--    CHECK (NOT EXISTS (SELECT 1 FROM animal WHERE peso <= 0));
--
--    No nosso schema isso é garantido por:
--      ALTER TABLE animal ADD CONSTRAINT chk_animal_peso CHECK (peso > 0);
-- ─────────────────────────────────────────────────────────────────────────────


-- ─────────────────────────────────────────────────────────────────────────────
-- 11. SUB QUERY (subconsulta com IN)
--    Animais vacinados com a vacina 'Anti-Rabica'.
-- ─────────────────────────────────────────────────────────────────────────────
SELECT nome, especie
FROM animal
WHERE id_animal IN (
    SELECT id_animal
    FROM cartao_vacina
    WHERE nome_vacina = 'Anti-Rabica'
);


-- ─────────────────────────────────────────────────────────────────────────────
-- 12. AVG (média de peso agrupada por espécie)
--    Calcula o peso médio por espécie.
-- ─────────────────────────────────────────────────────────────────────────────
SELECT especie, AVG(peso) AS peso_medio
FROM animal
GROUP BY especie
ORDER BY peso_medio DESC;


-- ─────────────────────────────────────────────────────────────────────────────
-- 13. SUM (soma do peso total acumulado por cliente)
--    Peso total dos animais de cada cliente.
-- ─────────────────────────────────────────────────────────────────────────────
SELECT c.nome AS nome_cliente, SUM(a.peso) AS peso_total_animais
FROM cliente AS c
JOIN animal AS a ON c.id_cliente = a.id_cliente
GROUP BY c.id_cliente, c.nome
ORDER BY peso_total_animais DESC;


-- ─────────────────────────────────────────────────────────────────────────────
-- 14. COUNT (contagem total de consultas por clínica)
--    Total de consultas realizadas em cada clínica.
-- ─────────────────────────────────────────────────────────────────────────────
SELECT cl.nome AS nome_clinica, COUNT(c.id_consulta) AS total_consultas
FROM clinica AS cl
LEFT JOIN consulta AS c ON cl.id_clinica = c.id_clinica
GROUP BY cl.id_clinica, cl.nome
ORDER BY total_consultas DESC;


-- ─────────────────────────────────────────────────────────────────────────────
-- 15. ORDER BY (ordenação ASC e DESC)
--    Lista animais ordenados por peso crescente e nome decrescente.
-- ─────────────────────────────────────────────────────────────────────────────
SELECT nome, especie, peso
FROM animal
ORDER BY peso ASC, nome DESC;


-- ─────────────────────────────────────────────────────────────────────────────
-- 16. GROUP BY com HAVING
--    Espécies que possuem mais de 2 animais cadastrados,
--    com contagem e peso médio.
-- ─────────────────────────────────────────────────────────────────────────────
SELECT especie, COUNT(*) AS total, AVG(peso) AS peso_medio
FROM animal
GROUP BY especie
HAVING COUNT(*) > 2;

-- =============================================================================
-- FIM — 16 cláusulas/comandos exigidos pela avaliação
-- =============================================================================
