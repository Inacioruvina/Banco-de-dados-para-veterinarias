# Dicionário de Dados - Sistema Veterinário

## 1. Tabela: `Clinicas`
Armazena as informações das unidades e filiais da clínica veterinária.

| Coluna | Tipo de Dado | Nulo? | Chave | Descrição |
| :--- | :--- | :--- | :--- | :--- |
| `id_clinica` | `INTEGER` | NÃO | **PK** | Identificador único da clínica |
| `nome` | `VARCHAR(100)` | NÃO | - | Nome fantasia da clínica |
| `endereco` | `VARCHAR(200)` | NÃO | - | Endereço completo (Rua, Número, Bairro, Cidade) |
| `telefone` | `VARCHAR(20)` | SIM | - | Telefone principal de contato |

---

## 2. Tabela: `Clientes`
Armazena os dados cadastrais dos tutores dos animais.

| Coluna | Tipo de Dado | Nulo? | Chave | Descrição |
| :--- | :--- | :--- | :--- | :--- |
| `id_cliente` | `INTEGER` | NÃO | **PK** | Identificador único do cliente |
| `nome` | `VARCHAR(100)` | NÃO | - | Nome completo do cliente/tutor |
| `telefone` | `VARCHAR(20)` | NÃO | - | Telefone de contato do cliente |
| `email` | `VARCHAR(100)` | SIM | - | Endereço de e-mail do cliente |

---

## 3. Tabela: `Animais`
Armazena os dados dos animais atendidos nas clínicas.

| Coluna | Tipo de Dado | Nulo? | Chave | Descrição |
| :--- | :--- | :--- | :--- | :--- |
| `id_animal` | `INTEGER` | NÃO | **PK** | Identificador único do animal |
| `nome` | `VARCHAR(50)` | NÃO | - | Nome do animal |
| `especie` | `VARCHAR(30)` | NÃO | - | Espécie do animal (ex: Cão, Gato) |
| `raca` | `VARCHAR(30)` | SIM | - | Raça do animal |
| `data_nascimento` | `DATE` | SIM | - | Data de nascimento aproximada do animal |
| `id_cliente` | `INTEGER` | NÃO | **FK** | Referência ao tutor do animal (`Clientes.id_cliente`) |