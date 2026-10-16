----------------------------------------------------------------------------------------
-- Código INÁCIO:
-- Consulta para verificar se o animal é um cão e se possui mais de 10kg.

SELECT nome, especie, raca, peso
FROM animal
WHERE especie = 'Cao' and peso > 10.0
ORDER BY peso DESC;

-- Consulta para identificar, a quantidade total e média de peso de cada especie de animal, de especies com mais de dois animais cadastrados

SELECT especie, COUNT(*), AVG(peso)
FROM animal
GROUP BY especie
HAVING COUNT(*) > 2;

-- Consulta para verificar os proprietários

SELECT a.nome AS nome_animal, c.nome AS nome_dono
FROM animal a 
JOIN cliente c ON a.id_cliente = c.id_cliente;

-- Consulta para verificar o nome do animal, data da consulta e o nome do veterinario

SELECT a.nome AS nome_animal, c.data_de_atendimento, v.nome AS veterinario
FROM consulta c
JOIN animal a ON c.id_animal = a.id_animal
JOIN veterinario v ON c.id_veterinario = v.id_veterinario;

-- Consulta para verificar todos os animais vacinados com a "Anti-rabica"

SELECT nome, especie
FROM animal
WHERE id_animal IN (
    SELECT id_animal
    FROM cartao_vacina
    WHERE nome_vacina = 'Anti-Rabica'
);
-- União do nome e telefone dos clientes com o nome e o telefone dos veterinários

SELECT nome, telefone
FROM cliente 
UNION
SELECT nome, telefone
FROM veterinario;

-- Utilização de tabelas temporárias para selecionar as especies com o peso medio maior do que 5

WITH Tabela_media AS (
    SELECT especie, AVG(peso) AS peso_medio
    FROM animal
    GROUP BY especie
)
SELECT peso_medio, especie
FROM Tabela_media
WHERE peso_medio > 5;

-- Seleção de animais que ja tiveram consultas

SELECT 
    c.horario,
    c.diagnostico,
    a.nome AS nome_animal,
    v.nome AS nome_veterinario
FROM consulta AS c
INNER JOIN animal AS a ON c.id_animal = a.id_animal
INNER JOIN veterinario AS v ON c.id_veterinario = v.id_veterinario;


-- Lista todos os animais e suas consultas (Incluindo animais que nunca consultaram)

SELECT 
    a.nome AS animal,
    a.especie,
    c.data_de_atendimento,
    c.motivo
FROM animal AS a
LEFT OUTER JOIN consulta AS c ON a.id_animal = c.id_animal;

-- Junção das duas tables animal e prontuario

SELECT 
    a.nome AS animal,
    a.especie,
    p.historico_saude,
    p.alergias
FROM animal AS a
NATURAL JOIN prontuario AS p;

-- Lista animais que passaram por consultas e já vacinaram

SELECT id_animal 
FROM consulta
INTERSECT
SELECT id_animal FROM cartao_vacina;

-- Seleção de animais que começam com a letra desejada

SELECT nome, especie, raca
FROM animal
WHERE nome LIKE '%L';
----------------------------------------------------------------------------------------