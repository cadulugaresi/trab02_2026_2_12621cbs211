# Requisitos — Gerenciador de Ativos e Vulnerabilidades

UID: S2_04

## Histórias de Usuário

**HU-01 — Cadastrar ativo:** como analista, quero cadastrar um ativo (ID, nome, categoria, setor, responsável, status) para manter o inventário atualizado.
→ RF-01, RF-02, RN-01, RN-02

**HU-02 — Consultar ativo:** como analista, quero buscar ativos por ID ou por nome para localizá-los rapidamente.
→ RF-05

**HU-03 — Atualizar ativo:** como analista, quero editar responsável, status, setor ou categoria de um ativo para refletir mudanças.
→ RF-06

**HU-04 — Remover ativo:** como analista, quero remover um ativo (com confirmação) para manter a base válida.
→ RF-07, RN-03

## Requisitos Funcionais

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

## Requisitos Não Funcionais

| ID | Categoria | Descrição |
|---|---|---|
| RNF-01 | Usabilidade | Menu textual com opções numeradas para todas as operações. |
| RNF-02 | Confiabilidade | Tratar entradas inválidas (vazias, tipos errados, opções inexistentes) sem encerrar o programa. |
| RNF-03 | Segurança | Não expor detalhes internos em mensagens de erro; tratar Ctrl+C/Ctrl+D de forma limpa, sem traceback. |

## Regras de Negócio

| ID | Descrição | Req. relacionados |
|---|---|---|
| RN-01 | O ID de um ativo é único e imutável após cadastro. | RF-01, RF-02 |
| RN-02 | Um ativo não pode ser cadastrado sem nome, responsável, categoria, setor e status válidos. | RF-01, RF-02 |
| RN-03 | Ao remover um ativo, suas vulnerabilidades são removidas junto. | RF-07 |
| RN-04 | Toda vulnerabilidade deve ter nome, tipo, nível e status. | RF-03 |

## Critérios de Aceitação

| Requisito | Como testar |
|---|---|
| RF-01 | Cadastrar ativo com dados válidos → ele aparece na listagem e persiste após reabrir o programa. |
| RF-02 | Tentar ID duplicado ou campo vazio → sistema exibe erro e pede novamente. |
| RF-03 | Adicionar vulnerabilidade → ela aparece na listagem do ativo e persiste. |
| RF-04 | Listar ativos → todos aparecem com seus dados. |
| RF-05 | Buscar `mac` → retorna ativos com "mac" no nome; buscar ID inexistente → "não encontrado". |
| RF-06 | Editar ativo existente → dados atualizados persistem após reabrir. |
| RF-07 | Remover ativo → ele e suas vulnerabilidades somem da listagem e do arquivo. |
| RF-08 | Reabrir o programa → dados previamente salvos são carregados. |

## Rastreabilidade

| História | Requisitos | Regras |
|---|---|---|
| HU-01 | RF-01, RF-02 | RN-01, RN-02 |
| HU-02 | RF-05 | — |
| HU-03 | RF-06 | RN-02 |
| HU-04 | RF-07 | RN-03 |

## Segurança

- **RNF-03** cobre: mensagens de erro sem vazar detalhes internos; Ctrl+C/Ctrl+D encerram sem traceback.
- Sem dados pessoais sensíveis além de nome do responsável — sem exigência LGPD.
- Sem requisito de auditoria no escopo atual.