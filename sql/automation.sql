-- =============================================================================
-- automation.sql  |  Views, funcao + trigger e perfis de acesso
-- Execute DEPOIS de ddl_schema.sql (e, de preferencia, de povoamento.sql).
-- Reexecutavel: remove os objetos antes de recria-los.
--
-- Mapeamento para o schema de 7 tabelas:
--   "agendamento" -> tabela consulta
--   "vacina"      -> tabela cartao_vacina
--   "prontuario"  -> tabela prontuario (historico_saude)
-- =============================================================================

-- ---------------------------------------------------------------------------
-- Views
-- ---------------------------------------------------------------------------
DROP VIEW IF EXISTS vw_agendamentos_resumo;
CREATE VIEW vw_agendamentos_resumo AS
SELECT
    c.id_consulta,
    c.data_de_atendimento,
    c.horario,
    c.motivo,
    an.nome AS animal,
    v.nome  AS veterinario
FROM consulta c
JOIN animal      an ON c.id_animal      = an.id_animal
JOIN veterinario v  ON c.id_veterinario = v.id_veterinario;

DROP VIEW IF EXISTS vw_prontuario_resumido;
CREATE VIEW vw_prontuario_resumido AS
SELECT
    p.id_prontuario,
    p.id_animal,
    p.nome
FROM prontuario p;


-- ---------------------------------------------------------------------------
-- Funcao e trigger: ao registrar uma vacina, anexa-a ao historico do prontuario
-- ---------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION fn_atualizar_prontuario_vacina()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE prontuario
    SET historico_saude = CONCAT_WS(' | ', historico_saude, 'Vacina: ' || NEW.nome_vacina)
    WHERE id_animal = NEW.id_animal;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_atualiza_prontuario_vacina ON cartao_vacina;
CREATE TRIGGER trg_atualiza_prontuario_vacina
AFTER INSERT ON cartao_vacina
FOR EACH ROW
EXECUTE FUNCTION fn_atualizar_prontuario_vacina();


-- ---------------------------------------------------------------------------
-- Perfis e controle de acesso
-- ---------------------------------------------------------------------------
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'role_atendente') THEN
        CREATE ROLE role_atendente;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'role_veterinario') THEN
        CREATE ROLE role_veterinario;
    END IF;
END
$$;

GRANT SELECT, INSERT, UPDATE ON consulta TO role_atendente;
GRANT SELECT ON vw_agendamentos_resumo TO role_atendente;

GRANT SELECT, INSERT, UPDATE ON cartao_vacina TO role_veterinario;
GRANT SELECT, INSERT, UPDATE ON prontuario    TO role_veterinario;
GRANT SELECT ON vw_prontuario_resumido TO role_veterinario;

REVOKE DELETE ON prontuario FROM role_atendente;
