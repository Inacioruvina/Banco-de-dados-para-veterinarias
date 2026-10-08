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
