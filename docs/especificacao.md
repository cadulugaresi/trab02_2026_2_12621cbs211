# Especificação de Requisitos — Gerenciador de Ativos e Vulnerabilidades

**Versão:** 1.0
**Data:** 24/09/2026
**Responsável:** Cadu Lugaresi
**UID:** S2_07

---

## 1. Objetivo

Especificar os requisitos funcionais e não funcionais do sistema de gerenciamento de ativos de TI e vulnerabilidades associadas, consolidando os artefatos produzidos ao longo da sprint S2.

## 2. Escopo

### Dentro do escopo

- Cadastro, consulta, atualização e remoção (CRUD) de ativos de TI;
- Cadastro, listagem e remoção de vulnerabilidades associadas a ativos;
- Persistência local em arquivo JSON;
- Interface textual (CLI) com menu interativo;
- Validação de entradas com mensagens seguras.

### Fora do escopo

- Autenticação de usuários;
- Interface gráfica (GUI) ou web;
- Banco de dados relacional;
- Consulta a bases externas de vulnerabilidades (CVE, NVD);
- Auditoria de alterações (log de quem fez o quê);
- Suporte a múltiplos usuários simultâneos.

## 3. Atores

- **Analista de segurança:** usuário único do sistema, responsável por manter o inventário.

## 4. Premissas

- O sistema é **local** (roda na máquina do usuário);
- Não há **autenticação**;
- O arquivo `ativos.json` é o **único** armazenamento;
- O usuário tem **Python 3.8+** instalado.

## 5. Modelo de Dados

### 5.1. Entidade: Ativo

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `id` | int | Sim | Identificador único, positivo e imutável |
| `nome` | str | Sim | Nome ou hostname do ativo |
| `categoria` | enum `Categorias` | Sim | NOTEBOOK, SERVIDOR, ROTEADOR, IMPRESSORA |
| `setor` | enum `Setor` | Sim | TI, FINANCEIRO, MARKETING, RH, JURIDICO |
| `responsavel` | str | Sim | Nome do responsável |
| `status` | enum `StatusDoAtivo` | Sim | ATIVO, INATIVO, EM_MANUTENCAO |
| `vulnerabilidades` | list[Vulnerabilidade] | Não | Lista inicial vazia |

### 5.2. Entidade: Vulnerabilidade

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `nome_vulnerabilidade` | str | Sim | Descrição da vulnerabilidade |
| `tipo` | str | Sim | Tipo/categoria da vulnerabilidade (texto livre) |
| `nivel` | enum `NivelDaVulnerabilidade` | Sim | BAIXO, MEDIO, ALTO |
| `status_tratamento` | enum `StatusDaVuln` | Sim | ABERTA, EM_TRATAMENTO, CORRIGIDA, ACEITA |

### 5.3. Enums

- **Categorias:** NOTEBOOK, SERVIDOR, ROTEADOR, IMPRESSORA
- **Setor:** TI, FINANCEIRO, MARKETING, RH, JURIDICO
- **StatusDoAtivo:** ATIVO, INATIVO, EM_MANUTENCAO
- **NivelDaVulnerabilidade:** BAIXO, MEDIO, ALTO
- **StatusDaVuln:** ABERTA, EM_TRATAMENTO, CORRIGIDA, ACEITA

## 6. Requisitos Funcionais

| ID | Descrição |
|---|---|
| RF-01 | Cadastrar ativos com ID, nome, categoria, setor, responsável e status. |
| RF-02 | Validar entradas: ID único e positivo; campos textuais não vazios nem só números. |
| RF-03 | Associar vulnerabilidades a ativos com nome, tipo, nível e status de tratamento. |
| RF-04 | Listar todos os ativos e suas vulnerabilidades. |
| RF-05 | Buscar ativos por ID ou por nome (parcial, case-insensitive). |
| RF-06 | Atualizar responsável, status, setor ou categoria de um ativo existente. |
| RF-07 | Remover ativo por ID, com confirmação, apagando suas vulnerabilidades. |
| RF-08 | Persistir dados em `ativos.json` e recarregar na inicialização. |

## 7. Requisitos Não Funcionais

| ID | Categoria | Descrição |
|---|---|---|
| RNF-01 | Usabilidade | Menu textual com opções numeradas para todas as operações. |
| RNF-02 | Confiabilidade | Tratar entradas inválidas sem encerrar o programa. |
| RNF-03 | Segurança | Não expor detalhes internos em mensagens de erro; tratar Ctrl+C/Ctrl+D de forma limpa, sem traceback. |

## 8. Regras de Negócio

| ID | Descrição | Requisitos relacionados |
|---|---|---|
| RN-01 | O ID de um ativo é único e imutável após o cadastro. | RF-01, RF-02 |
| RN-02 | Um ativo não pode ser cadastrado sem nome, responsável, categoria, setor e status válidos. | RF-01, RF-02 |
| RN-03 | Ao remover um ativo, suas vulnerabilidades são removidas junto. | RF-07 |
| RN-04 | Toda vulnerabilidade deve ter nome, tipo, nível e status. | RF-03 |

## 9. Funções e Classes

### 9.1. Classes

- `Ativo` — com `para_dicionario()`
- `Vulnerabilidade` — com `para_dicionario()`
- Enums: `Categorias`, `Setor`, `StatusDoAtivo`, `NivelDaVulnerabilidade`, `StatusDaVuln`
- Exceção: `DadoInvalidoError`

### 9.2. Funções de validação

- `validar_nome_responsavel(nome)`
- `validar_status(digitado)`
- `validar_setor(digitado)`
- `validar_categoria(digitado)`

### 9.3. Funções de I/O

- `pedir_id(mensagem)`
- `pedir_info(mensagem)`
- `pedir_status(mensagem)`
- `pedir_setor(mensagem)`
- `pedir_categoria(mensagem)`

### 9.4. Funções de busca

- `encontrar_ativo_por_id(ID, ativos)`
- `encontrar_ativo_por_nome(nome, ativos)`

### 9.5. Funções de exibição

- `Ativo.exibir_detalhes()`
- `mostrar_vulnerabilidade(vulnerabilidade)`

### 9.6. Funções de persistência

- `salvar_dados(ativos)`
- `carregar_dados()`

## 10. Restrições

- Linguagem: Python 3.8+;
- Biblioteca padrão apenas (`json`, `enum`);
- Execução local, sem rede;
- Arquivo único de persistência (`ativos.json`).

## 11. Matriz de Validações (Resumo)

Matriz completa em `docs/validacoes.md`.

| Campo | Regra | Mensagem |
|---|---|---|
| ID | Inteiro > 0, único | "O ID não pode ser nulo ou negativo." / "Já existe um ativo com este ID." |
| Nome | Não vazio, não só números | "Este campo não pode ser vazio." / "Este campo não pode ser composto apenas por números." |
| Categoria | Valor de enum | "Dado inválido. Tente novamente." |
| Setor | Valor de enum | "Setor inválido. Tente novamente." |
| Status | Valor de enum | "Status inválido. Tente novamente." |

## 12. Critérios de Aceitação (Resumo)

Critérios completos em `docs/criterios_aceitacao.md`.

15 cenários Dado–Quando–Então cobrindo CRUD (sucesso, erro e borda).

## 13. Rastreabilidade

| História | Requisitos | Regras | Cenários | Testes |
|---|---|---|---|---|
| HU-01 (Cadastrar) | RF-01, RF-02 | RN-01, RN-02 | CA-01 a CA-04 | `TestAtivo`, `TestValidacoes` |
| HU-02 (Consultar) | RF-04 | — | CA-05 a CA-08 | `TestBusca` |
| HU-03 (Atualizar) | RF-06 | RN-02 | CA-09 a CA-11 | — |
| HU-04 (Remover) | RF-07 | RN-03 | CA-12 a CA-15 | — |

## 14. Controle de Versão

| Versão | Data | Autor | Mudanças |
|---|---|---|---|
| 1.0 | 24/09/2026 | Cadu Lugaresi | Versão inicial consolidada |

## 15. Documentos Relacionados

- `docs/requisitos.md` — requisitos detalhados (S2_04)
- `docs/validacoes.md` — matriz de validações (S2_05)
- `docs/criterios_aceitacao.md` — cenários Dado–Quando–Então (S2_06)
- `docs/especificacao.md` — **este documento** (S2_07)
- `testes.py` — testes automatizados (S2_02 e S2_05)
- `README.md` / `README.pt-br.md` — visão geral do projeto