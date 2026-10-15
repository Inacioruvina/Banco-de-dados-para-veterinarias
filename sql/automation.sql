-- Views
CREATE OR REPLACE VIEW vw_agendamentos_resumo AS
SELECT 
    a.id_agendamento,
    a.data_hora,
    a.status,
    an.nome AS animal,
    v.nome AS veterinario
FROM agendamento a
JOIN animal an ON a.id_animal = an.id_animal
JOIN veterinario v ON a.id_veterinario = v.id_veterinario;

CREATE OR REPLACE VIEW vw_prontuario_resumido AS
SELECT 
    id_prontuario,
    id_animal,
    ultima_atualizacao
FROM prontuario;


-- Função e Trigger para atualizar prontuário ao registrar vacina
CREATE OR REPLACE FUNCTION fn_atualizar_prontuario_vacina()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE prontuario
    SET ultima_atualizacao = CURRENT_TIMESTAMP,
        historico_medico = CONCAT(historico_medico, ' | Vacina: ', NEW.nome_vacina)
    WHERE id_animal = NEW.id_animal;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_atualiza_prontuario_vacina
AFTER INSERT ON cartao_vacina
FOR EACH ROW
EXECUTE FUNCTION fn_atualizar_prontuario_vacina();


-- Perfis e controle de acesso
CREATE ROLE role_atendente;
CREATE ROLE role_veterinario;

GRANT SELECT, INSERT, UPDATE ON agendamento TO role_atendente;
GRANT SELECT ON vw_agendamento_resumo TO role_atendente;

GRANT SELECT, INSERT, UPDATE ON cartao_vacina TO role_veterinario;
GRANT SELECT, INSERT, UPDATE ON prontuario TO role_veterinario;
GRANT SELECT ON vw_prontuario_resumido TO role_veterinario;

REVOKE DELETE ON prontuario FROM role_atendente;
