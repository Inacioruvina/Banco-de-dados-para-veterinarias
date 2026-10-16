from connection import get_connection
import operations


def main():
    conexao = get_connection()

    while True:
        print("\n" + "=" * 30)
        print("<<< MENU >>>")
        print("=" * 30)
        print("[1] Buscar animais por peso")
        print("[2] Listar consultas por veterinario")
        print("[3] Relatorio de consultas por clinica")
        print("[4] Buscar animais vacinados")
        print("[5] Lista unificada de contatos")
        print("[6] Buscar animais por faixa de peso")
        print("[7] Relatorio de peso total por cliente")
        print("[8] Lista de especies distintas atendidas")
        print("[0] Sair")
        print("=" * 30)

        opcao = input("Digite a opcao: ")

        match opcao:
            case "1":
                peso = float(input("Digite o valor do peso minimo: "))
                resultados = operations.buscar_animais_por_peso(conexao, peso)

                if not resultados:
                    print(f"Nenhum animal com peso maior que {peso} kg foi encontrado.")
                else:
                    for linha in resultados:
                        nome, especie, raca, p = linha
                        print(
                            f"Nome: {nome} | Especie: {especie} | "
                            f"Raca: {raca} | Peso: {p}kg"
                        )

            case "2":
                idVeterinario = int(
                    input("Digite o ID do Veterinario que realizou a consulta: ")
                )
                resultados = operations.list_by_vet(conexao, idVeterinario)

                if not resultados:
                    print(f"Veterinario com ID {idVeterinario} nao encontrado.")
                else:
                    for linha in resultados:
                        dataAtendimento, motivoConsulta, diagnostico, nomeAnimal = linha
                        print("-" * 30)
                        print(f"Data de atendimento: {dataAtendimento}")
                        print(f"Motivo da consulta: {motivoConsulta}")
                        print(f"Diagnostico: {diagnostico}")
                        print(f"Nome do animal: {nomeAnimal}")

            case "3":
                resultados = operations.consultas_por_clinica(conexao)

                if not resultados:
                    print("Sem informacoes de clinicas")
                else:
                    for linha in resultados:
                        clId, clNome, totalConsultas = linha
                        print("-" * 30)
                        print(f"Id da clinica: {clId}")
                        print(f"Nome da clinica: {clNome}")
                        print(f"Total de consultas: {totalConsultas}")

            case "4":
                nomeVac = input("Digite o nome da vacina: ")
                resultados = operations.find_vaccined_animals(conexao, nomeVac)

                if not resultados:
                    print("Sem animais com essa vacina")
                else:
                    for linha in resultados:
                        nome, especie = linha
                        print("-" * 30)
                        print(f"Nome do animal: {nome}")
                        print(f"Especie do animal: {especie}")

            case "5":
                resultados = operations.unified_contact_list(conexao)

                if not resultados:
                    print("Sem lista de contatos")
                else:
                    for linha in resultados:
                        nome, telefone = linha
                        print("-" * 30)
                        print(f"Nome: {nome}")
                        print(f"Telefone: {telefone}")

            case "6":
                peso_min = float(input("Digite o peso minimo (kg): "))
                peso_max = float(input("Digite o peso maximo (kg): "))

                resultados = operations.buscar_animais_faixa_peso(
                    conexao, peso_min, peso_max
                )

                if not resultados:
                    print(
                        f"Nenhum animal encontrado na faixa de "
                        f"{peso_min} a {peso_max} kg."
                    )
                else:
                    for linha in resultados:
                        nome, especie, peso = linha
                        print(f"Nome: {nome} | Especie: {especie} | Peso: {peso}kg")

            case "7":
                resultados = operations.peso_total_por_cliente(conexao)

                if not resultados:
                    print("Nenhum registro encontrado.")
                else:
                    for linha in resultados:
                        cliente, peso_total = linha
                        print(
                            f"Cliente: {cliente} | "
                            f"Peso Total Acumulado: {peso_total}kg"
                        )

            case "8":
                resultados = operations.listar_especies_atendidas(conexao)

                if not resultados:
                    print("Nenhuma especie encontrada.")
                else:
                    for linha in resultados:
                        (especie,) = linha
                        print(f"Especie: {especie}")

            case "0":
                print("\nEncerrando o sistema...")
                conexao.close()
                break

            case _:
                print("\nOpcao invalida! Tente novamente")


if __name__ == "__main__":
    main()