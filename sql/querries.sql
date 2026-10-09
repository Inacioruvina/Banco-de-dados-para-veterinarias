----------------------------------------------------------------------------------------
-- Código INÁCIO:
-- Consulta para verificar se o animal é um cão e se possui mais de 10kg.

SELECT nome, especie, raca, peso
FROM animal
WHERE raca = 'Cao' and peso > 10.0
ORDER BY peso DESC;

-- Consulta para identificar, a quantidade total e média de peso de cada raça de animal, de raças com mais de dois animais cadastrados

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
JOIN c.id_veterinario = v.id_veterinario;

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
FROM veterinario


----------------------------------------------------------------------------------------