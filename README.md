# Sistema de Gestão de Clínica Veterinária 🐾

Sistema desenvolvido para gerenciamento de clínicas veterinárias, clientes, animais, consultas, agendamentos, vacinas e prontuários médicos, com backend em Python e banco de dados PostgreSQL via ODBC[cite: 1, 3, 5].

---

##  Equipe do Projeto

* **Integrante 1:** Infraestrutura, Esquema DDL (Tabelas Base) e Conexão Python ODBC (`sql/ddl_schema.sql`, `src/connection.py`)[cite: 1, 3]
* **Integrante 2:** Módulo Clínico, Consultas SQL e Relatórios (`sql/queries.sql`, `src/reports.py`, `src/operations.py`)[cite: 1, 4]
* **Integrante 3:** Automação, Segurança e Interface Principal (`sql/automation.sql`, `src/main.py`)[cite: 1, 5]
* **Integrante 4:** Povoamento de Dados, Garantia de Qualidade (QA) e Documentação (`sql/povoamento.sql`, `docs/`)

---

## Tecnologias Utilizadas

* **Linguagem Backend:** Python 3.10+ (Execução nativa de rotinas e relatórios)[cite: 1, 13]
* **Driver de Conexão:** `pyodbc` / `psqlODBC` (PostgreSQL Unicode)[cite: 1, 3, 13]
* **Banco de Dados:** PostgreSQL (DDL, DQL, PL/pgSQL com Views, Functions e Triggers)[cite: 1, 3, 5]
* **Documentação & Modelagem:** Markdown, Mermaid (Diagrama ER) e Relatório de QA[cite: 6]

---

##  Como Executar

Requisitos: Python 3.10+, PostgreSQL e o driver ODBC `psqlODBC` (PostgreSQL Unicode)[cite: 13].

```bash
pip install -r requirements.txt
copy .env.example .env        # preencha DB_PORT, DB_DATABASE, DB_USER e DB_PASSWORD

psql -U postgres -c "CREATE DATABASE veterinaria_db"
psql -U postgres -d veterinaria_db -f sql/ddl_schema.sql    # Estrutura do banco
psql -U postgres -d veterinaria_db -f sql/povoamento.sql    # Dados de teste
psql -U postgres -d veterinaria_db -f sql/automation.sql    # Views, trigger e perfis

python -m src.main       # agendamentos e vacinas (execute da raiz do projeto)
python -m src.reports    # relatórios (execute da raiz do projeto)
python -m unittest tests.test_connection