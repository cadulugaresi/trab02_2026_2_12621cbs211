# PRODUCT.md — Inventário de ativos e vulnerabilidades (Trabalho 2)

## O que é

Sistema web para gerenciar os ativos de TI de uma empresa (notebooks, servidores, roteadores e impressoras), as vulnerabilidades que afetam esses ativos e o risco de cada um. O risco é calculado com álgebra linear: risco próprio (CVSS das vulnerabilidades não corrigidas × fator de exposição do ativo), risco herdado (pelas dependências entre ativos) e risco efetivo (a soma dos dois).

É o Trabalho 2 da disciplina de Cibersegurança (turma 2) da UFU. O backend já existe e está completo: API HTTP em Flask, serviços, domínio e persistência em SQLite, rodando num container Docker. Este frontend é a aplicação web que usa essa API.

## Quem usa

- O próprio aluno (Cadu), que vai usar o sistema de verdade e apresentá-lo aos professores.
- Os professores (Igor e Amanda), que avaliam o trabalho na apresentação, possivelmente num computador Windows.
- Pessoa fictícia de exemplo nos dados: Rafael Torres.

## O que o usuário faz aqui

1. Vê, logo ao abrir, onde está o perigo: quantas vulnerabilidades críticas estão abertas, qual setor está mais exposto, quais ativos estão no topo do risco.
2. Cadastra, edita e exclui ativos e vulnerabilidades.
3. Vincula vulnerabilidades a ativos e acompanha o status de tratamento (Aberta, Em tratamento, Corrigida, Aceita).
4. Cadastra as dependências entre ativos (quem depende de quem, e com que fração).
5. Consulta o ranking de risco e entende de onde vem o risco de cada ativo (próprio ou herdado).
6. Explora o mapa de dependências entre ativos.

## Modo

Operate. O usuário completa tarefas. Clareza, consistência e capricho nos detalhes vêm antes de efeito. A personalidade está nos componentes-assinatura e na tipografia, não em decoração.

## Restrições

- O backend NÃO muda: a API, os serviços, o domínio e a persistência ficam como estão. O frontend só consome as rotas existentes (lista em DESIGN.md, seção "API usada").
- O próprio Flask serve as páginas, na mesma porta 5000 e na mesma origem da API (sem CORS). Os arquivos do frontend ficam dentro de `inventario/` para o `Dockerfile` copiar.
- Os caminhos da API (`/ativos`, `/vulnerabilidades`...) já são usados pela API. A navegação do frontend usa rotas com `#` (ex.: `/#/ativos/3`), servidas por um único `index.html` em `/`.
- Sem CDN e sem dependência de internet: fontes, ícones e qualquer biblioteca ficam dentro do projeto (a apresentação pode ser feita offline).
- Sem framework de frontend e sem etapa de build: HTML, CSS e JavaScript puros (módulos ES). Uma única base de JavaScript para todos os temas; o tema é só CSS.
- Desktop primeiro; depois celular.
- Prazo: entrega em 27/11/2026.

## Fora do escopo desta entrega

- Tema Task Bar Hero (estilo RPG): vem depois, como segundo tema trocável. A base de JS e as variáveis de CSS devem permitir isso sem reescrever telas.
- Modo escuro: só se sobrar tempo. Mesmo assim, todas as cores ficam em variáveis desde o início.
- Login e usuários: não existem. A saudação usa um nome fixo ("Anakin").
