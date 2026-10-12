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

COMMIT;
