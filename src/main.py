import pyodbc
from connection import get_connection

# Exibe o menu de opções no terminal
def menu_principal():
    print("\n--- SISTEMA VETERINÁRIO - AGENDAMENTOS E AUTOMAÇÃO ---")
    print("1. Cadastrar Novo Agendamento")
    print("2. Registrar Aplicação de Vacina")
    print("3. Visualizar Resumo de Agendamentos (View)")
    print("4. Sair")
    return input("Escolha uma opção: ")

# Cadastra agendamento (tabela consulta) usando consultas parametrizadas.
# A clínica é a mesma do veterinário escolhido.
def novo_agendamento(cursor):
    print("\n-- Novo Agendamento --")
    data_atendimento = input("Data (AAAA-MM-DD): ")
    horario = input("Horário (HH:MM): ")
    motivo = input("Motivo da consulta: ")
    id_animal = int(input("ID do Animal: "))
    id_veterinario = int(input("ID do Veterinário: "))

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
    nome_vacina = input("Nome da Vacina: ")
    data_aplicacao = input("Data de Aplicação (AAAA-MM-DD): ")
    numero_da_dose = int(input("Número da dose: "))
    proxima_dose = input("Data da Próxima Dose (AAAA-MM-DD, vazio se não houver): ") or None
    id_animal = int(input("ID do Animal: "))
    id_veterinario = int(input("ID do Veterinário: "))

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

    for r in registros:
        print(f"ID: {r[0]} | Data: {r[1]} | Hora: {r[2]} | Motivo: {r[3]} | Animal: {r[4]} | Vet: {r[5]}")

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
