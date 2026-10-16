# ----------------------------------------------------------------------------------------
# main.py  |  Rotina principal: agendamento, vacina e resumo via view
# Execução:  python src/main.py   OU   cd src && python main.py
# ----------------------------------------------------------------------------------------

import sys
from pathlib import Path

# ── Normalização de imports ────────────────────────────────────────────
_SRC_DIR = str(Path(__file__).resolve().parent)
if _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)

import pyodbc  # noqa: E402
from connection import get_connection  # noqa: E402


def _ler_int(mensagem: str) -> int:
    """Lê um inteiro do teclado com tratamento de ValueError."""
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Entrada invalida! Digite um numero inteiro valido.")


# Exibe o menu de opções no terminal
def menu_principal():
    print("\n--- SISTEMA VETERINÁRIO - AGENDAMENTOS E AUTOMAÇÃO ---")
    print("1. Cadastrar Novo Agendamento")
    print("2. Registrar Aplicação de Vacina")
    print("3. Visualizar Resumo de Agendamentos (View)")
    print("4. Sair")
    return input("Escolha uma opção: ").strip()


# Cadastra agendamento (tabela consulta) usando consultas parametrizadas.
# A clínica é a mesma do veterinário escolhido.
def novo_agendamento(cursor):
    print("\n-- Novo Agendamento --")
    data_atendimento = input("Data (AAAA-MM-DD): ").strip()
    horario = input("Horário (HH:MM): ").strip()
    motivo = input("Motivo da consulta: ").strip()
    id_animal = _ler_int("ID do Animal: ")
    id_veterinario = _ler_int("ID do Veterinário: ")

    sql = """
        INSERT INTO consulta (data_de_atendimento, horario, motivo,
                              id_animal, id_veterinario, id_clinica)
        SELECT ?, ?, ?, ?, v.id_veterinario, v.id_clinica
        FROM veterinario AS v
        WHERE v.id_veterinario = ?
    """
    cursor.execute(sql, (data_atendimento, horario, motivo, id_animal, id_veterinario))
    if cursor.rowcount == 0:
        raise ValueError(f"Veterinário com ID {id_veterinario} não encontrado.")
    print("Agendamento cadastrado com sucesso!")


# Registra a aplicação de vacinas (tabela cartao_vacina)
def registrar_vacina(cursor):
    print("\n-- Aplicação de Vacina --")
    nome_vacina = input("Nome da Vacina: ").strip()
    data_aplicacao = input("Data de Aplicação (AAAA-MM-DD): ").strip()
    numero_da_dose = _ler_int("Número da dose: ")
    proxima_dose = input("Data da Próxima Dose (AAAA-MM-DD, vazio se não houver): ").strip() or None
    id_animal = _ler_int("ID do Animal: ")
    id_veterinario = _ler_int("ID do Veterinário: ")

    sql = """
        INSERT INTO cartao_vacina (nome_vacina, data_aplicacao, numero_da_dose,
                                   proxima_dose, id_animal, id_veterinario)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor.execute(sql, (nome_vacina, data_aplicacao, numero_da_dose,
                         proxima_dose, id_animal, id_veterinario))
    print("Vacina registrada com sucesso!")


# Consulta os agendamentos através da visão criada no banco
def listar_agendamentos(cursor):
    print("\n-- Resumo dos Agendamentos --")
    sql = "SELECT * FROM vw_agendamentos_resumo"
    cursor.execute(sql)
    registros = cursor.fetchall()

    if not registros:
        print("Nenhum agendamento encontrado.")
    else:
        for r in registros:
            print(f"ID: {r[0]} | Data: {r[1]} | Hora: {r[2]} | "
                  f"Motivo: {r[3]} | Animal: {r[4]} | Vet: {r[5]}")


# Conecta ao banco e executa o menu
def main():
    try:
        conn = get_connection()
    except (ConnectionError, ValueError) as erro:
        print(f"Erro ao conectar ao banco de dados: {erro}")
        return

    cursor = conn.cursor()

    try:
        while True:
            opcao = menu_principal()

            if opcao in ('1', '2'):
                try:
                    if opcao == '1':
                        novo_agendamento(cursor)
                    else:
                        registrar_vacina(cursor)
                    conn.commit()
                except (ValueError, pyodbc.Error) as erro:
                    conn.rollback()
                    print(f"Não foi possível concluir a operação: {erro}")
            elif opcao == '3':
                listar_agendamentos(cursor)
            elif opcao == '4':
                print("Saindo do sistema...")
                break
            else:
                print("Opção inválida, tente novamente.")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()
