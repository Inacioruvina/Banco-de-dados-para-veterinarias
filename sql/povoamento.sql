-- Dados de teste. Execute depois de ddl_schema.sql.
BEGIN;

INSERT INTO clinicas (nome, telefone, endereco)
SELECT 'Clinica Exemplo Norte', '(00) 0000-0001', 'Rua Exemplo, 10'
WHERE NOT EXISTS (
    SELECT 1 FROM clinicas
    WHERE nome = 'Clinica Exemplo Norte' AND telefone = '(00) 0000-0001'
);

INSERT INTO clinicas (nome, telefone, endereco)
SELECT 'Clinica Exemplo Sul', '(00) 0000-0002', 'Avenida Exemplo, 20'
WHERE NOT EXISTS (
    SELECT 1 FROM clinicas
    WHERE nome = 'Clinica Exemplo Sul' AND telefone = '(00) 0000-0002'
);

INSERT INTO clientes (nome, telefone, email)
SELECT 'Ana Exemplo', '(00) 90000-0001', 'ana.exemplo@exemplo.com'
WHERE NOT EXISTS (SELECT 1 FROM clientes WHERE email = 'ana.exemplo@exemplo.com');

INSERT INTO clientes (nome, telefone, email)
SELECT 'Bruno Exemplo', '(00) 90000-0002', 'bruno.exemplo@exemplo.com'
WHERE NOT EXISTS (SELECT 1 FROM clientes WHERE email = 'bruno.exemplo@exemplo.com');

INSERT INTO animais (nome, especie, raca, data_nascimento, id_cliente)
SELECT 'Luna', 'Cão', 'Vira-lata', DATE '2021-04-12', c.id_cliente
FROM clientes AS c
WHERE c.email = 'ana.exemplo@exemplo.com'
  AND NOT EXISTS (
      SELECT 1 FROM animais AS a
      WHERE a.id_cliente = c.id_cliente AND a.nome = 'Luna'
        AND a.data_nascimento = DATE '2021-04-12'
  );

INSERT INTO animais (nome, especie, raca, data_nascimento, id_cliente)
SELECT 'Tico', 'Gato', 'Siames', DATE '2022-09-03', c.id_cliente
FROM clientes AS c
WHERE c.email = 'ana.exemplo@exemplo.com'
  AND NOT EXISTS (
      SELECT 1 FROM animais AS a
      WHERE a.id_cliente = c.id_cliente AND a.nome = 'Tico'
        AND a.data_nascimento = DATE '2022-09-03'
  );

INSERT INTO animais (nome, especie, raca, data_nascimento, id_cliente)
SELECT 'Mel', 'Cão', 'Poodle', DATE '2020-01-20', c.id_cliente
FROM clientes AS c
WHERE c.email = 'bruno.exemplo@exemplo.com'
  AND NOT EXISTS (
      SELECT 1 FROM animais AS a
      WHERE a.id_cliente = c.id_cliente AND a.nome = 'Mel'
        AND a.data_nascimento = DATE '2020-01-20'
  );

-- Implementação do Eduardo
--4. VETERINARIOS
INSERT INTO veterinarios (nome, crmv, id_clinica)
SELECT 'Dra. Sofia Mendes', 'CRMV-TO 1234', cl.id_cliente
FROM clinicas AS cl
WHERE cl.nome = 'Clinica Exemplo Norte'
 AND NOT EXISTS(
  SELECT 1 FROM veterinarios WHERE crmv = 'CRMV-TO 1234'
 );

--5. CONSULTAS
 INSERT INTO consultas (data_hora, diagnostico, valor, id_animal, id_veterinario, id_clinica)
SELECT TIMESTAMP '2026-03-10 14:00:00', 'Consulta de rotina e vacinação', 150.00, a.id_animal, v.id_veterinario, cl.id_clinica
FROM animais AS a, veterinarios AS v, clinicas AS cl
WHERE a.nome = 'Luna' 
  AND v.crmv = 'CRMV-TO 1234' 
  AND cl.nome = 'Clinica Exemplo Norte'
  AND NOT EXISTS (
      SELECT 1 FROM consultas WHERE data_hora = TIMESTAMP '2026-03-10 14:00:00' AND id_animal = a.id_animal
  );

-- 6. MEDICAMENTOS
  INSERT INTO medicamentos (nome, dosagem, id_consulta)
SELECT 'Vermífugo Vet', '1 comprimido via oral', c.id_consulta
FROM consultas AS c
JOIN animais AS a ON c.id_animal = a.id_animal
WHERE a.nome = 'Luna' AND c.data_hora = TIMESTAMP '2026-03-10 14:00:00'
  AND NOT EXISTS (
      SELECT 1 FROM medicamentos WHERE nome = 'Vermífugo Vet' AND id_consulta = c.id_consulta
  );

7. AGENDAMENTOS
  INSERT INTO agendamentos (data_hora, status, id_animal, id_veterinario)
SELECT TIMESTAMP '2026-11-05 10:00:00', 'Agendado', a.id_animal, v.id_veterinario
FROM animais AS a, veterinarios AS v
WHERE a.nome = 'Tico' AND v.crmv = 'CRMV-TO 1234'
  AND NOT EXISTS (
      SELECT 1 FROM agendamentos WHERE data_hora = TIMESTAMP '2026-11-05 10:00:00' AND id_animal = a.id_animal
  );

  -- 8. VACINAS
 
INSERT INTO vacinas (nome_vacina, data_aplicacao, proxima_dose, id_animal)
SELECT 'Antirrábica', DATE '2026-03-10', DATE '2027-03-10', a.id_animal
FROM animais AS a
WHERE a.nome = 'Luna'
  AND NOT EXISTS (
      SELECT 1 FROM vacinas WHERE nome_vacina = 'Antirrábica' AND id_animal = a.id_animal
  );

  -- 9. PRONTUARIO
  INSERT INTO prontuario (historico_medico, ultima_atualizacao, id_animal)
SELECT 'Animal saudável, histórico de vacinas em dia.', TIMESTAMP '2026-03-10 14:30:00', a.id_animal
FROM animais AS a
WHERE a.nome = 'Luna'
  AND NOT EXISTS (
      SELECT 1 FROM prontuario WHERE id_animal = a.id_animal
  );