# Dicionário de Dados - Sistema Veterinário

Reflete exatamente o schema de `sql/ddl_schema.sql` (PostgreSQL, 7 tabelas no singular).
Todas as chaves estrangeiras usam `ON DELETE CASCADE`.

## 1. Tabela: `clinica`
| Coluna | Tipo | Nulo? | Chave | Descrição |
| :--- | :--- | :--- | :--- | :--- |
| `id_clinica` | `SERIAL` | NÃO | **PK** | Identificador da clínica |
| `nome` | `VARCHAR(128)` | NÃO | - | Nome da clínica (não pode ser vazio) |
| `telefone` | `VARCHAR(20)` | SIM | - | Telefone de contato |
| `endereco` | `TEXT` | SIM | - | Endereço completo |

## 2. Tabela: `cliente`
| Coluna | Tipo | Nulo? | Chave | Descrição |
| :--- | :--- | :--- | :--- | :--- |
| `id_cliente` | `SERIAL` | NÃO | **PK** | Identificador do cliente/tutor |
| `nome` | `VARCHAR(128)` | NÃO | - | Nome completo |
| `cpf` | `VARCHAR(14)` | SIM | - | CPF (com ou sem pontuação) |
| `telefone` | `VARCHAR(20)` | SIM | - | Telefone de contato |
| `endereco` | `TEXT` | SIM | - | Endereço |
| `id_clinica` | `INTEGER` | NÃO | **FK** | Clínica do cliente (`clinica.id_clinica`) |

## 3. Tabela: `veterinario`
| Coluna | Tipo | Nulo? | Chave | Descrição |
| :--- | :--- | :--- | :--- | :--- |
| `id_veterinario` | `SERIAL` | NÃO | **PK** | Identificador do veterinário |
| `nome` | `VARCHAR(128)` | NÃO | - | Nome completo |
| `crmv` | `VARCHAR(20)` | SIM | - | Registro profissional |
| `telefone` | `VARCHAR(20)` | SIM | - | Telefone de contato |
| `especialidade` | `VARCHAR(50)` | SIM | - | Especialidade |
| `id_clinica` | `INTEGER` | NÃO | **FK** | Clínica onde atua (`clinica.id_clinica`) |

## 4. Tabela: `animal`
| Coluna | Tipo | Nulo? | Chave | Descrição |
| :--- | :--- | :--- | :--- | :--- |
| `id_animal` | `SERIAL` | NÃO | **PK** | Identificador do animal |
| `nome` | `VARCHAR(128)` | NÃO | - | Nome do animal |
| `especie` | `VARCHAR(50)` | NÃO | - | `CHECK`: Cão, Cao, Gato, Ave, Roedor, Coelho, Réptil, Reptil, Outro |
| `raca` | `VARCHAR(50)` | SIM | - | Raça |
| `sexo` | `VARCHAR(10)` | SIM | - | `CHECK`: M, F, Macho, Fêmea, Femea |
| `data_de_nascimento` | `DATE` | SIM | - | `CHECK`: não pode ser futura |
| `peso` | `NUMERIC(5,2)` | SIM | - | Peso em kg (`CHECK` > 0) |
| `id_cliente` | `INTEGER` | NÃO | **FK** | Tutor (`cliente.id_cliente`) |

## 5. Tabela: `prontuario`
| Coluna | Tipo | Nulo? | Chave | Descrição |
| :--- | :--- | :--- | :--- | :--- |
| `id_prontuario` | `SERIAL` | NÃO | **PK** | Identificador do prontuário |
| `nome` | `VARCHAR(128)` | NÃO | - | Título/identificação do prontuário |
| `historico_saude` | `TEXT` | SIM | - | Histórico de saúde |
| `alergias` | `TEXT` | SIM | - | Alergias conhecidas |
| `observacoes` | `TEXT` | SIM | - | Observações gerais |
| `id_animal` | `INTEGER` | NÃO | **FK** | Animal (`animal.id_animal`) |

## 6. Tabela: `cartao_vacina`
| Coluna | Tipo | Nulo? | Chave | Descrição |
| :--- | :--- | :--- | :--- | :--- |
| `id_vacina` | `SERIAL` | NÃO | **PK** | Identificador do registro de vacina |
| `nome_vacina` | `VARCHAR(100)` | NÃO | - | Nome da vacina |
| `data_aplicacao` | `DATE` | NÃO | - | Data de aplicação |
| `numero_da_dose` | `INTEGER` | SIM | - | Número da dose (`CHECK` > 0) |
| `proxima_dose` | `DATE` | SIM | - | Próxima dose (`CHECK` ≥ `data_aplicacao`) |
| `observacoes` | `TEXT` | SIM | - | Observações |
| `id_animal` | `INTEGER` | NÃO | **FK** | Animal (`animal.id_animal`) |
| `id_veterinario` | `INTEGER` | SIM | **FK** | Veterinário (`veterinario.id_veterinario`) |

## 7. Tabela: `consulta`
| Coluna | Tipo | Nulo? | Chave | Descrição |
| :--- | :--- | :--- | :--- | :--- |
| `id_consulta` | `SERIAL` | NÃO | **PK** | Identificador da consulta |
| `data_de_atendimento` | `DATE` | NÃO | - | Data do atendimento |
| `horario` | `TIME` | SIM | - | Horário (sem fuso) |
| `motivo` | `TEXT` | SIM | - | Motivo da consulta |
| `diagnostico` | `TEXT` | SIM | - | Diagnóstico |
| `observacoes` | `TEXT` | SIM | - | Observações |
| `id_animal` | `INTEGER` | NÃO | **FK** | Animal (`animal.id_animal`) |
| `id_veterinario` | `INTEGER` | NÃO | **FK** | Veterinário (`veterinario.id_veterinario`) |
| `id_clinica` | `INTEGER` | NÃO | **FK** | Clínica (`clinica.id_clinica`) |