# Relatório de Casos de Teste e Garantia de Qualidade (QA)

Este documento registra as validações de integridade, restrições (CHECKS, PKs, FKs) e regras de negócio executadas no banco de dados PostgreSQL.

---

## CT-01: Inserção de Animal com Espécie Inválida (Validação de CHECK)
* **Objetivo:** Verificar se a restrição `CHECK` na tabela `Animais` impede o cadastro de espécies não autorizadas (ex: aceitar apenas 'Cão', 'Gato').
* **Comando SQL Executado:**
```sql
INSERT INTO Animais (nome, especie, raca, data_nascimento, id_cliente)
VALUES ('Piu', 'Papagaio', 'Arara', '2023-01-01', 1);
```
* **Resultado Esperado:** O banco de dados deve rejeitar o comando e retornar erro de violação de restrição de verificação (`check constraint violation`).
* **Status:** PASSOU (Erro retornado com sucesso)

---

## CT-02: Cadastro de Animal associado a Cliente Inexistente (Integridade Referencial FK)
* **Objetivo:** Testar se o banco impede o cadastro de um animal vinculado a um `id_cliente` que não existe.
* **Comando SQL Executado:**
```sql
INSERT INTO Animais (nome, especie, raca, data_nascimento, id_cliente)
VALUES ('Rex', 'Cão', 'Labrador', '2022-05-10', 9999);
```
* **Resultado Esperado:** O banco deve bloquear a inserção apontando erro de Chave Estrangeira (`foreign key constraint violation`).
* **Status:** PASSOU (Bloqueio efetuado)

---

## CT-03: Inserção de Consulta com Valor Negativo (Validação de Regra Financeira)
* **Objetivo:** Garantir que o valor cobrado em uma consulta não seja um número negativo.
* **Comando SQL Executado:**
```sql
INSERT INTO Consultas (data_hora, diagnostico, valor, id_animal, id_veterinario, id_clinica)
VALUES (NOW(), 'Exame de rotina', -150.00, 1, 1, 1);
```
* **Resultado Esperado:** O banco de dados deve barrar a operação exibindo erro de violação de regra `CHECK (valor >= 0)`.
* **Status:** PASSOU (Operação barrada)

---

## CT-04: Inserção de Registro Válido (Caminho Feliz / Sucesso)
* **Objetivo:** Confirmar que dados válidos inseridos respeitando todas as regras são gravados corretamente no banco.
* **Comando SQL Executado:**
```sql
INSERT INTO Clientes (nome, telefone, email)
VALUES ('Fernanda Lima', '(63) 99111-2222', 'fernanda.lima@email.com');
```
* **Resultado Esperado:** Registro inserido com sucesso (1 linha afetada).
* **Status:** PASSOU