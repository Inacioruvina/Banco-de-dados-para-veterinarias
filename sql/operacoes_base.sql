-- Exercícios de DDL e DML em uma tabela temporária.
BEGIN;

CREATE TEMP TABLE exemplo_cliente (
    id_cliente INTEGER PRIMARY KEY,
    nome VARCHAR(128) NOT NULL,
    telefone VARCHAR(20)
);
ALTER TABLE exemplo_cliente
    ADD COLUMN situacao VARCHAR(10) NOT NULL DEFAULT 'ativo';
ALTER TABLE exemplo_cliente
    ALTER COLUMN telefone TYPE VARCHAR(30);

INSERT INTO exemplo_cliente (id_cliente, nome, telefone)
VALUES (1, 'Ana Exemplo', '(00) 90000-0001'),
       (2, 'Bruno Exemplo', '(00) 90000-0002');

UPDATE exemplo_cliente
SET situacao = CASE
    WHEN id_cliente = 1 THEN 'revisado'
    ELSE situacao
END
WHERE id_cliente = 1;

DELETE FROM exemplo_cliente WHERE id_cliente = 2;
SELECT * FROM exemplo_cliente ORDER BY id_cliente;

DROP TABLE IF EXISTS exemplo_cliente CASCADE;
COMMIT;
