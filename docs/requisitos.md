# Requisitos — Gerenciador de Ativos e Vulnerabilidades

UID: S2_04 (atualizado na S4_01)

## ✨ Histórias de Usuário

**HU-01 — Cadastrar ativo:** como analista, quero cadastrar um ativo (ID, nome, tipo, setor, responsável, status e atributos do tipo) para manter o inventário atualizado.
→ RF-01, RF-02, RN-01, RN-02

**HU-02 — Consultar ativo:** como analista, quero listar os ativos, filtrá-los por tipo ou status e buscá-los por ID ou por nome para localizá-los rapidamente.
→ RF-04, RF-05

**HU-03 — Atualizar ativo:** como analista, quero editar responsável, status, setor, atributos específicos ou tipo de um ativo para refletir mudanças.
→ RF-06, RN-08

**HU-04 — Remover ativo:** como analista, quero remover um ativo (com confirmação) para manter a base válida.
→ RF-07, RN-03

**HU-05 — Manter o catálogo de vulnerabilidades:** como analista, quero cadastrar, editar e excluir vulnerabilidades com nota CVSS para ter uma base única e consistente.
→ RF-03, RF-10, RF-12, RN-04, RN-05, RN-07, RN-09

**HU-06 — Vincular vulnerabilidades a ativos:** como analista, quero vincular vulnerabilidades a ativos e acompanhar o status de tratamento em cada um.
→ RF-09, RF-11, RN-06

## 🫧 Requisitos Funcionais

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

## ✨ Requisitos Não Funcionais

| ID     | Categoria        | Descrição                                                                                             |
| ------ | ---------------- | ----------------------------------------------------------------------------------------------------- |
| RNF-01 | Usabilidade      | Menu textual com opções numeradas para todas as operações.                                            |
| RNF-02 | Confiabilidade   | Tratar entradas inválidas (vazias, tipos errados, opções inexistentes) sem encerrar o programa.       |
| RNF-03 | Segurança        | Não expor detalhes internos em mensagens de erro; tratar Ctrl+C/Ctrl+D de forma limpa, sem traceback. |
| RNF-04 | Manutenibilidade | Código organizado em camadas; o domínio não depende de nenhuma outra camada.                          |
| RNF-05 | Testabilidade    | Regras de negócio sem `input`/`print`, testadas com arquivos temporários.                             |

## 🫧 Regras de Negócio

| ID    | Descrição                                                                                                  | Req. relacionados |
| ----- | ---------------------------------------------------------------------------------------------------------- | ----------------- |
| RN-01 | O ID de um ativo é único e imutável após cadastro.                                                         | RF-01, RF-02      |
| RN-02 | Um ativo não pode ser cadastrado sem nome, responsável, tipo, setor e status válidos.                      | RF-01, RF-02      |
| RN-03 | Ao remover um ativo, seus vínculos são removidos junto; as vulnerabilidades continuam no catálogo.         | RF-07             |
| RN-04 | A nota CVSS fica entre 0.1 e 10.0 e é arredondada para uma casa decimal antes de ser validada.             | RF-03, RF-12      |
| RN-05 | O nível é derivado do CVSS: até 3.9 Baixo, de 4.0 a 6.9 Médio, de 7.0 a 8.9 Alto, a partir de 9.0 Crítico. | RF-03, RF-10      |
| RN-06 | Uma vulnerabilidade não pode ser vinculada duas vezes ao mesmo ativo.                                      | RF-09             |
| RN-07 | Ao excluir uma vulnerabilidade do catálogo, ela é desvinculada de todos os ativos.                         | RF-12             |
| RN-08 | Ao trocar o tipo de um ativo, seus vínculos com vulnerabilidades são mantidos.                             | RF-06             |
| RN-09 | O ID de uma nova vulnerabilidade é o maior ID existente + 1; IDs excluídos não são reaproveitados.         | RF-03             |

## ✨ Critérios de Aceitação

| Requisito | Como testar                                                                                             |
| --------- | ------------------------------------------------------------------------------------------------------- |
| RF-01     | Cadastrar ativo com dados válidos → ele aparece na listagem e persiste após reabrir o programa.         |
| RF-02     | Tentar ID duplicado ou campo vazio → sistema exibe erro e pede novamente.                               |
| RF-03     | Cadastrar vulnerabilidade com CVSS válido → ela aparece no catálogo com ID e nível corretos.            |
| RF-04     | Listar todos, ou filtrar por tipo/status → aparecem só os ativos correspondentes.                       |
| RF-05     | Buscar `mac` → retorna ativos com "mac" no nome; buscar ID inexistente → "Nenhum ativo encontrado."     |
| RF-06     | Editar ativo existente e escolher "Voltar" → dados atualizados persistem após reabrir.                  |
| RF-07     | Remover ativo → ele e seus vínculos somem da listagem e do arquivo; o catálogo não muda.                |
| RF-08     | Reabrir o programa → ativos, vínculos e catálogo previamente salvos são carregados.                     |
| RF-09     | Vincular vulnerabilidade a um ativo → ela aparece nas vulnerabilidades do ativo com o status escolhido. |
| RF-10     | Listar vulnerabilidades de um ativo → cada uma aparece com o status de tratamento naquele ativo.        |
| RF-11     | Atualizar status ou desvincular → a mudança aparece só naquele ativo e persiste.                        |
| RF-12     | Excluir vulnerabilidade do catálogo → ela some do catálogo e de todos os ativos vinculados.             |

## 🫧 Rastreabilidade

| História | Requisitos          | Regras                     |
| -------- | ------------------- | -------------------------- |
| HU-01    | RF-01, RF-02        | RN-01, RN-02               |
| HU-02    | RF-04, RF-05        | —                          |
| HU-03    | RF-06               | RN-02, RN-08               |
| HU-04    | RF-07               | RN-03                      |
| HU-05    | RF-03, RF-10, RF-12 | RN-04, RN-05, RN-07, RN-09 |
| HU-06    | RF-09, RF-11        | RN-06                      |

## ✨ Segurança

- **RNF-03** cobre: mensagens de erro sem vazar detalhes internos; Ctrl+C/Ctrl+D encerram sem traceback.
- Sem dados pessoais sensíveis além de nome do responsável — sem exigência LGPD.
- Sem requisito de auditoria no escopo atual.
