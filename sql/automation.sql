-- Views
CREATE OR REPLACE VIEW vw_agendamentos_resumo AS
SELECT 
    [link suspeito removido]_agendamento,
    [link suspeito removido]_hora,
    a.status,
    an.nome AS animal,
    v.nome AS veterinario
FROM Agendamentos a
JOIN Animais an ON [link suspeito removido]_animal = [link suspeito removido]_animal
JOIN Veterinarios v ON [link suspeito removido]_veterinario = [link suspeito removido]_veterinario;

CREATE OR REPLACE VIEW vw_prontuario_resumido AS
SELECT 
    id_prontuario,
    id_animal,
    ultima_atualizacao
FROM Prontuario;


-- Função e Trigger para atualizar prontuário ao registrar vacina
CREATE OR REPLACE FUNCTION fn_atualizar_prontuario_vacina()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE Prontuario
    SET ultima_atualizacao = CURRENT_TIMESTAMP,
        historico_medico = CONCAT(historico_medico, ' | Vacina: ', NEW.nome_vacina)
    WHERE id_animal = [link suspeito removido]_animal;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_atualiza_prontuario_vacina
AFTER INSERT ON Vacinas
FOR EACH ROW
EXECUTE FUNCTION fn_atualizar_prontuario_vacina();


-- Perfis e controle de acesso
CREATE ROLE role_atendente;
CREATE ROLE role_veterinario;

GRANT SELECT, INSERT, UPDATE ON Agendamentos TO role_atendente;
GRANT SELECT ON vw_agendamentos_resumo TO role_atendente;

GRANT SELECT, INSERT, UPDATE ON Vacinas TO role_veterinario;
GRANT SELECT, INSERT, UPDATE ON Prontuario TO role_veterinario;
GRANT SELECT ON vw_prontuario_resumido TO role_veterinario;

REVOKE DELETE ON Prontuario FROM role_atendente;
