# Critérios de Aceitação — CRUD de Ativos e Vulnerabilidades

UID: S2_06

Cenários em formato Dado–Quando–Então para as quatro operações do CRUD, cobrindo caminhos de sucesso, erro e borda.

## Create — Cadastrar ativo

### CA-01 — Cadastro com dados válidos (sucesso)
**Dado** que o sistema está no menu principal,
**Quando** o usuário escolhe "Cadastrar ativo" e informa ID único, nome, categoria, setor, responsável e status válidos,
**Então** o sistema exibe "Ativo cadastrado com sucesso" e o ativo aparece na listagem.
**Requisito:** RF-01, RF-02

### CA-02 — Tentativa de cadastro com ID já existente (erro)
**Dado** que existe um ativo cadastrado com ID 1,
**Quando** o usuário tenta cadastrar outro ativo com ID 1,
**Então** o sistema exibe "Já existe um ativo cadastrado com este ID. Tente outro." e pede um novo ID.
**Requisito:** RF-02, RN-01

### CA-03 — Cadastro com campo vazio (borda)
**Dado** que o sistema está no cadastro de ativo,
**Quando** o usuário deixa o nome vazio e aperta Enter,
**Então** o sistema exibe "Este campo não pode ser vazio" e pede o campo novamente.
**Requisito:** RF-02, RN-02

### CA-04 — Cadastro com nome só de números (borda)
**Dado** que o sistema está no cadastro de ativo,
**Quando** o usuário informa "123" como nome,
**Então** o sistema exibe "Este campo não pode ser composto apenas por números" e pede novamente.
**Requisito:** RF-02

## Read — Consultar ativo

### CA-05 — Busca por ID existente (sucesso)
**Dado** que existe um ativo com ID 1 cadastrado,
**Quando** o usuário busca por ID 1,
**Então** o sistema exibe os dados do ativo (ID, nome, categoria, setor, responsável, status).
**Requisito:** RF-04

### CA-06 — Busca por ID inexistente (erro)
**Dado** que não existe ativo com ID 999,
**Quando** o usuário busca por ID 999,
**Então** o sistema exibe "Nenhum ativo encontrado."
**Requisito:** RF-04

### CA-07 — Busca parcial por nome (sucesso)
**Dado** que existem ativos chamados "macbook", "mac-mini" e "imac",
**Quando** o usuário busca pelo nome "mac",
**Então** o sistema exibe os três ativos.
**Requisito:** RF-04

### CA-08 — Busca por nome com maiúsculas (borda)
**Dado** que existe um ativo chamado "macbook",
**Quando** o usuário busca por "MAC",
**Então** o sistema exibe o ativo (busca case-insensitive).
**Requisito:** RF-04

## Update — Atualizar ativo

### CA-09 — Edição de responsável (sucesso)
**Dado** que existe um ativo com ID 1,
**Quando** o usuário escolhe editar o responsável e informa um novo nome válido,
**Então** o sistema exibe "Responsável atualizado com sucesso" e o novo valor persiste após reabrir o programa.
**Requisito:** RF-05

### CA-10 — Edição de ativo inexistente (erro)
**Dado** que não existe ativo com ID 999,
**Quando** o usuário tenta editar o ativo 999,
**Então** o sistema exibe "Nenhum ativo com este ID cadastrado."
**Requisito:** RF-05

### CA-11 — Edição de categoria (sucesso)
**Dado** que existe um ativo cadastrado como NOTEBOOK,
**Quando** o usuário edita a categoria para SERVIDOR,
**Então** o sistema exibe "Categoria do ativo atualizada com sucesso" e o novo valor persiste.
**Requisito:** RF-05

## Delete — Remover ativo

### CA-12 — Remoção com confirmação (sucesso)
**Dado** que existe um ativo com ID 1,
**Quando** o usuário escolhe excluir, informa o ID 1 e confirma com "sim",
**Então** o sistema exibe "Ativo excluído com sucesso" e o ativo some da listagem.
**Requisito:** RF-06

### CA-13 — Remoção cancelada (borda)
**Dado** que existe um ativo com ID 1,
**Quando** o usuário escolhe excluir, informa o ID 1 e **não** confirma,
**Então** o sistema exibe "Exclusão cancelada" e o ativo permanece na listagem.
**Requisito:** RF-06

### CA-14 — Remoção de ativo inexistente (erro)
**Dado** que não existe ativo com ID 999,
**Quando** o usuário tenta excluir o ID 999,
**Então** o sistema exibe "Ativo não encontrado."
**Requisito:** RF-06

### CA-15 — Remoção remove vulnerabilidades associadas (sucesso)
**Dado** que existe um ativo com ID 1 e vulnerabilidades associadas,
**Quando** o usuário exclui o ativo 1,
**Então** o ativo e suas vulnerabilidades somem da listagem e do arquivo `ativos.json`.
**Requisito:** RF-06, RN-03

## Rastreabilidade

| Cenário | Requisito | Tipo |
|---|---|---|
| CA-01 | RF-01, RF-02 | Sucesso |
| CA-02 | RF-02, RN-01 | Erro |
| CA-03 | RF-02, RN-02 | Borda |
| CA-04 | RF-02 | Borda |
| CA-05 | RF-04 | Sucesso |
| CA-06 | RF-04 | Erro |
| CA-07 | RF-04 | Sucesso |
| CA-08 | RF-04 | Borda |
| CA-09 | RF-05 | Sucesso |
| CA-10 | RF-05 | Erro |
| CA-11 | RF-05 | Sucesso |
| CA-12 | RF-06 | Sucesso |
| CA-13 | RF-06 | Borda |
| CA-14 | RF-06 | Erro |
| CA-15 | RF-06, RN-03 | Sucesso |