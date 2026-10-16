-- =============================================================================
-- povoamento.sql  |  Dados de teste (7 tabelas do ddl_schema.sql)
-- Execute DEPOIS de ddl_schema.sql e UMA vez por schema criado.
-- Para recomecar do zero, execute ddl_schema.sql novamente (ele recria tudo).
-- Os dados sao ficticios.
-- Obs.: a especie usa 'Cao' (sem acento) para casar com querries.sql/operations.py.
-- =============================================================================
BEGIN;

INSERT INTO clinica (nome, telefone, endereco) VALUES
    ('Clinica Exemplo Norte', '(00) 0000-0001', 'Rua Exemplo, 10'),
    ('Clinica Exemplo Sul',   '(00) 0000-0002', 'Avenida Exemplo, 20');

INSERT INTO cliente (nome, cpf, telefone, endereco, id_clinica) VALUES
    ('Ana Exemplo',   '111.111.111-11', '(00) 90000-0001', 'Rua A, 1',
        (SELECT id_clinica FROM clinica WHERE nome = 'Clinica Exemplo Norte')),
    ('Bruno Exemplo', '222.222.222-22', '(00) 90000-0002', 'Rua B, 2',
        (SELECT id_clinica FROM clinica WHERE nome = 'Clinica Exemplo Sul')),
    ('Carla Exemplo', '333.333.333-33', '(00) 90000-0003', 'Rua C, 3',
        (SELECT id_clinica FROM clinica WHERE nome = 'Clinica Exemplo Norte'));

INSERT INTO veterinario (nome, crmv, telefone, especialidade, id_clinica) VALUES
    ('Dr. Paulo Exemplo',   'CRMV-00 1001', '(00) 91000-0001', 'Clinica Geral',
        (SELECT id_clinica FROM clinica WHERE nome = 'Clinica Exemplo Norte')),
    ('Dra. Marina Exemplo', 'CRMV-00 1002', '(00) 91000-0002', 'Felinos',
        (SELECT id_clinica FROM clinica WHERE nome = 'Clinica Exemplo Sul'));

INSERT INTO animal (nome, especie, raca, sexo, data_de_nascimento, peso, id_cliente) VALUES
    ('Luna', 'Cao',  'Vira-lata',      'F', DATE '2021-04-12', 12.50,
        (SELECT id_cliente FROM cliente WHERE nome = 'Ana Exemplo')),
    ('Tico', 'Gato', 'Siames',         'M', DATE '2022-09-03',  4.30,
        (SELECT id_cliente FROM cliente WHERE nome = 'Ana Exemplo')),
    ('Mel',  'Cao',  'Poodle',         'F', DATE '2020-01-20',  6.80,
        (SELECT id_cliente FROM cliente WHERE nome = 'Bruno Exemplo')),
    ('Rex',  'Cao',  'Pastor Alemao',  'M', DATE '2018-03-10', 28.40,
        (SELECT id_cliente FROM cliente WHERE nome = 'Bruno Exemplo')),
    ('Thor', 'Cao',  'Labrador',       'M', DATE '2019-06-15', 32.00,
        (SELECT id_cliente FROM cliente WHERE nome = 'Carla Exemplo'));

INSERT INTO prontuario (nome, historico_saude, alergias, observacoes, id_animal) VALUES
    ('Prontuario Luna', 'Castrada em 2022.',  NULL,                'Animal docil.',
        (SELECT id_animal FROM animal WHERE nome = 'Luna')),
    ('Prontuario Tico', 'Sem intercorrencias.', 'Alergia a frango', NULL,
        (SELECT id_animal FROM animal WHERE nome = 'Tico')),
    ('Prontuario Thor', 'Displasia leve de quadril.', NULL,        'Acompanhar peso.',
        (SELECT id_animal FROM animal WHERE nome = 'Thor'));

INSERT INTO cartao_vacina (nome_vacina, data_aplicacao, numero_da_dose, proxima_dose,
                           observacoes, id_animal, id_veterinario) VALUES
    ('Anti-Rabica', DATE '2025-03-10', 1, DATE '2026-03-10', NULL,
        (SELECT id_animal FROM animal WHERE nome = 'Luna'),
        (SELECT id_veterinario FROM veterinario WHERE nome = 'Dr. Paulo Exemplo')),
    ('Anti-Rabica', DATE '2025-05-02', 1, DATE '2026-05-02', NULL,
        (SELECT id_animal FROM animal WHERE nome = 'Thor'),
        (SELECT id_veterinario FROM veterinario WHERE nome = 'Dr. Paulo Exemplo')),
    ('V4',          DATE '2025-06-20', 2, NULL,              NULL,
        (SELECT id_animal FROM animal WHERE nome = 'Tico'),
        (SELECT id_veterinario FROM veterinario WHERE nome = 'Dra. Marina Exemplo'));

INSERT INTO consulta (data_de_atendimento, horario, motivo, diagnostico, observacoes,
                      id_animal, id_veterinario, id_clinica) VALUES
    (DATE '2025-03-10', TIME '09:00', 'Vacinacao',       'Saudavel',         NULL,
        (SELECT id_animal FROM animal WHERE nome = 'Luna'),
        (SELECT id_veterinario FROM veterinario WHERE nome = 'Dr. Paulo Exemplo'),
        (SELECT id_clinica FROM clinica WHERE nome = 'Clinica Exemplo Norte')),
    (DATE '2025-04-15', TIME '14:30', 'Coceira intensa', 'Dermatite alergica', 'Retorno em 15 dias',
        (SELECT id_animal FROM animal WHERE nome = 'Tico'),
        (SELECT id_veterinario FROM veterinario WHERE nome = 'Dra. Marina Exemplo'),
        (SELECT id_clinica FROM clinica WHERE nome = 'Clinica Exemplo Sul')),
    (DATE '2025-05-02', TIME '10:15', 'Claudicacao',     'Displasia leve',   NULL,
        (SELECT id_animal FROM animal WHERE nome = 'Thor'),
        (SELECT id_veterinario FROM veterinario WHERE nome = 'Dr. Paulo Exemplo'),
        (SELECT id_clinica FROM clinica WHERE nome = 'Clinica Exemplo Norte')),
    (DATE '2025-07-01', TIME '16:00', 'Check-up anual',  'Saudavel',         NULL,
        (SELECT id_animal FROM animal WHERE nome = 'Mel'),
        (SELECT id_veterinario FROM veterinario WHERE nome = 'Dra. Marina Exemplo'),
        (SELECT id_clinica FROM clinica WHERE nome = 'Clinica Exemplo Sul'));

COMMIT;
