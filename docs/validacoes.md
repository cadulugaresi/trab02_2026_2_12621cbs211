# Validações e Matriz de Regras

UID: S2_05

Matriz campo × regra × mensagem de erro para as entradas do sistema.

## Matriz de Validação

| Campo | Tipo | Regra | Mensagem de erro |
|---|---|---|---|
| ID do ativo | int | Não vazio | "Este campo não pode ser vazio. Tente novamente." |
| ID do ativo | int | Maior que zero | "O ID não pode ser nulo ou negativo. Tente novamente." |
| ID do ativo | int | Único (não pode existir) | "Já existe um ativo cadastrado com este ID. Tente outro." |
| ID do ativo | int | Formato numérico | "Digite um número válido." |
| Nome do ativo | str | Não vazio | "Este campo não pode ser vazio." |
| Nome do ativo | str | Não só números | "Este campo não pode ser composto apenas por números." |
| Responsável | str | Não vazio | "Este campo não pode ser vazio." |
| Responsável | str | Não só números | "Este campo não pode ser composto apenas por números." |
| Categoria | Enum | Um dos valores: NOTEBOOK, SERVIDOR, ROTEADOR, IMPRESSORA | "Dado inválido. Tente novamente." |
| Setor | Enum | Um dos valores: TI, FINANCEIRO, MARKETING, RH, JURIDICO | "Setor inválido. Tente novamente." |
| Status do ativo | Enum | Um dos valores: ATIVO, INATIVO, EM_MANUTENCAO | "Status inválido. Tente novamente." |
| Nome da vulnerabilidade | str | Não vazio | "Vulnerabilidade não pode ser vazia. Tente novamente." |
| Tipo da vulnerabilidade | str | Não vazio | "Este campo não pode ser vazio." |
| Nível da vulnerabilidade | Enum | Um dos valores: BAIXO, MEDIO, ALTO | "Nível inválido. Tente novamente." |
| Status de tratamento | Enum | Um dos valores: ABERTA, EM_TRATAMENTO, CORRIGIDA, ACEITA | "Status inválido. Tente novamente." |

## Funções Validadoras

| Função | O que valida | Onde é usada |
|---|---|---|
| `validar_nome_responsavel(nome)` | Não vazio, não só números | `pedir_info` |
| `validar_status(digitado)` | Status do ativo é um dos permitidos | `pedir_status` |
| `validar_setor(digitado)` | Setor é um dos permitidos | `pedir_setor` |
| `validar_categoria(digitado)` | Categoria é uma das permitidas | `pedir_categoria` |
| `pedir_id` (validação interna) | ID é numérico, positivo e não vazio | Vários |
| `pedir_id_disponivel` | ID não está em uso | `cadastrar_ativo` |

## Tipos de Validação Aplicados

- **Presença:** campos obrigatórios não podem ser vazios
- **Tipo:** ID deve ser conversível pra `int`; demais campos são `str` ou `Enum`
- **Formato:** nome e responsável não podem ser só números
- **Domínio:** enums só aceitam valores predefinidos
- **Faixa:** ID deve ser maior que zero

## Estratégia de Tratamento de Erro

- Cada validação levanta `DadoInvalidoError` (exceção customizada);
- A camada de I/O (`pedir_*`) captura a exceção, exibe a mensagem e pede novamente;
- O programa **não encerra** por erro de entrada — o usuário pode tentar de novo;
- Mensagens **não expõem** stack trace nem detalhes internos;
- **Ctrl+C** e **Ctrl+D** são tratados no `main` (encerram limpo).

## Valores de Fronteira Testados

| Campo | Valor de fronteira | Comportamento esperado |
|---|---|---|
| ID | 0 | Rejeitado ("não pode ser nulo ou negativo") |
| ID | -1 | Rejeitado |
| ID | 1 | Aceito (menor ID válido) |
| ID | "abc" | Rejeitado ("Digite um número válido") |
| ID | "" (vazio) | Rejeitado ("não pode ser vazio") |
| Nome | "" (vazio) | Rejeitado |
| Nome | "123" | Rejeitado ("só números") |
| Nome | "cadu" | Aceito |
| Categoria | "5" | Rejeitado (não existe) |
| Categoria | "1" | Aceito (NOTEBOOK) |