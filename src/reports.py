#----------------------------------------------------------------------------------------
# Código INÁCIO

from connection import get_connection
import operations

def main ():
    
    conexao = get_connection()
    
    while True:
        print("\n" + "="*30)
        print("      < < < MENU > > >")
        print("="*30)
        print("[1] Buscar animais por peso")
        print("[2] Listar consultas por veterinario")
        print("[3] Relatorio de consultas por clinica")
        print("[4] Buscar animais vacinados")
        print("[5] Lista unificada de contatos")
        print("[0] Sair")
        print("="*30)
        
        opcao = input("Digita a opcao: ")
        
        match opcao:
            
            case "1":
                
                peso = float(input("Digite o valor do peso minimo: "))
                
                resultados = operations.search_by_weight(conexao, peso)
                
                if not resultados:
                    
                    print(f"Nem um animal com peso maior de {peso} kg foi encontrado.")
                    
                else:
                    
                    for linha in resultados:
                        nome, especie, raca, p = linha
                        print(f"Nome:{nome} | Especie: {especie} | Raca: {raca} | Peso: {p}kg")
            case "2":
                
                idVeterinario = int(input("Digite o ID do Veterinario que realizou a consulta: "))
                
                resultados = operations.list_by_vet(conexao, idVeterinario)
                
                if not resultados:
                    
                    print(f"Veterinario com ID {idVeterinario} nao encontrado.")
                    
                else: 
                    
                    for linha in resultados:
                        dataAtendimento, motivoConsulta, diagnostico, nomeAnimal = linha
                        print("-"*30)
                        print(f"Data de atendimento: {dataAtendimento}")
                        print(f"Motivo da consulta: {motivoConsulta}")
                        print(f"Diagnostico: {diagnostico}")
                        print(f"Nome do animal: {nomeAnimal}")
                
            case "3":
                
                pass
                
            case "4":
            
                pass
                
            case "5":
            
                pass
        
            case "  0":
                
                print("\nEncerrando o sistema...")
                conexao.close()
                break
            
            case _:
                print("\nOpcao invalida! Tente novamente")
                

if __name__ == "__main__":
    main()
    
    
#----------------------------------------------------------------------------------------