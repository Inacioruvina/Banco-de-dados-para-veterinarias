-- =============================================================================
-- ddl_schema.sql  |  Banco de dados da clinica veterinaria (PostgreSQL)
-- Execute ANTES de povoamento.sql:
--     psql -U <usuario> -d <banco> -f sql/ddl_schema.sql
--
-- Tabelas (ordem de dependencia das chaves estrangeiras):
--   clinica -> cliente -> animal -> prontuario
--   clinica -> veterinario -> cartao_vacina / consulta
-- O script e idempotente: pode ser executado varias vezes (recria tudo).
-- =============================================================================
BEGIN;

-- -----------------------------------------------------------------------------
-- 1. DROP: ordem inversa das dependencias.
--    As 3 ultimas linhas removem as tabelas no plural da versao antiga do
--    schema (clinicas, clientes, animais), caso existam em algum banco local.
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS consulta       CASCADE;
DROP TABLE IF EXISTS cartao_vacina  CASCADE;
DROP TABLE IF EXISTS prontuario     CASCADE;
DROP TABLE IF EXISTS animal         CASCADE;
DROP TABLE IF EXISTS veterinario    CASCADE;
DROP TABLE IF EXISTS cliente        CASCADE;
DROP TABLE IF EXISTS clinica        CASCADE;
DROP TABLE IF EXISTS animais        CASCADE;  -- legado
DROP TABLE IF EXISTS clientes       CASCADE;  -- legado
DROP TABLE IF EXISTS clinicas       CASCADE;  -- legado

-- -----------------------------------------------------------------------------
-- 2. CREATE TABLE
-- -----------------------------------------------------------------------------

-- 2.1 clinica
CREATE TABLE clinica (
    id_clinica  SERIAL PRIMARY KEY,
    nome        VARCHAR(128) NOT NULL,
    telefone    VARCHAR(20),
    endereco    TEXT
);

-- 2.2 cliente
--     id_clinica e a FK de cliente: a constraint e adicionada via ALTER TABLE
--     na secao 3 (a coluna ja nasce na posicao final).
CREATE TABLE cliente (
    id_cliente  SERIAL PRIMARY KEY,
    nome        VARCHAR(128) NOT NULL,
    cpf         VARCHAR(14),
    telefone    VARCHAR(20),
    endereco    TEXT,
    id_clinica  INTEGER
);

-- 2.3 veterinario
CREATE TABLE veterinario (
    id_veterinario  SERIAL PRIMARY KEY,
    nome            VARCHAR(128) NOT NULL,
    crmv            VARCHAR(20),
    telefone        VARCHAR(20),
    especialidade   VARCHAR(50),
    id_clinica      INTEGER NOT NULL
        REFERENCES clinica (id_clinica) ON DELETE CASCADE
);

-- 2.4 animal
--     especie aceita 'Cão' (acentuado, usado em povoamento.sql) e 'Cao'
--     (sem acento, usado em querries.sql / operations.py), alem de outras
--     especies comuns, para que o CHECK nao bloqueie os INSERTs dos demais.
CREATE TABLE animal (
    id_animal           SERIAL PRIMARY KEY,
    nome                VARCHAR(128) NOT NULL,
    especie             VARCHAR(50)  NOT NULL
        CONSTRAINT chk_animal_especie CHECK (especie IN (
            'Cão', 'Cao', 'Gato', 'Ave', 'Roedor', 'Coelho',
            'Réptil', 'Reptil', 'Outro')),
    raca                VARCHAR(50),
    sexo                VARCHAR(10),
    data_de_nascimento  DATE,
    peso                NUMERIC(5,2),
    id_cliente          INTEGER NOT NULL
        REFERENCES cliente (id_cliente) ON DELETE CASCADE
);

-- 2.5 prontuario
CREATE TABLE prontuario (
    id_prontuario    SERIAL PRIMARY KEY,
    nome             VARCHAR(128) NOT NULL,
    historico_saude  TEXT,
    alergias         TEXT,
    observacoes      TEXT,
    id_animal        INTEGER NOT NULL
        REFERENCES animal (id_animal) ON DELETE CASCADE
);

-- 2.6 cartao_vacina
CREATE TABLE cartao_vacina (
    id_vacina       SERIAL PRIMARY KEY,
    nome_vacina     VARCHAR(100) NOT NULL,
    data_aplicacao  DATE NOT NULL,
    numero_da_dose  INTEGER,
    proxima_dose    DATE,
    observacoes     TEXT,
    id_animal       INTEGER NOT NULL
        REFERENCES animal (id_animal) ON DELETE CASCADE,
    id_veterinario  INTEGER
        REFERENCES veterinario (id_veterinario) ON DELETE CASCADE
);

-- 2.7 consulta
CREATE TABLE consulta (
    id_consulta          SERIAL PRIMARY KEY,
    data_de_atendimento  DATE NOT NULL,
    horario              TIME WITHOUT TIME ZONE,
    motivo               TEXT,
    diagnostico          TEXT,
    observacoes          TEXT,
    id_animal            INTEGER NOT NULL
        REFERENCES animal (id_animal) ON DELETE CASCADE,
    id_veterinario       INTEGER NOT NULL
        REFERENCES veterinario (id_veterinario) ON DELETE CASCADE,
    id_clinica           INTEGER NOT NULL
        REFERENCES clinica (id_clinica) ON DELETE CASCADE
);

-- -----------------------------------------------------------------------------
-- 3. ALTER TABLE
--    Completam as tabelas acima sem alterar as colunas finais (nomes, tipos e
--    ordem continuam exatamente os da especificacao).
-- -----------------------------------------------------------------------------

-- 3.1 FK de cliente -> clinica, com exclusao em cascata
ALTER TABLE cliente
    ADD CONSTRAINT fk_cliente_clinica
    FOREIGN KEY (id_clinica) REFERENCES clinica (id_clinica) ON DELETE CASCADE;

-- 3.2 Todo cliente pertence a uma clinica
ALTER TABLE cliente
    ALTER COLUMN id_clinica SET NOT NULL;

-- 3.3 Regras de dominio (CHECK) adicionadas depois da criacao das tabelas
ALTER TABLE animal
    ADD CONSTRAINT chk_animal_sexo
    CHECK (sexo IN ('M', 'F', 'Macho', 'Fêmea', 'Femea'));

ALTER TABLE animal
    ADD CONSTRAINT chk_animal_peso
    CHECK (peso > 0);

ALTER TABLE animal
    ADD CONSTRAINT chk_animal_nascimento
    CHECK (data_de_nascimento <= CURRENT_DATE);

ALTER TABLE cartao_vacina
    ADD CONSTRAINT chk_vacina_dose
    CHECK (numero_da_dose > 0);

ALTER TABLE cartao_vacina
    ADD CONSTRAINT chk_vacina_proxima_dose
    CHECK (proxima_dose >= data_aplicacao);

-- 3.4 Nome da clinica nao pode ser vazio (NOT NULL ja existe; aqui exigimos texto)
ALTER TABLE clinica
    ADD CONSTRAINT chk_clinica_nome
    CHECK (char_length(trim(nome)) > 0);

-- -----------------------------------------------------------------------------
-- 4. UPDATE condicional com CASE
--    Classifica a situacao de cada dose de vacina que ainda nao tem observacao.
--    Pode ser reexecutado depois de povoamento.sql: so atualiza linhas com
--    observacoes IS NULL e nao faz nada se a tabela estiver vazia.
-- -----------------------------------------------------------------------------
UPDATE cartao_vacina
SET observacoes = CASE
        WHEN proxima_dose IS NULL                        THEN 'Esquema vacinal concluido'
        WHEN proxima_dose <  CURRENT_DATE                THEN 'Dose atrasada - reagendar'
        WHEN proxima_dose <= CURRENT_DATE + INTERVAL '30 days'
                                                         THEN 'Dose proxima - avisar tutor'
        ELSE 'Vacinacao em dia'
    END
WHERE observacoes IS NULL;

COMMIT;
