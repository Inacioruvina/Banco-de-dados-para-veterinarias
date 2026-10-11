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

# Cadastra agendamento usando consultas parametrizadas
def novo_agendamento(cursor):
    print("\n-- Novo Agendamento --")
    data_hora = input("Data e Hora (AAAA-MM-DD HH:MM): ")
    status = input("Status (ex: Agendado, Cancelado): ")
    id_animal = int(input("ID do Animal: "))
    id_veterinario = int(input("ID do Veterinário: "))

    sql = """
        INSERT INTO Agendamentos (data_hora, status, id_animal, id_veterinario)
        VALUES (?, ?, ?, ?)
    """
    cursor.execute(sql, (data_hora, status, id_animal, id_veterinario))
    print("Agendamento cadastrado com sucesso!")

# Registra a aplicação de vacinas
def registrar_vacina(cursor):
    print("\n-- Aplicação de Vacina --")
    nome_vacina = input("Nome da Vacina: ")
    data_aplicacao = input("Data de Aplicação (AAAA-MM-DD): ")
    proxima_dose = input("Data da Próxima Dose (AAAA-MM-DD): ")
    id_animal = int(input("ID do Animal: "))

    sql = """
        INSERT INTO Vacinas (nome_vacina, data_aplicacao, proxima_dose, id_animal)
        VALUES (?, ?, ?, ?)
    """
    cursor.execute(sql, (nome_vacina, data_aplicacao, proxima_dose, id_animal))
    print("Vacina registrada com sucesso!")

# Consulta os agendamentos através da visão criada no banco
def listar_agendamentos(cursor):
    print("\n-- Resumo dos Agendamentos --")
    sql = "SELECT * FROM vw_agendamentos_resumo"
    cursor.execute(sql)
    registros = cursor.fetchall()

    for r in registros:
        print(f"ID: {r[0]} | Data: {r[1]} | Status: {r[2]} | Animal: {r[3]} | Vet: {r[4]}")

# Conecta ao banco e executa o menu
def main():
    conn = get_connection()
    if not conn:
        print("Erro ao conectar ao banco de dados.")
        return

    cursor = conn.cursor()

    while True:
        opcao = menu_principal()
        
        if opcao == '1':
            novo_agendamento(cursor)
            conn.commit()
        elif opcao == '2':
            registrar_vacina(cursor)
            conn.commit()
        elif opcao == '3':
            listar_agendamentos(cursor)
        elif opcao == '4':
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida, tente novamente.")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
