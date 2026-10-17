# ----------------------------------------------------------------------------------------
# main.py  |  Sistema Operacional da Rede Veterinária (Atendimento e Cadastros)
# Execução:  python src/main.py   OU   python -m src.main
# ----------------------------------------------------------------------------------------

import sys
from datetime import datetime
from pathlib import Path

# ── Normalização de imports ────────────────────────────────────────────
_SRC_DIR = str(Path(__file__).resolve().parent)
if _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)

import pyodbc  # noqa: E402
from connection import get_connection  # noqa: E402


# ── Utilitários de Validação e Dependências ──────────────────────────────
def _contar_registros(cursor, tabela: str) -> int:
    """Retorna a contagem de registros em uma tabela para validação de dependências."""
    tabelas_validas = {"clinica", "cliente", "veterinario", "animal", "consulta", "cartao_vacina"}
    if tabela not in tabelas_validas:
        raise ValueError(f"Tabela inválida: {tabela}")
    cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
    return cursor.fetchone()[0]


def _ler_int_faixa(mensagem: str, min_val: int, max_val: int) -> int:
    """Lê um inteiro dentro de uma faixa especificada."""
    while True:
        try:
            val = int(input(mensagem).strip())
            if min_val <= val <= max_val:
                return val
            print(f"Opção inválida! Escolha um número entre {min_val} e {max_val}.")
        except ValueError:
            print("Entrada inválida! Digite um número inteiro.")


def _ler_float(mensagem: str, minimo: float = 0.01) -> float:
    """Lê um valor decimal positivo do teclado."""
    while True:
        try:
            val = float(input(mensagem).strip().replace(",", "."))
            if val >= minimo:
                return val
            print(f"O valor deve ser maior ou igual a {minimo}.")
        except ValueError:
            print("Entrada inválida! Digite um número válido (ex: 12.5).")


def _ler_data(mensagem: str, permite_vazio: bool = False, no_futuro: bool = False) -> str | None:
    """Valida e lê datas no formato AAAA-MM-DD."""
    while True:
        entrada = input(mensagem).strip()
        if permite_vazio and not entrada:
            return None
        try:
            dt = datetime.strptime(entrada, "%Y-%m-%d").date()
            if not no_futuro and dt > datetime.now().date():
                print("A data não pode ser superior à data de hoje.")
                continue
            return entrada
        except ValueError:
            print("Formato inválido! Utilize o padrão AAAA-MM-DD (ex: 2025-05-20).")


def _ler_horario(mensagem: str) -> str:
    """Valida e lê horários no formato HH:MM."""
    while True:
        entrada = input(mensagem).strip()
        try:
            datetime.strptime(entrada, "%H:%M")
            return entrada
        except ValueError:
            print("Formato inválido! Utilize o padrão HH:MM (ex: 14:30).")


# ── Seleção e Busca por Nome (UX do Atendente) ───────────────────────────
def selecionar_clinica(cursor) -> tuple[int | None, str | None]:
    """Lista as clínicas cadastradas para vinculação ou permite cadastrar uma nova."""
    while True:
        cursor.execute("SELECT id_clinica, nome, endereco FROM clinica ORDER BY id_clinica")
        clinicas = cursor.fetchall()
        if not clinicas:
            print("\n[Aviso] Nenhuma clínica cadastrada no banco de dados.")
            cadastrar = input("Deseja cadastrar uma clínica agora? (s/n): ").strip().lower()
            if cadastrar == "s":
                novo_id, nome = cadastrar_clinica(cursor)
                if novo_id:
                    return novo_id, nome
            return None, None

        print("\n--- Clínicas Cadastradas ---")
        for idx, (id_c, nome, end) in enumerate(clinicas, 1):
            print(f"  [{idx}] {nome} ({end or 'Sem endereço informado'})")
        print(f"  [{len(clinicas) + 1}] + Cadastrar Nova Clínica")
        print("  [0] Cancelar")

        escolha = _ler_int_faixa("Escolha a clínica: ", 0, len(clinicas) + 1)
        if escolha == 0:
            return None, None
        if escolha == len(clinicas) + 1:
            novo_id, nome = cadastrar_clinica(cursor)
            if novo_id:
                return novo_id, nome
            continue

        id_c, nome, _ = clinicas[escolha - 1]
        return id_c, nome


def selecionar_ou_buscar_cliente(cursor) -> tuple[int | None, str | None]:
    """Busca tutor/cliente pelo nome ou CPF."""
    while True:
        termo = input("\nNome ou CPF do Tutor/Cliente (ou '0' para cancelar): ").strip()
        if termo == "0":
            return None, None
        if not termo:
            print("Digite um nome ou CPF para pesquisar.")
            continue

        sql = """
            SELECT id_cliente, nome, cpf, telefone
            FROM cliente
            WHERE nome ILIKE ? OR cpf ILIKE ?
            ORDER BY nome
        """
        cursor.execute(sql, (f"%{termo}%", f"%{termo}%"))
        clientes = cursor.fetchall()

        if not clientes:
            print(f"Nenhum tutor encontrado com '{termo}'.")
            cadastrar = input("Deseja cadastrar esse novo tutor agora? (s/n): ").strip().lower()
            if cadastrar == "s":
                novo_id = cadastrar_cliente(cursor, nome_sugerido=termo)
                if novo_id:
                    return novo_id, termo
            continue

        if len(clientes) == 1:
            id_c, nome, cpf, tel = clientes[0]
            print(f"-> Tutor selecionado: {nome} (CPF: {cpf or 'N/A'}, Tel: {tel or 'N/A'})")
            return id_c, nome

        print(f"\nForam encontrados {len(clientes)} tutores:")
        for idx, (id_c, nome, cpf, tel) in enumerate(clientes, 1):
            print(f"  [{idx}] {nome} | CPF: {cpf or 'N/A'} | Tel: {tel or 'N/A'}")
        print("  [0] Fazer outra busca")

        escolha = _ler_int_faixa("Selecione o número correspondente: ", 0, len(clientes))
        if escolha == 0:
            continue
        id_c, nome, _, _ = clientes[escolha - 1]
        return id_c, nome


def selecionar_ou_buscar_animal(cursor) -> tuple[int | None, str | None]:
    """Busca animal pelo nome, exibindo dados de raça e tutor para desambiguação."""
    while True:
        termo = input("\nNome do Animal (ou '0' para cancelar): ").strip()
        if termo == "0":
            return None, None
        if not termo:
            print("Digite o nome do animal para buscar.")
            continue

        sql = """
            SELECT a.id_animal, a.nome, a.especie, a.raca, c.nome AS tutor
            FROM animal a
            JOIN cliente c ON a.id_cliente = c.id_cliente
            WHERE a.nome ILIKE ?
            ORDER BY a.nome
        """
        cursor.execute(sql, (f"%{termo}%",))
        animais = cursor.fetchall()

        if not animais:
            print(f"Nenhum animal cadastrado com o nome '{termo}'.")
            cadastrar = input("Deseja cadastrar esse novo animal agora? (s/n): ").strip().lower()
            if cadastrar == "s":
                novo_id = cadastrar_animal(cursor, nome_sugerido=termo)
                if novo_id:
                    return novo_id, termo
            continue

        if len(animais) == 1:
            id_a, nome, esp, raca, tutor = animais[0]
            print(f"-> Animal selecionado: {nome} ({esp} - {raca}) | Tutor: {tutor}")
            return id_a, nome

        print(f"\nForam encontrados {len(animais)} animais com esse nome:")
        for idx, (id_a, nome, esp, raca, tutor) in enumerate(animais, 1):
            print(f"  [{idx}] {nome} ({esp} - {raca}) | Tutor: {tutor}")
        print("  [0] Fazer outra busca")

        escolha = _ler_int_faixa("Selecione o animal correspondente: ", 0, len(animais))
        if escolha == 0:
            continue
        id_a, nome, _, _, _ = animais[escolha - 1]
        return id_a, nome


def selecionar_veterinario(cursor) -> tuple[int | None, int | None, str | None]:
    """Lista os veterinários cadastrados e retorna (id_veterinario, id_clinica, nome_vet)."""
    cursor.execute("""
        SELECT v.id_veterinario, v.nome, v.especialidade, c.nome AS clinica, v.id_clinica
        FROM veterinario v
        JOIN clinica c ON v.id_clinica = c.id_clinica
        ORDER BY v.nome
    """)
    vets = cursor.fetchall()
    if not vets:
        print("\n[Aviso] Nenhum funcionário/veterinário cadastrado no sistema.")
        cadastrar = input("Deseja cadastrar um veterinário agora? (s/n): ").strip().lower()
        if cadastrar == "s":
            novo_id, id_clinica, nome = cadastrar_veterinario(cursor)
            return novo_id, id_clinica, nome
        return None, None, None

    print("\n--- Selecione o Veterinário Responsável ---")
    for idx, (id_v, nome, esp, clinica, id_c) in enumerate(vets, 1):
        print(f"  [{idx}] {nome} ({esp}) | Clínica: {clinica}")
    print("  [0] Cancelar")

    escolha = _ler_int_faixa("Escolha o número do veterinário: ", 0, len(vets))
    if escolha == 0:
        return None, None, None
    id_v, nome, _, _, id_c = vets[escolha - 1]
    return id_v, id_c, nome


# ── Operações de Cadastro (DML com Validação de Dependências) ────────────
def cadastrar_clinica(cursor) -> tuple[int | None, str | None]:
    """Cadastra uma nova clínica veterinária na rede."""
    print("\n-- Cadastro de Nova Clínica Veterinária --")
    nome = input("Nome da Clínica (ex: Clínica Veterinária Central): ").strip()
    while not nome:
        nome = input("O nome da clínica é obrigatório. Digite o nome: ").strip()

    telefone = input("Telefone de contato (ex: (63) 3000-0000): ").strip() or None
    endereco = input("Endereço completo (Rua, Número, Bairro): ").strip() or None

    sql = """
        INSERT INTO clinica (nome, telefone, endereco)
        VALUES (?, ?, ?)
        RETURNING id_clinica
    """
    cursor.execute(sql, (nome, telefone, endereco))
    id_novo = cursor.fetchone()[0]
    print(f"\nClínica '{nome}' cadastrada com sucesso (ID: {id_novo})!")
    return id_novo, nome


def cadastrar_cliente(cursor, nome_sugerido: str = "") -> int | None:
    """Cadastra um novo tutor/cliente associado a uma clínica."""
    print("\n-- Cadastro de Novo Tutor (Cliente) --")

    # Dependência: precisa ter ao menos uma clínica cadastrada
    if _contar_registros(cursor, "clinica") == 0:
        print("\n[Dependência não atendida] Não é possível cadastrar um cliente sem uma clínica cadastrada no sistema.")
        cadastrar = input("Deseja cadastrar uma clínica agora? (s/n): ").strip().lower()
        if cadastrar == "s":
            id_clinica, _ = cadastrar_clinica(cursor)
            if not id_clinica:
                return None
        else:
            print("Operação cancelada. Cadastre uma clínica primeiro (Opção 7).")
            return None

    if nome_sugerido:
        nome = input(f"Nome completo [{nome_sugerido}]: ").strip() or nome_sugerido
    else:
        nome = input("Nome completo: ").strip()
        while not nome:
            nome = input("Nome é obrigatório. Digite o nome: ").strip()

    cpf = input("CPF (ex: 000.000.000-00): ").strip() or None
    telefone = input("Telefone de contato: ").strip() or None
    endereco = input("Endereço: ").strip() or None

    id_clinica, nome_clinica = selecionar_clinica(cursor)
    if not id_clinica:
        print("Cadastro de tutor cancelado.")
        return None

    sql = """
        INSERT INTO cliente (nome, cpf, telefone, endereco, id_clinica)
        VALUES (?, ?, ?, ?, ?)
        RETURNING id_cliente
    """
    cursor.execute(sql, (nome, cpf, telefone, endereco, id_clinica))
    id_novo = cursor.fetchone()[0]
    print(f"\nTutor '{nome}' cadastrado com sucesso (ID: {id_novo}) na {nome_clinica}!")
    return id_novo


def cadastrar_veterinario(cursor) -> tuple[int | None, int | None, str | None]:
    """Cadastra um novo funcionário veterinário no sistema."""
    print("\n-- Cadastro de Funcionário / Veterinário --")

    # Dependência: precisa ter ao menos uma clínica cadastrada
    if _contar_registros(cursor, "clinica") == 0:
        print("\n[Dependência não atendida] Não é possível cadastrar um veterinário sem uma clínica cadastrada no sistema.")
        cadastrar = input("Deseja cadastrar uma clínica agora? (s/n): ").strip().lower()
        if cadastrar == "s":
            id_clinica, nome_clinica = cadastrar_clinica(cursor)
            if not id_clinica:
                return None, None, None
        else:
            print("Operação cancelada. Cadastre uma clínica primeiro (Opção 7).")
            return None, None, None

    nome = input("Nome completo (ex: Dr. Carlos Silva): ").strip()
    while not nome:
        nome = input("Nome é obrigatório: ").strip()

    crmv = input("CRMV (ex: CRMV-00 1234): ").strip() or None
    telefone = input("Telefone de contato: ").strip() or None
    especialidade = input("Especialidade (ex: Clínica Geral, Cirurgia, Felinos): ").strip() or "Clínica Geral"

    id_clinica, nome_clinica = selecionar_clinica(cursor)
    if not id_clinica:
        print("Cadastro cancelado.")
        return None, None, None

    sql = """
        INSERT INTO veterinario (nome, crmv, telefone, especialidade, id_clinica)
        VALUES (?, ?, ?, ?, ?)
        RETURNING id_veterinario
    """
    cursor.execute(sql, (nome, crmv, telefone, especialidade, id_clinica))
    id_novo = cursor.fetchone()[0]
    print(f"\nVeterinário '{nome}' cadastrado com sucesso na {nome_clinica}!")
    return id_novo, id_clinica, nome


def cadastrar_animal(cursor, nome_sugerido: str = "") -> int | None:
    """Cadastra um novo animal vinculado a um tutor e inicializa seu prontuário."""
    print("\n-- Cadastro de Novo Animal (Pet) --")

    # Dependência: não é possível cadastrar um animal sem cliente (tutor) cadastrado
    if _contar_registros(cursor, "cliente") == 0:
        print("\n[Dependência não atendida] Não é possível cadastrar um animal sem um cliente (tutor) cadastrado.")
        cadastrar = input("Deseja cadastrar um novo tutor agora? (s/n): ").strip().lower()
        if cadastrar == "s":
            id_cliente = cadastrar_cliente(cursor)
            if not id_cliente:
                print("Cadastro do animal cancelado.")
                return None
        else:
            print("Operação cancelada. Cadastre um cliente primeiro (Opção 6).")
            return None

    if nome_sugerido:
        nome = input(f"Nome do Pet [{nome_sugerido}]: ").strip() or nome_sugerido
    else:
        nome = input("Nome do Pet: ").strip()
        while not nome:
            nome = input("Nome é obrigatório: ").strip()

    print("\nIdentificação do Tutor (Cliente):")
    id_cliente, nome_tutor = selecionar_ou_buscar_cliente(cursor)
    if not id_cliente:
        print("Cadastro do animal cancelado (é necessário vincular a um tutor).")
        return None

    # Espécies aceitas pela constraint CHECK do banco
    especies = ["Cão", "Gato", "Ave", "Roedor", "Coelho", "Réptil", "Outro"]
    print("\nEscolha a Espécie:")
    for idx, esp in enumerate(especies, 1):
        print(f"  [{idx}] {esp}")
    idx_esp = _ler_int_faixa("Opção de espécie: ", 1, len(especies))
    especie = especies[idx_esp - 1]

    raca = input("Raça (ex: Vira-lata, Labrador, Siamês): ").strip() or "SRD"

    print("\nSexo do Animal:")
    print("  [1] Fêmea (F)")
    print("  [2] Macho (M)")
    sexo = "F" if _ler_int_faixa("Opção de sexo: ", 1, 2) == 1 else "M"

    data_nasc = _ler_data("Data de Nascimento (AAAA-MM-DD, vazio se desconhecido): ", permite_vazio=True)
    peso = _ler_float("Peso em kg (ex: 8.5): ", minimo=0.01)

    sql_animal = """
        INSERT INTO animal (nome, especie, raca, sexo, data_de_nascimento, peso, id_cliente)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        RETURNING id_animal
    """
    cursor.execute(sql_animal, (nome, especie, raca, sexo, data_nasc, peso, id_cliente))
    id_animal = cursor.fetchone()[0]

    # Cria prontuário inicial automaticamente para o animal
    sql_prontuario = """
        INSERT INTO prontuario (nome, historico_saude, observacoes, id_animal)
        VALUES (?, 'Prontuário aberto no cadastro.', 'Primeiro registro.', ?)
    """
    cursor.execute(sql_prontuario, (f"Prontuário {nome}", id_animal))

    print(f"\nPet '{nome}' ({especie} - {raca}) cadastrado com sucesso com seu prontuário inicial!")
    return id_animal


# ── Atendimento: Agendamento e Vacinação (Com Validação de Dependências) ──
def novo_agendamento(cursor):
    """Cadastra um novo agendamento de consulta ligando nomes de animal e veterinário."""
    print("\n-- Novo Agendamento de Consulta --")

    # Dependência 1: não deve ser possível cadastrar consulta sem animais
    if _contar_registros(cursor, "animal") == 0:
        print("\n[Dependência não atendida] Não é possível cadastrar uma consulta sem animais cadastrados no sistema.")
        print("Cadastre primeiro um animal (Opção 4).")
        return

    # Dependência 2: não deve ser possível cadastrar consulta sem veterinário
    if _contar_registros(cursor, "veterinario") == 0:
        print("\n[Dependência não atendida] Não é possível cadastrar uma consulta sem um funcionário/veterinário cadastrado.")
        print("Cadastre primeiro um veterinário (Opção 5).")
        return

    id_animal, nome_animal = selecionar_ou_buscar_animal(cursor)
    if not id_animal:
        print("Agendamento cancelado.")
        return

    id_veterinario, id_clinica, nome_vet = selecionar_veterinario(cursor)
    if not id_veterinario:
        print("Agendamento cancelado (é obrigatório selecionar um veterinário).")
        return

    data_atendimento = _ler_data("Data do Atendimento (AAAA-MM-DD): ", no_futuro=True)
    horario = _ler_horario("Horário da Consulta (HH:MM): ")
    motivo = input("Motivo da consulta (ex: Check-up, Vacinação, Coceira): ").strip() or "Consulta Geral"

    sql = """
        INSERT INTO consulta (data_de_atendimento, horario, motivo,
                              id_animal, id_veterinario, id_clinica)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor.execute(sql, (data_atendimento, horario, motivo, id_animal, id_veterinario, id_clinica))
    print(f"\nConsulta para '{nome_animal}' agendada com sucesso com {nome_vet} em {data_atendimento} às {horario}!")


def registrar_vacina(cursor):
    """Registra aplicação de vacina ligando animal e veterinário por nome."""
    print("\n-- Aplicação de Vacina --")

    # Dependência 1: precisa de animais cadastrados
    if _contar_registros(cursor, "animal") == 0:
        print("\n[Dependência não atendida] Não é possível registrar vacinação sem animais cadastrados no sistema.")
        print("Cadastre primeiro um animal (Opção 4).")
        return

    # Dependência 2: não deve ser possível registrar vacina sem um veterinário
    if _contar_registros(cursor, "veterinario") == 0:
        print("\n[Dependência não atendida] Não é possível registrar uma vacina sem um funcionário/veterinário cadastrado.")
        print("Cadastre primeiro um veterinário (Opção 5).")
        return

    id_animal, nome_animal = selecionar_ou_buscar_animal(cursor)
    if not id_animal:
        print("Operação cancelada.")
        return

    id_veterinario, _, nome_vet = selecionar_veterinario(cursor)
    if not id_veterinario:
        print("Operação cancelada (é obrigatório indicar o veterinário aplicador).")
        return

    nome_vacina = input("Nome da Vacina (ex: Antirrábica, V10, V4): ").strip()
    while not nome_vacina:
        nome_vacina = input("Nome da vacina é obrigatório: ").strip()

    data_aplicacao = _ler_data("Data de Aplicação (AAAA-MM-DD) [Hoje se vazio]: ", permite_vazio=True)
    if not data_aplicacao:
        data_aplicacao = datetime.now().strftime("%Y-%m-%d")

    numero_da_dose = _ler_int_faixa("Número da dose (ex: 1, 2, 3): ", 1, 20)
    proxima_dose = _ler_data(
        "Data da Próxima Dose (AAAA-MM-DD, vazio se não houver): ",
        permite_vazio=True,
        no_futuro=True,
    )
    observacoes = input("Observações (opcional): ").strip() or None

    sql = """
        INSERT INTO cartao_vacina (nome_vacina, data_aplicacao, numero_da_dose,
                                   proxima_dose, observacoes, id_animal, id_veterinario)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(sql, (nome_vacina, data_aplicacao, numero_da_dose,
                         proxima_dose, observacoes, id_animal, id_veterinario))
    print(f"\nVacina '{nome_vacina}' (Dose {numero_da_dose}) aplicada em '{nome_animal}' por {nome_vet} registrada com sucesso!")
    print("O prontuário do animal foi atualizado automaticamente via Trigger do banco!")


def listar_agendamentos(cursor):
    """Consulta os agendamentos através da view 'vw_agendamentos_resumo' com validação prévia."""
    # Dependência: não deve ser possível visualizar o resumo de atendimentos sem ter atendimentos
    if _contar_registros(cursor, "consulta") == 0:
        print("\n" + "=" * 70)
        print("       [DEPENDÊNCIA NÃO ATENDIDA] RESUMO DE ATENDIMENTOS        ")
        print("=" * 70)
        print("Não é possível visualizar o resumo porque ainda não há nenhum")
        print("atendimento/consulta cadastrado no sistema.")
        print("Cadastre ao menos um agendamento de consulta (Opção 1) antes de visualizar.")
        print("=" * 70)
        return

    print("\n" + "=" * 70)
    print("               RESUMO DOS AGENDAMENTOS (VIEW)              ")
    print("=" * 70)
    sql = """
        SELECT id_consulta, data_de_atendimento, horario, motivo, animal, veterinario
        FROM vw_agendamentos_resumo
        ORDER BY data_de_atendimento DESC, horario DESC
    """
    cursor.execute(sql)
    registros = cursor.fetchall()

    for r in registros:
        hora_str = str(r[2])[:5] if r[2] else "--:--"
        print(f"ID #{r[0]} | {r[1]} às {hora_str} | Pet: {r[4]:<12} | Vet: {r[5]:<20} | Motivo: {r[3]}")
    print("=" * 70)


# ── Menu Principal e Loop da Aplicação ───────────────────────────────────
def menu_principal() -> str:
    print("\n" + "=" * 55)
    print("   SISTEMA VETERINÁRIO - GESTÃO E ATENDIMENTO CLÍNICO   ")
    print("=" * 55)
    print(" [1] Cadastrar Novo Agendamento (Consulta)")
    print(" [2] Registrar Aplicação de Vacina")
    print(" [3] Visualizar Resumo de Agendamentos (View)")
    print(" [4] Cadastrar Novo Animal (Pet)")
    print(" [5] Cadastrar Funcionário / Veterinário")
    print(" [6] Cadastrar Novo Tutor (Cliente)")
    print(" [7] Cadastrar Nova Clínica")
    print(" [0] Sair")
    print("=" * 55)
    return input("Escolha uma opção: ").strip()


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

            if opcao in ("1", "2", "4", "5", "6", "7"):
                try:
                    if opcao == "1":
                        novo_agendamento(cursor)
                    elif opcao == "2":
                        registrar_vacina(cursor)
                    elif opcao == "4":
                        cadastrar_animal(cursor)
                    elif opcao == "5":
                        cadastrar_veterinario(cursor)
                    elif opcao == "6":
                        cadastrar_cliente(cursor)
                    elif opcao == "7":
                        cadastrar_clinica(cursor)
                    conn.commit()
                except (ValueError, pyodbc.Error) as erro:
                    conn.rollback()
                    print(f"\nNão foi possível concluir a operação: {erro}")
            elif opcao == "3":
                listar_agendamentos(cursor)
            elif opcao in ("0", "sair", "exit"):
                print("\nEncerrando o sistema...")
                break
            else:
                print("Opção inválida! Tente novamente.")
    except (KeyboardInterrupt, EOFError):
        print("\n\nOperação interrompida pelo usuário. Encerrando...")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()
