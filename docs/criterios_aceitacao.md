# Critérios de Aceitação — CRUD de Ativos e Vulnerabilidades

UID: S2_06 (atualizado na S4_01)

Cenários em formato Dado–Quando–Então para o CRUD de ativos e para as operações de vulnerabilidades, cobrindo caminhos de sucesso, erro e borda.

## ✨ Create — Cadastrar ativo

### CA-01 — Cadastro com dados válidos (sucesso)
**Dado** que o sistema está no menu principal,
**Quando** o usuário escolhe "Cadastrar ativo" e informa tipo, ID único, nome, setor, responsável, status e os atributos específicos do tipo,
**Então** o sistema exibe "Ativo cadastrado com sucesso!" e o ativo aparece na listagem.
**Requisito:** RF-01, RF-02

### CA-02 — Tentativa de cadastro com ID já existente (erro)
**Dado** que existe um ativo cadastrado com ID 1,
**Quando** o usuário tenta cadastrar outro ativo com ID 1,
**Então** o sistema exibe "Já existe um ativo cadastrado com este ID. Tente outro." e pede um novo ID.
**Requisito:** RF-02, RN-01

### CA-03 — Cadastro com campo vazio (borda)
**Dado** que o sistema está no cadastro de ativo,
**Quando** o usuário deixa o nome vazio e aperta Enter,
**Então** o sistema exibe "Este campo não pode ser vazio." e pede o campo novamente.
**Requisito:** RF-02, RN-02

### CA-04 — Cadastro com nome só de números (borda)
**Dado** que o sistema está no cadastro de ativo,
**Quando** o usuário informa "123" como nome,
**Então** o sistema exibe "Este campo não pode ser composto apenas por números." e pede novamente.
**Requisito:** RF-02

## 🫧 Read — Consultar ativo

### CA-05 — Busca por ID existente (sucesso)
**Dado** que existe um ativo com ID 1 cadastrado,
**Quando** o usuário busca por ID 1,
**Então** o sistema exibe os dados do ativo (ID, nome, tipo, setor, responsável, status e atributos específicos).
**Requisito:** RF-05

### CA-06 — Busca por ID inexistente (erro)
**Dado** que não existe ativo com ID 999,
**Quando** o usuário busca por ID 999,
**Então** o sistema exibe "Nenhum ativo encontrado."
**Requisito:** RF-05

### CA-07 — Busca parcial por nome (sucesso)
**Dado** que existem ativos chamados "macbook", "mac-mini" e "imac",
**Quando** o usuário busca pelo nome "mac",
**Então** o sistema exibe os três ativos.
**Requisito:** RF-05

### CA-08 — Busca por nome com maiúsculas (borda)
**Dado** que existe um ativo chamado "macbook",
**Quando** o usuário busca por "MAC",
**Então** o sistema exibe o ativo (busca case-insensitive).
**Requisito:** RF-05

## ✨ Update — Atualizar ativo

### CA-09 — Edição de responsável (sucesso)
**Dado** que existe um ativo com ID 1,
**Quando** o usuário escolhe editar o responsável, informa um novo nome válido e escolhe "Voltar",
**Então** o sistema exibe "Responsável atualizado com sucesso." e o novo valor persiste após reabrir o programa.
**Requisito:** RF-06

### CA-10 — Edição de ativo inexistente (erro)
**Dado** que não existe ativo com ID 999,
**Quando** o usuário tenta editar o ativo 999,
**Então** o sistema exibe "Ativo não encontrado." e não abre o menu de edição.
**Requisito:** RF-06

### CA-11 — Troca de tipo mantendo vulnerabilidades (sucesso)
**Dado** que existe um ativo cadastrado como Notebook, com vulnerabilidades vinculadas,
**Quando** o usuário edita o tipo para Servidor e informa RAM e armazenamento,
**Então** o sistema exibe "Tipo do ativo atualizado com sucesso!", o ativo passa a ser um Servidor e continua com as mesmas vulnerabilidades.
**Requisito:** RF-06, RN-08

## 🫧 Delete — Remover ativo

### CA-12 — Remoção com confirmação (sucesso)
**Dado** que existe um ativo com ID 1,
**Quando** o usuário escolhe excluir, informa o ID 1 e confirma com "sim",
**Então** o sistema exibe "Ativo excluído com sucesso!" e o ativo some da listagem.
**Requisito:** RF-07

### CA-13 — Remoção cancelada (borda)
**Dado** que existe um ativo com ID 1,
**Quando** o usuário escolhe excluir, informa o ID 1 e **não** confirma,
**Então** o sistema exibe "Exclusão cancelada." e o ativo permanece na listagem.
**Requisito:** RF-07

### CA-14 — Remoção de ativo inexistente (erro)
**Dado** que não existe ativo com ID 999,
**Quando** o usuário tenta excluir o ID 999,
**Então** o sistema exibe "Ativo não encontrado." e não pede confirmação.
**Requisito:** RF-07

### CA-15 — Remoção apaga os vínculos do ativo (sucesso)
**Dado** que existe um ativo com ID 1 e vulnerabilidades vinculadas,
**Quando** o usuário exclui o ativo 1,
**Então** o ativo e seus vínculos somem da listagem e do arquivo `ativos.json`, e as vulnerabilidades continuam no catálogo.
**Requisito:** RF-07, RN-03

## ✨ Vulnerabilidades

### CA-16 — Cadastro no catálogo com CVSS válido (sucesso)
**Dado** que o catálogo tem vulnerabilidades com IDs 1 e 3,
**Quando** o usuário cadastra "SMB desatualizado" com CVSS "8,14",
**Então** a vulnerabilidade recebe o ID 4, a nota é guardada como 8.1 e o nível exibido é "alto".
**Requisito:** RF-03, RN-04, RN-05, RN-09

### CA-17 — Cadastro com CVSS fora da faixa (borda)
**Dado** que o sistema está no cadastro de vulnerabilidade,
**Quando** o usuário informa o CVSS 15,
**Então** o sistema exibe "O CVSS deve estar entre 0.1 e 10." e pede a nota novamente.
**Requisito:** RF-03, RN-04

### CA-18 — Vínculo com status de tratamento (sucesso)
**Dado** que existem o ativo 1 e a vulnerabilidade 3 no catálogo,
**Quando** o usuário vincula a vulnerabilidade 3 ao ativo 1 com status "Em tratamento",
**Então** o sistema exibe "Vulnerabilidade vinculada com sucesso!" e a vulnerabilidade aparece no ativo com esse status.
**Requisito:** RF-09

### CA-19 — Vínculo duplicado (erro)
**Dado** que a vulnerabilidade 3 já está vinculada ao ativo 1,
**Quando** o usuário tenta vinculá-la de novo ao mesmo ativo,
**Então** o sistema exibe "Esta vulnerabilidade já está vinculada a este ativo." e o status anterior é mantido.
**Requisito:** RF-09, RN-06

### CA-20 — Desvínculo mantém o catálogo (sucesso)
**Dado** que a vulnerabilidade 3 está vinculada ao ativo 1,
**Quando** o usuário desvincula a vulnerabilidade 3 do ativo 1,
**Então** o sistema exibe "Vulnerabilidade desvinculada com sucesso!" e ela continua existindo no catálogo.
**Requisito:** RF-11

### CA-21 — Exclusão do catálogo desvincula de todos os ativos (sucesso)
**Dado** que a vulnerabilidade 3 está vinculada aos ativos 1 e 2,
**Quando** o usuário a exclui do catálogo e confirma com "sim",
**Então** ela some do catálogo e das vulnerabilidades dos dois ativos.
**Requisito:** RF-12, RN-07

## 🫧 Rastreabilidade

| Cenário | Requisito                  | Tipo    |
| ------- | -------------------------- | ------- |
| CA-01   | RF-01, RF-02               | Sucesso |
| CA-02   | RF-02, RN-01               | Erro    |
| CA-03   | RF-02, RN-02               | Borda   |
| CA-04   | RF-02                      | Borda   |
| CA-05   | RF-05                      | Sucesso |
| CA-06   | RF-05                      | Erro    |
| CA-07   | RF-05                      | Sucesso |
| CA-08   | RF-05                      | Borda   |
| CA-09   | RF-06                      | Sucesso |
| CA-10   | RF-06                      | Erro    |
| CA-11   | RF-06, RN-08               | Sucesso |
| CA-12   | RF-07                      | Sucesso |
| CA-13   | RF-07                      | Borda   |
| CA-14   | RF-07                      | Erro    |
| CA-15   | RF-07, RN-03               | Sucesso |
| CA-16   | RF-03, RN-04, RN-05, RN-09 | Sucesso |
| CA-17   | RF-03, RN-04               | Borda   |
| CA-18   | RF-09                      | Sucesso |
| CA-19   | RF-09, RN-06               | Erro    |
| CA-20   | RF-11                      | Sucesso |
| CA-21   | RF-12, RN-07               | Sucesso |
