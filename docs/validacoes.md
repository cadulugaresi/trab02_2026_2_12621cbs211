# Validações e Matriz de Regras

UID: S2_05 (atualizado na S4_01)

Matriz campo × regra × mensagem de erro para as entradas do sistema.

## ✨ Matriz de Validação

### Ativos

| Campo                   | Tipo   | Regra                                                 | Mensagem de erro                                             |
| ----------------------- | ------ | ----------------------------------------------------- | ------------------------------------------------------------ |
| ID do ativo             | int    | Não vazio                                             | "Este campo não pode ser vazio. Tente novamente."            |
| ID do ativo             | int    | Maior que zero                                        | "Este campo não pode ser nulo ou negativo. Tente novamente." |
| ID do ativo             | int    | Único (não pode existir)                              | "Já existe um ativo cadastrado com este ID. Tente outro."    |
| ID do ativo             | int    | Formato numérico                                      | "Digite um número válido"                                    |
| Nome do ativo           | str    | Não vazio                                             | "Este campo não pode ser vazio."                             |
| Nome do ativo           | str    | Não só números                                        | "Este campo não pode ser composto apenas por números."       |
| Responsável             | str    | Não vazio                                             | "Este campo não pode ser vazio."                             |
| Responsável             | str    | Não só números                                        | "Este campo não pode ser composto apenas por números."       |
| Tipo                    | Classe | Opção 1 a 4: Notebook, Servidor, Roteador, Impressora | "Tipo inválido. Tente novamente."                            |
| Setor                   | Enum   | Opção 1 a 5: TI, FINANCEIRO, MARKETING, RH, JURIDICO  | "Setor inválido. Tente novamente."                           |
| Status do ativo         | Enum   | Opção 1 a 3: ATIVO, INATIVO, EM_MANUTENCAO            | "Status inválido. Tente novamente."                          |
| Sistema operacional     | str    | Não vazio, não só números                             | Mesmas mensagens do nome                                     |
| Tela, armazenamento     | float  | Número maior que zero (aceita vírgula)                | "Este campo não pode ser nulo ou negativo. Tente novamente." |
| RAM, portas, velocidade | int    | Número inteiro maior que zero                         | "Este campo não pode ser nulo ou negativo. Tente novamente." |
| Cor                     | Enum   | Opção 1 ou 2: COLORIDA, PRETA_E_BRANCA                | "Cor inválida. Tente novamente."                             |
| Tecnologia              | Enum   | Opção 1 ou 2: TINTA, LASER                            | "Tecnologia inválida. Tente novamente."                      |

### Vulnerabilidades

| Campo                   | Tipo  | Regra                                                     | Mensagem de erro                                                             |
| ----------------------- | ----- | --------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Nome da vulnerabilidade | str   | Não vazio, não só números                                 | Mesmas mensagens do nome do ativo                                            |
| CVSS                    | float | De 0.1 a 10.0, arredondado para uma casa antes de validar | "O CVSS deve estar entre 0.1 e 10."                                          |
| Status de tratamento    | Enum  | Opção 1 a 4: ABERTA, EM_TRATAMENTO, CORRIGIDA, ACEITA     | "Status inválido. Tente novamente."                                          |
| Vínculo                 | —     | A vulnerabilidade deve existir no catálogo                | "Vulnerabilidade não encontrada no catálogo."                                |
| Vínculo                 | —     | Não pode vincular duas vezes ao mesmo ativo               | "Esta vulnerabilidade já está vinculada a este ativo."                       |
| Desvínculo              | —     | A vulnerabilidade deve estar vinculada ao ativo           | "Esta vulnerabilidade não está vinculada a este ativo."                      |
| Atualização de status   | —     | A vulnerabilidade deve estar vinculada ao ativo           | "Este ativo não possui nenhuma vulnerabilidade com este ID vinculada a ele." |
| Ativo informado         | —     | O ativo deve existir                                      | "Ativo não encontrado."                                                      |

## 🫧 Funções Validadoras

| Função                                                                                                                   | O que valida                                                     | Camada    | Onde é usada                                                                                                 |
| ------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------- | --------- | ------------------------------------------------------------------------------------------------------------ |
| `validar_texto_obrigatorio(texto)`                                                                                       | Não vazio, não só números                                        | Domínio   | `pedir_info`                                                                                                 |
| `validar_cvss(cvss)`                                                                                                     | Faixa de 0.1 a 10.0 e arredondamento                             | Domínio   | `pedir_cvss`, `registrar_vulnerabilidade_no_catalogo`, `atualizar_vulnerabilidade_no_catalogo`               |
| `obter_ativo(ativos, id_ativo)`                                                                                          | O ativo existe                                                   | Serviços  | Serviços de ativo e de vínculo, `perguntar_ativo`                                                            |
| `registrar_ativo_no_inventario`                                                                                          | O ID do ativo não está em uso                                    | Serviços  | `cadastrar_ativo`                                                                                            |
| `vincular_vulnerabilidade`                                                                                               | Vulnerabilidade existe no catálogo e não está vinculada ao ativo | Serviços  | `vincular_a_um_ativo`                                                                                        |
| `validar_tipo`, `validar_setor`, `validar_status`, `validar_status_vulnerabilidade`, `validar_cor`, `validar_tecnologia` | A opção digitada existe no menu                                  | Interface | `pedir_tipo`, `pedir_setor`, `pedir_status`, `pedir_status_vulnerabilidade`, `pedir_cor`, `pedir_tecnologia` |
| `pedir_int`, `pedir_float` (validação interna)                                                                           | Número válido, não vazio e maior que zero                        | Interface | Vários                                                                                                       |
| `pedir_id_disponivel`                                                                                                    | ID não está em uso (pede de novo)                                | Interface | `cadastrar_ativo`                                                                                            |

## ✨ Tipos de Validação Aplicados

- **Presença:** campos obrigatórios não podem ser vazios
- **Tipo:** ID e números devem ser conversíveis para `int` ou `float`; demais campos são `str` ou `Enum`
- **Formato:** nome e responsável não podem ser só números
- **Domínio:** enums e tipos só aceitam as opções predefinidas
- **Faixa:** ID e medidas maiores que zero; CVSS de 0.1 a 10.0
- **Integridade:** vínculos só com vulnerabilidades do catálogo e sem duplicidade

## 🫧 Estratégia de Tratamento de Erro

- Cada validação levanta `DadoInvalidoError` (exceção customizada) com a mensagem do erro;
- As regras ficam no **domínio** e nos **serviços**; a **interface** captura a exceção, exibe a mensagem e pede novamente;
- Regras importantes, como a faixa do CVSS, são checadas na interface (para pedir de novo) e nos serviços (como garantia);
- O programa **não encerra** por erro de entrada — o usuário pode tentar de novo;
- Mensagens **não expõem** stack trace nem detalhes internos;
- **Ctrl+C** e **Ctrl+D** são tratados no `menu_principal` (encerram limpo).

## ✨ Valores de Fronteira Testados

| Campo | Valor de fronteira | Comportamento esperado                      |
| ----- | ------------------ | ------------------------------------------- |
| ID    | 0                  | Rejeitado ("não pode ser nulo ou negativo") |
| ID    | -1                 | Rejeitado                                   |
| ID    | 1                  | Aceito (menor ID válido)                    |
| ID    | "abc"              | Rejeitado ("Digite um número válido")       |
| ID    | "" (vazio)         | Rejeitado ("não pode ser vazio")            |
| Nome  | "" (vazio)         | Rejeitado                                   |
| Nome  | "123"              | Rejeitado ("só números")                    |
| Nome  | "Rafael Torres"    | Aceito                                      |
| Tipo  | "5"                | Rejeitado (não existe)                      |
| Tipo  | "1"                | Aceito (Notebook)                           |
| CVSS  | 0                  | Rejeitado                                   |
| CVSS  | 0.04               | Rejeitado (vira 0.0 ao arredondar)          |
| CVSS  | 0.1                | Aceito (menor nota válida)                  |
| CVSS  | 10                 | Aceito (maior nota válida)                  |
| CVSS  | 10.1               | Rejeitado                                   |
| CVSS  | "7,4"              | Aceito como 7.4 (vírgula como separador)    |
