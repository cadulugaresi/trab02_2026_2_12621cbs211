# Especificação de Requisitos — Gerenciador de Ativos e Vulnerabilidades

**Versão:** 2.0
**Data:** 04/11/2026
**Responsável:** Cadu Lugaresi
**UID:** S2_07 (atualizado na S4_01)

---

## ✨ 1. Objetivo

Especificar os requisitos funcionais e não funcionais do sistema de gerenciamento de ativos de TI e vulnerabilidades associadas, consolidando os artefatos produzidos ao longo das sprints.

## 🫧 2. Escopo

### Dentro do escopo

- Cadastro, consulta, atualização e remoção (CRUD) de ativos de TI de quatro tipos (Notebook, Servidor, Roteador, Impressora);
- Catálogo de vulnerabilidades com nota CVSS e nível de severidade calculado;
- Vínculo entre vulnerabilidades do catálogo e ativos, com status de tratamento por ativo;
- Persistência local em arquivos JSON;
- Interface textual (CLI) com menu interativo;
- Validação de entradas com mensagens seguras;
- Arquitetura em camadas (interface, serviços, persistência e domínio).

### Fora do escopo

- Autenticação de usuários;
- Interface gráfica (GUI) ou web;
- Banco de dados relacional;
- Consulta a bases externas de vulnerabilidades (CVE, NVD);
- Auditoria de alterações (log de quem fez o quê);
- Suporte a múltiplos usuários simultâneos.

## ✨ 3. Atores

- **Analista de segurança:** usuário único do sistema, responsável por manter o inventário.

## 🫧 4. Premissas

- O sistema é **local** (roda na máquina do usuário);
- Não há **autenticação**;
- Os arquivos `ativos.json` (ativos e vínculos) e `vulnerabilidades.json` (catálogo) são o **único** armazenamento;
- O usuário tem **Python 3.8+** instalado.

## ✨ 5. Modelo de Dados

### 5.1. Entidade: Ativo (classe base)

| Campo              | Tipo                      | Obrigatório | Descrição                                                            |
| ------------------ | ------------------------- | ----------- | -------------------------------------------------------------------- |
| `id`               | int                       | Sim         | Identificador único, positivo e imutável                             |
| `nome`             | str                       | Sim         | Nome ou hostname do ativo                                            |
| `setor`            | enum `Setor`              | Sim         | TI, FINANCEIRO, MARKETING, RH, JURIDICO                              |
| `responsavel`      | str                       | Sim         | Nome do responsável                                                  |
| `status`           | enum `StatusDoAtivo`      | Sim         | ATIVO, INATIVO, EM_MANUTENCAO                                        |
| `vulnerabilidades` | dict[int, `StatusDaVuln`] | Não         | Vínculos: ID da vulnerabilidade → status de tratamento. Começa vazio |

O **tipo** do ativo é a própria subclasse. No JSON, ele é gravado no campo `tipo` (ex.: `"Notebook"`).

### 5.2. Subclasses de Ativo

| Subclasse    | Atributos específicos                                  |
| ------------ | ------------------------------------------------------ |
| `Notebook`   | `sistema_operacional` (str), `tela` (float, polegadas) |
| `Servidor`   | `ram` (int, GB), `armazenamento` (float, TB)           |
| `Roteador`   | `portas` (int), `velocidade` (int, MB)                 |
| `Impressora` | `cor` (enum `Cor`), `tecnologia` (enum `Tecnologia`)   |

### 5.3. Entidade: Vulnerabilidade (catálogo)

| Campo                  | Tipo  | Obrigatório | Descrição                                       |
| ---------------------- | ----- | ----------- | ----------------------------------------------- |
| `id_vulnerabilidade`   | int   | Sim         | Gerado automaticamente (maior ID existente + 1) |
| `nome_vulnerabilidade` | str   | Sim         | Descrição da vulnerabilidade                    |
| `cvss`                 | float | Sim         | Nota de 0.1 a 10.0, com uma casa decimal        |

O **nível** (`NivelDaVulnerabilidade`) não é armazenado: é calculado pelo método `nivel()` a partir da nota CVSS.

### 5.4. Enums

- **Setor:** TI, FINANCEIRO, MARKETING, RH, JURIDICO
- **StatusDoAtivo:** ATIVO, INATIVO, EM_MANUTENCAO
- **StatusDaVuln:** ABERTA, EM_TRATAMENTO, CORRIGIDA, ACEITA
- **NivelDaVulnerabilidade:** BAIXO, MEDIO, ALTO, CRITICO
- **Cor:** COLORIDA, PRETA_E_BRANCA
- **Tecnologia:** TINTA, LASER

## 🫧 6. Requisitos Funcionais

| ID    | Descrição                                                                                                       |
| ----- | --------------------------------------------------------------------------------------------------------------- |
| RF-01 | Cadastrar ativos com ID, nome, tipo, setor, responsável, status e atributos específicos do tipo.                |
| RF-02 | Validar entradas: ID único e positivo; campos textuais não vazios nem só números; opções dentro das permitidas. |
| RF-03 | Cadastrar vulnerabilidades no catálogo com nome e nota CVSS, gerando o ID automaticamente.                      |
| RF-04 | Listar todos os ativos ou filtrar por tipo ou por status.                                                       |
| RF-05 | Buscar ativos por ID ou por nome (parcial, case-insensitive).                                                   |
| RF-06 | Atualizar responsável, status, setor, atributos específicos ou tipo de um ativo existente.                      |
| RF-07 | Remover ativo por ID, com confirmação, apagando seus vínculos.                                                  |
| RF-08 | Persistir dados em `ativos.json` e `vulnerabilidades.json` e recarregar na inicialização.                       |
| RF-09 | Vincular uma vulnerabilidade do catálogo a um ativo, com status de tratamento.                                  |
| RF-10 | Listar o catálogo e as vulnerabilidades de um ativo, com o status de cada uma nele.                             |
| RF-11 | Atualizar o status de tratamento de uma vulnerabilidade em um ativo, ou desvinculá-la.                          |
| RF-12 | Editar nome ou CVSS de uma vulnerabilidade do catálogo, ou excluí-la com confirmação.                           |

## ✨ 7. Requisitos Não Funcionais

| ID     | Categoria        | Descrição                                                                                             |
| ------ | ---------------- | ----------------------------------------------------------------------------------------------------- |
| RNF-01 | Usabilidade      | Menu textual com opções numeradas para todas as operações.                                            |
| RNF-02 | Confiabilidade   | Tratar entradas inválidas sem encerrar o programa.                                                    |
| RNF-03 | Segurança        | Não expor detalhes internos em mensagens de erro; tratar Ctrl+C/Ctrl+D de forma limpa, sem traceback. |
| RNF-04 | Manutenibilidade | Código organizado em camadas; o domínio não depende de nenhuma outra camada.                          |
| RNF-05 | Testabilidade    | Regras de negócio sem `input`/`print`, testadas com arquivos temporários.                             |

## 🫧 8. Regras de Negócio

| ID    | Descrição                                                                                                  | Requisitos relacionados |
| ----- | ---------------------------------------------------------------------------------------------------------- | ----------------------- |
| RN-01 | O ID de um ativo é único e imutável após o cadastro.                                                       | RF-01, RF-02            |
| RN-02 | Um ativo não pode ser cadastrado sem nome, responsável, tipo, setor e status válidos.                      | RF-01, RF-02            |
| RN-03 | Ao remover um ativo, seus vínculos são removidos junto; as vulnerabilidades continuam no catálogo.         | RF-07                   |
| RN-04 | A nota CVSS fica entre 0.1 e 10.0 e é arredondada para uma casa decimal antes de ser validada.             | RF-03, RF-12            |
| RN-05 | O nível é derivado do CVSS: até 3.9 Baixo, de 4.0 a 6.9 Médio, de 7.0 a 8.9 Alto, a partir de 9.0 Crítico. | RF-03, RF-10            |
| RN-06 | Uma vulnerabilidade não pode ser vinculada duas vezes ao mesmo ativo.                                      | RF-09                   |
| RN-07 | Ao excluir uma vulnerabilidade do catálogo, ela é desvinculada de todos os ativos.                         | RF-12                   |
| RN-08 | Ao trocar o tipo de um ativo, seus vínculos com vulnerabilidades são mantidos.                             | RF-06                   |
| RN-09 | O ID de uma nova vulnerabilidade é o maior ID existente + 1; IDs excluídos não são reaproveitados.         | RF-03                   |

## ✨ 9. Arquitetura

O sistema é organizado em quatro camadas, cada uma em um pacote de `inventario/`. As dependências só apontam para baixo: interface → serviços → persistência, e todas podem usar o domínio. O diagrama completo está no `README.md`.

### 9.1. Domínio (`inventario/dominio/`)

- Classes: `Ativo`, `Notebook`, `Servidor`, `Roteador`, `Impressora`, `Vulnerabilidade` (com `para_dicionario()` e `de_dicionario()`)
- Enums: `Setor`, `StatusDoAtivo`, `StatusDaVuln`, `NivelDaVulnerabilidade`, `Cor`, `Tecnologia`
- Exceção: `DadoInvalidoError`
- Regras de validação: `validar_nome_responsavel(nome)`, `validar_cvss(cvss)`

### 9.2. Serviços (`inventario/servicos/`)

- Ativos: `registrar_ativo_no_inventario`, `atualizar_ativo_no_inventario`, `remover_ativo_do_inventario`, `obter_ativo`, `encontrar_ativo_por_id`, `encontrar_ativos_por_nome`, `encontrar_ativos_por_status`, `encontrar_ativos_por_tipo`
- Vulnerabilidades: `registrar_vulnerabilidade_no_catalogo`, `atualizar_vulnerabilidade_no_catalogo`, `excluir_vulnerabilidade_do_catalogo`, `vincular_vulnerabilidade`, `desvincular_vulnerabilidade`, `atualizar_status_vulnerabilidade`, `proximo_id`

### 9.3. Persistência (`inventario/persistencia/`)

- `salvar_dados(ativos)`, `carregar_dados()`, `salvar_catalogo(catalogo)`, `carregar_catalogo()`

### 9.4. Interface (`inventario/interface/`)

- Menus: `menu_principal`, `menu_listagem`, `menu_vulnerabilidades`
- Telas: `cadastrar_ativo`, `editar_ativo`, `excluir_ativo`, `perguntar_ativo`, `cadastrar_vulnerabilidade`, `editar_vulnerabilidade`, `vincular_a_um_ativo`, `mostrar_vulnerabilidade`, entre outras
- Entradas: `pedir_info`, `pedir_int`, `pedir_float`, `pedir_cvss`, `pedir_tipo`, `pedir_setor`, `pedir_status`, `pedir_status_vulnerabilidade`, `pedir_cor`, `pedir_tecnologia`
- Conversões do menu: `validar_tipo`, `validar_setor`, `validar_status`, `validar_status_vulnerabilidade`, `validar_cor`, `validar_tecnologia`

## 🫧 10. Restrições

- Linguagem: Python 3.8+;
- Biblioteca padrão apenas (`json`, `enum`);
- Execução local, sem rede;
- Persistência em dois arquivos JSON (`ativos.json` e `vulnerabilidades.json`).

## ✨ 11. Matriz de Validações (Resumo)

Matriz completa em `docs/validacoes.md`.

| Campo              | Regra                     | Mensagem                                                                                                                 |
| ------------------ | ------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| ID                 | Inteiro > 0, único        | "Este campo não pode ser nulo ou negativo. Tente novamente." / "Já existe um ativo cadastrado com este ID. Tente outro." |
| Nome / responsável | Não vazio, não só números | "Este campo não pode ser vazio." / "Este campo não pode ser composto apenas por números."                                |
| Tipo               | Opção do menu             | "Tipo inválido. Tente novamente."                                                                                        |
| Setor              | Opção do menu             | "Setor inválido. Tente novamente."                                                                                       |
| Status             | Opção do menu             | "Status inválido. Tente novamente."                                                                                      |
| CVSS               | De 0.1 a 10.0             | "O CVSS deve estar entre 0.1 e 10."                                                                                      |

## 🫧 12. Critérios de Aceitação (Resumo)

Critérios completos em `docs/criterios_aceitacao.md`.

21 cenários Dado–Quando–Então cobrindo o CRUD de ativos e as operações de vulnerabilidades (sucesso, erro e borda).

## ✨ 13. Rastreabilidade

| História                | Requisitos          | Regras                     | Cenários            | Testes                                                                         |
| ----------------------- | ------------------- | -------------------------- | ------------------- | ------------------------------------------------------------------------------ |
| HU-01 (Cadastrar ativo) | RF-01, RF-02        | RN-01, RN-02               | CA-01 a CA-04       | `TestCadastrarAtivo`, `TestValidarNomeResponsavel`                             |
| HU-02 (Consultar ativo) | RF-04, RF-05        | —                          | CA-05 a CA-08       | `TestEncontrarAtivoPorId`, `TestEncontrarAtivosPorNome`                        |
| HU-03 (Atualizar ativo) | RF-06               | RN-02, RN-08               | CA-09 a CA-11       | `TestEditarAtivo`, `TestAtualizarAtivoNoInventario`                            |
| HU-04 (Remover ativo)   | RF-07               | RN-03                      | CA-12 a CA-15       | `TestExcluirAtivo`, `TestRemoverAtivoDoInventario`                             |
| HU-05 (Catálogo)        | RF-03, RF-10, RF-12 | RN-04, RN-05, RN-07, RN-09 | CA-16, CA-17, CA-21 | `TestCadastrarVulnerabilidade`, `TestValidarCvss`, `TestEditarVulnerabilidade` |
| HU-06 (Vínculos)        | RF-09, RF-11        | RN-06                      | CA-18 a CA-20       | `TestVincularVulnerabilidade`, `TestDesvincularVulnerabilidade`                |

## 🫧 14. Controle de Versão

| Versão | Data       | Autor         | Mudanças                                                                                                           |
| ------ | ---------- | ------------- | ------------------------------------------------------------------------------------------------------------------ |
| 1.0    | 24/09/2026 | Cadu Lugaresi | Versão inicial consolidada                                                                                         |
| 2.0    | 04/11/2026 | Cadu Lugaresi | Subclasses de ativo, catálogo de vulnerabilidades com CVSS, vínculos, novos RF/RN e arquitetura em camadas (S4_01) |

## ✨ 15. Documentos Relacionados

- `docs/requisitos.md` — requisitos detalhados (S2_04)
- `docs/validacoes.md` — matriz de validações (S2_05)
- `docs/criterios_aceitacao.md` — cenários Dado–Quando–Então (S2_06)
- `docs/especificacao.md` — **este documento** (S2_07)
- `docs/relatorio_testes.md` — relatório de testes (S2_18)
- `tests/` — testes automatizados
- `README.md` / `docs/README.pt-br.md` — visão geral do projeto e arquitetura
