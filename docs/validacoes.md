# Validações e Matriz de Regras

UID: S2_05 (atualizado na S4_01 e na S4_05)

Matriz campo × regra × mensagem de erro para as entradas do sistema, tanto pelo menu do terminal quanto pela API HTTP. As regras ficam no domínio e nos serviços, então valem para as duas interfaces. Quando uma mensagem só existe no menu ou só na API, a tabela indica.

## ✨ Matriz de Validação

### Ativos

| Campo                                        | Tipo   | Regra                                                        | Mensagem de erro                                                                  |
| -------------------------------------------- | ------ | ------------------------------------------------------------ | --------------------------------------------------------------------------------- |
| ID do ativo                                  | int    | Não vazio (menu)                                             | "Este campo não pode ser vazio."                                                  |
| ID do ativo                                  | int    | Formato numérico (menu)                                      | "Digite um número válido"                                                         |
| ID do ativo                                  | int    | Só número inteiro (API: texto, `true` ou `1.0`)              | "Este campo precisa ser um número inteiro."                                       |
| ID do ativo                                  | int    | Maior que zero                                               | "Este campo não pode ser nulo ou negativo."                                       |
| ID do ativo                                  | int    | No máximo `2**63 - 1`, o maior inteiro que o SQLite guarda   | "Este número é grande demais. O máximo aceito é 9223372036854775807."             |
| ID do ativo                                  | int    | Único (menu)                                                 | "Já existe um ativo cadastrado com este ID. Tente outro."                         |
| ID do ativo                                  | int    | Único (serviço e API)                                        | "Já existe um ativo cadastrado com este ID."                                      |
| Nome do ativo                                | str    | Texto (API: número ou booleano)                              | "Este campo precisa ser um texto."                                                |
| Nome do ativo                                | str    | Não vazio (só espaços conta como vazio)                      | "Este campo não pode ser vazio."                                                  |
| Nome do ativo                                | str    | Não só números                                               | "Este campo não pode ser composto apenas por números."                            |
| Responsável                                  | str    | Mesmas regras do nome                                        | Mesmas mensagens do nome                                                          |
| Sistema operacional                          | str    | Mesmas regras do nome                                        | Mesmas mensagens do nome                                                          |
| Tipo                                         | Classe | Opção 1 a 4 (menu): Notebook, Servidor, Roteador, Impressora | "Tipo inválido. Tente novamente."                                                 |
| Tipo                                         | Classe | Nome de um tipo existente (API)                              | "Dados do ativo incompletos ou inválidos."                                        |
| Setor                                        | Enum   | Opção 1 a 5 (menu): TI, FINANCEIRO, MARKETING, RH, JURIDICO  | "Setor inválido. Tente novamente."                                                |
| Status do ativo                              | Enum   | Opção 1 a 3 (menu): ATIVO, INATIVO, EM_MANUTENCAO            | "Status inválido. Tente novamente."                                               |
| Cor                                          | Enum   | Opção 1 ou 2 (menu): COLORIDA, PRETA_E_BRANCA                | "Cor inválida. Tente novamente."                                                  |
| Tecnologia                                   | Enum   | Opção 1 ou 2 (menu): TINTA, LASER                            | "Tecnologia inválida. Tente novamente."                                           |
| Setor, status, cor, tecnologia               | Enum   | Só número inteiro (API: `true` ou `1.0`)                     | "Este campo precisa ser um número inteiro."                                       |
| Setor, status, cor, tecnologia               | Enum   | Valor que existe no Enum (API)                               | "Dados do ativo incompletos ou inválidos."                                        |
| Tela, armazenamento                          | float  | Número (não texto nem booleano)                              | "Este campo precisa ser um número."                                               |
| Tela, armazenamento                          | float  | Finito (não `NaN` nem infinito)                              | "Este campo precisa ser um número finito."                                        |
| Tela, armazenamento                          | float  | Maior que zero (o menu aceita vírgula)                       | "Este campo não pode ser nulo ou negativo."                                       |
| RAM, portas, velocidade                      | int    | Só número inteiro                                            | "Este campo precisa ser um número inteiro."                                       |
| RAM, portas, velocidade                      | int    | Maior que zero                                               | "Este campo não pode ser nulo ou negativo."                                       |
| Tela, armazenamento, RAM, portas, velocidade | número | Se for inteiro, no máximo `2**63 - 1`                        | "Este número é grande demais. O máximo aceito é 9223372036854775807."             |
| Fator de exposição                           | float  | Número finito (não texto, booleano, `NaN` nem infinito)      | "Este campo precisa ser um número." ou "Este campo precisa ser um número finito." |
| Fator de exposição                           | float  | Maior que 0 e no máximo 2                                    | "O fator de exposição deve ser maior que 0 e no máximo 2."                        |
| Campo obrigatório                            | —      | Presente no corpo da requisição (API)                        | "Dados do ativo incompletos ou inválidos."                                        |

### Vulnerabilidades

| Campo                            | Tipo  | Regra                                                        | Mensagem de erro                                                             |
| -------------------------------- | ----- | ------------------------------------------------------------ | ---------------------------------------------------------------------------- |
| Nome da vulnerabilidade          | str   | Mesmas regras do nome do ativo                               | Mesmas mensagens do nome do ativo                                            |
| CVSS                             | float | Formato numérico (menu)                                      | "Digite um número válido"                                                    |
| CVSS                             | float | Número (API: não texto nem booleano)                         | "Este campo precisa ser um número."                                          |
| CVSS                             | float | Finito (não `NaN` nem infinito)                              | "Este campo precisa ser um número finito."                                   |
| CVSS                             | float | De 0.1 a 10.0, arredondado para uma casa antes de validar    | "O CVSS deve estar entre 0.1 e 10."                                          |
| Nome ou CVSS                     | —     | Presentes no corpo da requisição (API)                       | "Dados da vulnerabilidade incompletos ou inválidos."                         |
| Status de tratamento             | Enum  | Opção 1 a 4 (menu): ABERTA, EM_TRATAMENTO, CORRIGIDA, ACEITA | "Status inválido. Tente novamente."                                          |
| Status de tratamento             | Enum  | Só número inteiro (API: `true` ou `1.0`)                     | "Este campo precisa ser um número inteiro."                                  |
| Status de tratamento             | Enum  | Presente e com valor que existe no Enum (API)                | "Dados incompletos ou inválidos."                                            |
| ID da vulnerabilidade no vínculo | int   | Inteiro maior que zero e no máximo `2**63 - 1`               | Mesmas mensagens do ID do ativo                                              |
| Vínculo                          | —     | A vulnerabilidade deve existir no catálogo                   | "Vulnerabilidade não encontrada no catálogo."                                |
| Vínculo                          | —     | Não pode vincular duas vezes ao mesmo ativo                  | "Esta vulnerabilidade já está vinculada a este ativo."                       |
| Desvínculo                       | —     | A vulnerabilidade deve estar vinculada ao ativo              | "Esta vulnerabilidade não está vinculada a este ativo."                      |
| Atualização de status            | —     | A vulnerabilidade deve estar vinculada ao ativo              | "Este ativo não possui nenhuma vulnerabilidade com este ID vinculada a ele." |
| Ativo informado                  | —     | O ativo deve existir                                         | "Ativo não encontrado."                                                      |

### Dependências

| Campo                   | Tipo  | Regra                                                            | Mensagem de erro                                                                           |
| ----------------------- | ----- | ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| Ativos da dependência   | —     | Os dois ativos devem existir                                     | "Ativo não encontrado."                                                                    |
| Dependência             | —     | Um ativo não pode depender dele próprio                          | "Um ativo não pode depender dele próprio."                                                 |
| Dependência             | —     | Não pode cadastrar a mesma dependência duas vezes                | "Este ativo já possui essa dependência."                                                   |
| Dependência             | —     | Para remover ou atualizar, a dependência deve existir            | "Este ativo não possui essa dependência."                                                  |
| Dependência             | —     | Na atualização, não pode trocar para um ativo do qual já depende | "Este ativo já depende do ativo N. Edite essa dependência em vez disso."                   |
| Fração                  | float | Número finito (não texto, booleano, `NaN` nem infinito)          | "Este campo precisa ser um número." ou "Este campo precisa ser um número finito."          |
| Fração                  | float | Maior que zero                                                   | "A fração precisa ser maior que zero."                                                     |
| Fração                  | float | A soma das frações do ativo fica abaixo de 1                     | "A soma das frações precisa ficar abaixo de 1. Ainda cabem X." (X com três casas decimais) |
| Fração (edição no menu) | float | Formato numérico                                                 | "Digite um número válido."                                                                 |

### Respostas de erro da API

Toda resposta de erro da API é um JSON no formato `{"erro": "..."}`, nunca uma página HTML.

| Situação                                                                                 | Status | Resposta                                            |
| ---------------------------------------------------------------------------------------- | ------ | --------------------------------------------------- |
| Corpo que não é JSON ou JSON malformado                                                  | 400    | Mensagem genérica da rota                           |
| Campo obrigatório faltando ou que não pode ser lido                                      | 400    | Mensagem genérica da rota                           |
| Regra do domínio ou dos serviços violada (`DadoInvalidoError`)                           | 400    | A mensagem da regra, como nas tabelas acima         |
| Filtro inválido no `GET /ativos` (tipo, status ou ordenação)                             | 400    | "Filtro inválido."                                  |
| Ativo, vulnerabilidade, vínculo ou dependência inexistente (`RecursoNaoEncontradoError`) | 404    | A mensagem do recurso, como "Ativo não encontrado." |
| Rota que não existe (inclusive id em texto na URL, como `/ativos/abc`)                   | 404    | "Rota não encontrada."                              |
| Método que a rota não aceita                                                             | 405    | "Método não permitido para esta rota."              |
| Dados que impedem a análise de risco em `GET /riscos`                                    | 409    | A mensagem da análise de risco                      |
| Falha do banco (`PersistenciaError`)                                                     | 500    | A mensagem da persistência                          |
| Erro inesperado                                                                          | 500    | "Erro interno do servidor.", sem detalhes internos  |

A mensagem genérica muda conforme o recurso: "Dados do ativo incompletos ou inválidos." nas rotas de ativo, "Dados da vulnerabilidade incompletos ou inválidos." nas de vulnerabilidade, "Dados da dependência incompletos ou inválidos." nas de dependência e "Dados incompletos ou inválidos." nas de vínculo.

## 🫧 Funções Validadoras

| Função                                                                                                                   | O que valida                                                                                            | Camada    | Onde é usada                                                                                                                                                                                                                                                                   |
| ------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `validar_numero(valor)`                                                                                                  | É `int` ou `float` (booleano não conta), é finito e, se for inteiro, não passa de `2**63 - 1`           | Domínio   | `validar_numero_positivo`, `validar_cvss`, `validar_fator_exposicao`, `validar_fracao`                                                                                                                                                                                         |
| `validar_numero_positivo(valor)`                                                                                         | `validar_numero` e maior que zero                                                                       | Domínio   | `validar_inteiro_positivo`, `Notebook.validar_dados` (tela), `Servidor.validar_dados` (armazenamento), `pedir_float`                                                                                                                                                           |
| `validar_inteiro_positivo(valor)`                                                                                        | Só `int` e `validar_numero_positivo`                                                                    | Domínio   | `Ativo.validar_dados` (ID), `Roteador.validar_dados`, `Servidor.validar_dados` (RAM), os `de_dicionario` (antes de criar cada Enum), rotas de vínculo (status de tratamento), `vincular_vulnerabilidade`, `cadastrar_dependencia` e `atualizar_dependencia` (ids), `pedir_int` |
| `validar_texto_obrigatorio(texto)`                                                                                       | É texto, não vazio (espaços não contam) e não só números                                                | Domínio   | `pedir_info`, `Ativo.validar_dados` (nome, responsável), `Notebook.validar_dados` (sistema operacional), `registrar_vulnerabilidade_no_catalogo`, `atualizar_vulnerabilidade_no_catalogo`                                                                                      |
| `validar_cvss(cvss)`                                                                                                     | `validar_numero`, faixa de 0.1 a 10.0 e arredondamento                                                  | Domínio   | `pedir_cvss`, `registrar_vulnerabilidade_no_catalogo`, `atualizar_vulnerabilidade_no_catalogo`                                                                                                                                                                                 |
| `validar_fator_exposicao(fator)`                                                                                         | `validar_numero`, maior que 0 e no máximo 2                                                             | Domínio   | `pedir_fator_exposicao`, `Ativo.validar_dados`                                                                                                                                                                                                                                 |
| `validar_fracao_da_dependencia(soma_atual, fracao)`                                                                      | `validar_fracao` (`validar_numero` e maior que zero) e `validar_soma_fracao` (soma abaixo de 1)         | Domínio   | `cadastrar_dependencia`, `atualizar_dependencia`                                                                                                                                                                                                                               |
| `validar_dependencia_de_si_mesmo`                                                                                        | O ativo não depende dele próprio                                                                        | Domínio   | `cadastrar_dependencia`, `atualizar_dependencia`                                                                                                                                                                                                                               |
| `Ativo.validar_dados()`                                                                                                  | Os campos comuns; cada subclasse acrescenta os seus (polimorfismo, sem `if/elif` por tipo)              | Domínio   | `registrar_ativo_no_inventario`                                                                                                                                                                                                                                                |
| `obter_ativo(ativos, id_ativo)`                                                                                          | O ativo existe (senão levanta `RecursoNaoEncontradoError`)                                              | Serviços  | Serviços de ativo, de vínculo e de dependência, `perguntar_ativo`, rotas da API                                                                                                                                                                                                |
| `obter_vulnerabilidade(catalogo, id_vulnerabilidade)`                                                                    | A vulnerabilidade existe (senão levanta `RecursoNaoEncontradoError`)                                    | Serviços  | `vincular_vulnerabilidade`, `excluir_vulnerabilidade_do_catalogo`, `atualizar_vulnerabilidade_no_catalogo`, rotas de vulnerabilidade                                                                                                                                           |
| `garantir_que_dependencia_existe(ativo, id_ativo_do_qual_depende)`                                                       | A dependência existe (senão levanta `RecursoNaoEncontradoError`)                                        | Serviços  | `remover_dependencia`, `atualizar_dependencia`, `PUT /ativos/<id>/dependencias/<id_dep>`                                                                                                                                                                                       |
| `registrar_ativo_no_inventario`                                                                                          | Chama `validar_dados` e confere se o ID não está em uso                                                 | Serviços  | `cadastrar_ativo`, `POST /ativos`                                                                                                                                                                                                                                              |
| `atualizar_ativo_no_inventario`                                                                                          | Chama `validar_dados` e confere se o ativo existe                                                       | Serviços  | `editar_ativo` do menu, `PUT /ativos/<id>`                                                                                                                                                                                                                                     |
| `atualizar_vulnerabilidade_no_catalogo`                                                                                  | A vulnerabilidade existe, o nome (`validar_texto_obrigatorio`) e o CVSS (`validar_cvss`)                | Serviços  | `editar_vulnerabilidade` do menu, `PUT /vulnerabilidades/<id>`                                                                                                                                                                                                                 |
| `vincular_vulnerabilidade`                                                                                               | ID da vulnerabilidade inteiro; a vulnerabilidade existe no catálogo e não está vinculada ao ativo       | Serviços  | `vincular_a_um_ativo`, `POST /ativos/<id>/vulnerabilidades`                                                                                                                                                                                                                    |
| `validar_tipo`, `validar_setor`, `validar_status`, `validar_status_vulnerabilidade`, `validar_cor`, `validar_tecnologia` | A opção digitada existe no menu                                                                         | Interface | `pedir_tipo`, `pedir_setor`, `pedir_status`, `pedir_status_vulnerabilidade`, `pedir_cor`, `pedir_tecnologia`                                                                                                                                                                   |
| `pedir_int`, `pedir_float`                                                                                               | Não vazio e conversível; o valor é conferido por `validar_inteiro_positivo` e `validar_numero_positivo` | Interface | Vários                                                                                                                                                                                                                                                                         |
| `pedir_id_disponivel`                                                                                                    | ID não está em uso (pede de novo)                                                                       | Interface | `cadastrar_ativo`                                                                                                                                                                                                                                                              |
| `filtrar_ativos(ativos, filtros)`                                                                                        | O tipo e o status pedidos existem (senão a rota responde 400)                                           | Interface | `GET /ativos`                                                                                                                                                                                                                                                                  |

## ✨ Tipos de Validação Aplicados

- **Presença:** campos obrigatórios não podem faltar nem ser vazios (só espaços conta como vazio)
- **Tipo:** cada campo só aceita o tipo esperado: texto, número (`int` ou `float`, nunca booleano) ou número inteiro; no menu, o que foi digitado precisa ser conversível
- **Formato:** nome, responsável e sistema operacional não podem ser só números
- **Domínio:** enums e tipos só aceitam as opções predefinidas
- **Faixa:** ID e medidas maiores que zero; CVSS de 0.1 a 10.0; fator de exposição maior que 0 e no máximo 2; fração maior que zero e soma das frações abaixo de 1; números finitos (sem `NaN` nem infinito); inteiros até `2**63 - 1` (9223372036854775807), o maior inteiro que o SQLite guarda
- **Integridade:** vínculos só com vulnerabilidades do catálogo e sem duplicidade; dependências só entre ativos existentes, sem repetição e sem o ativo depender dele próprio

## 🫧 Estratégia de Tratamento de Erro

- Cada validação levanta `DadoInvalidoError` (exceção customizada) com a mensagem do erro;
- As regras ficam no **domínio** e nos **serviços**; o **menu** captura a exceção, exibe a mensagem e pede novamente, e a **API** devolve a mensagem em JSON pelos tratadores de erro do `criar_app`: 400 para `DadoInvalidoError` e 404 para a filha dela, `RecursoNaoEncontradoError`;
- Regras importantes, como a faixa do CVSS, são checadas no menu (para pedir de novo) e nos serviços (como garantia). Como a API chama os mesmos serviços, ela recebe as mesmas garantias;
- Os serviços gravam no banco **antes** de alterar os dados em memória, e as telas de edição do menu trabalham sobre uma cópia do objeto. Se a gravação falhar, a memória continua igual ao banco, e a tela mostra o motivo e "As alterações não foram salvas.";
- O programa **não encerra** por erro de entrada: o usuário pode tentar de novo;
- Mensagens **não expõem** stack trace nem detalhes internos, nem no menu nem na API;
- **Ctrl+C** e **Ctrl+D** são tratados no `menu_principal` (encerram limpo).

## ✨ Valores de Fronteira Testados

| Campo                            | Valor de fronteira                                                     | Comportamento esperado                      |
| -------------------------------- | ---------------------------------------------------------------------- | ------------------------------------------- |
| ID                               | 0                                                                      | Rejeitado ("não pode ser nulo ou negativo") |
| ID                               | -1                                                                     | Rejeitado                                   |
| ID                               | 1                                                                      | Aceito (menor ID válido)                    |
| ID                               | `2**63 - 1` (9223372036854775807)                                      | Aceito (maior ID válido)                    |
| ID                               | `2**63`                                                                | Rejeitado ("grande demais")                 |
| ID                               | "abc" (menu)                                                           | Rejeitado ("Digite um número válido")       |
| ID                               | "abc" (API)                                                            | Rejeitado ("precisa ser um número inteiro") |
| ID                               | "" (vazio)                                                             | Rejeitado ("não pode ser vazio")            |
| Nome                             | "" (vazio)                                                             | Rejeitado                                   |
| Nome                             | "   " (só espaços)                                                     | Rejeitado ("não pode ser vazio")            |
| Nome                             | "123"                                                                  | Rejeitado ("só números")                    |
| Nome                             | 123 (número, API)                                                      | Rejeitado ("precisa ser um texto")          |
| Nome                             | "Rafael Torres"                                                        | Aceito                                      |
| Tipo                             | "5"                                                                    | Rejeitado (não existe)                      |
| Tipo                             | "1"                                                                    | Aceito (Notebook)                           |
| Setor, status, cor, tecnologia   | `true` ou `1.0` (API)                                                  | Rejeitado ("precisa ser um número inteiro") |
| Tela                             | `Infinity` (API)                                                       | Rejeitado ("precisa ser um número finito")  |
| Tela                             | `10**30` como inteiro (API)                                            | Rejeitado ("grande demais")                 |
| Portas                           | 8.5 (API)                                                              | Rejeitado ("precisa ser um número inteiro") |
| Tela, armazenamento              | "nan", "inf" ou "Infinity" (menu)                                      | Rejeitado ("precisa ser um número finito")  |
| CVSS                             | 0                                                                      | Rejeitado                                   |
| CVSS                             | 0.04                                                                   | Rejeitado (vira 0.0 ao arredondar)          |
| CVSS                             | 0.1                                                                    | Aceito (menor nota válida)                  |
| CVSS                             | 10                                                                     | Aceito (maior nota válida)                  |
| CVSS                             | 10.1                                                                   | Rejeitado                                   |
| CVSS                             | "7,4"                                                                  | Aceito como 7.4 (vírgula como separador)    |
| CVSS                             | `NaN`, `Infinity` ou `-Infinity` (API)                                 | Rejeitado ("precisa ser um número finito")  |
| CVSS                             | `true` (API)                                                           | Rejeitado ("precisa ser um número")         |
| Fator de exposição               | `NaN` (API) ou `true` (API)                                            | Rejeitado                                   |
| Fração da dependência            | `NaN`, infinito ou menos infinito                                      | Rejeitado ("precisa ser um número finito")  |
| ID da vulnerabilidade no vínculo | `true`, `1.0` ou `2**63` (API)                                         | Rejeitado                                   |
| ID na URL                        | `/ativos/abc`                                                          | Rejeitado (404 "Rota não encontrada.")      |
| Filtro do `GET /ativos`          | `tipo=Tablet`, `status=9`, `status=abc`, `status=1.0` ou `ordenar=xyz` | Rejeitado ("Filtro inválido.")              |
