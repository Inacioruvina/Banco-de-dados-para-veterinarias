# Banco-de-dados-para-veterinarias
O projeto está sendo desenvolvido com objetivo avaliativo na matéria de banco de dados do curso de Ciência da Computação da UFT lecionado pelo professor Ary Henrique, desenvolvido pelos alunos Inácio Ruvina, Arthur Sidarta, Bruno Alef e Eduardo Cunha

## Como executar

Requisitos: Python 3.10+, PostgreSQL e o driver ODBC `psqlODBC` (PostgreSQL Unicode).

```powershell
pip install -r requirements.txt
copy .env.example .env        # preencha DB_PORT, DB_DATABASE, DB_USER e DB_PASSWORD

psql -U postgres -c "CREATE DATABASE veterinaria"
psql -U postgres -d veterinaria -f sql/ddl_schema.sql     # 7 tabelas
psql -U postgres -d veterinaria -f sql/povoamento.sql     # dados de teste
psql -U postgres -d veterinaria -f sql/automation.sql     # views, trigger e perfis

python src/main.py       # agendamentos e vacinas
python src/reports.py    # relatórios
python -m unittest tests.test_connection
```

Tabelas: `clinica`, `cliente`, `veterinario`, `animal`, `prontuario`, `cartao_vacina`, `consulta`
(detalhes em `docs/dicionario_de_dados.md` e `docs/diagrama_er.md`).
