# DESIGN.md — Tema macOS/iOS

Decisões tomadas com o Cadu em rodadas de perguntas e referências. As imagens citadas estão em `docs/referencias/`. Quando este arquivo e uma referência discordarem, vale este arquivo.

## 1. Clima

- Informações soltas sobre o fundo, sem caixas em volta de tudo. A hierarquia vem de títulos grandes, peso, tamanho e espaçamento (r1-01, r1-02).
- Gráficos sem moldura, fazendo parte da página (r1-02, r2-01, r2-02).
- Quase tudo preto e branco. Cor só onde carrega informação, sempre em detalhes pequenos: bolinhas, nome do nível, uma barra destacada, o campo de CVSS (r1-03 a r1-05, r2-04, r2-05).
- Espaçoso.
- Só o que flutua tem "cartão": janelas, balões, menus suspensos e o painel do menu lateral são brancos, com cantos bem arredondados e sombra larga e suave (r3-01).
- Proibido: azul (inclusive no foco), vidro fosco nos painéis, gradientes, texto em gradiente, rótulo pequeno em caixa alta acima de títulos, cartões iguais lado a lado como estrutura da página, animação de entrada em toda seção.

## 2. Cores (variáveis CSS)

Todas as cores ficam em variáveis no `:root`. O modo escuro, se entrar, só troca os valores.

| Variável | Valor | Uso |
|---|---|---|
| `--fundo` | `#FBFBFA` | fundo da página |
| `--superficie` | `#FFFFFF` | janelas, balões, menus, painel lateral |
| `--campo` | `#F1F1EF` | campos em pílula, faixa do segmentado |
| `--tinta` | `#0A0A0A` | texto principal, botões pretos, contador, cartão preto do segmentado |
| `--texto-secundario` | `#6E6D69` | textos de apoio, rótulos, placeholders (contraste de 4,6:1 sobre `--campo`) |
| `--texto-apagado` | `#A3A29D` | itens "já corrigida em" (histórico, apagado de propósito), setas das linhas |
| `--linha` | `rgba(0,0,0,0.08)` | divisórias finas |
| `--sombra-flutuante` | `0 18px 48px rgba(0,0,0,0.12), 0 4px 12px rgba(0,0,0,0.06)` | janelas e balões |
| `--veu` | `rgba(255,255,255,0.55)` + `backdrop-filter: blur(8px)` | fundo atrás de janelas e do menu aberto |

Gravidade das vulnerabilidades (limiares de `Vulnerabilidade.nivel()`), em tons escuros e sérios:

| Nível | CVSS | Cor |
|---|---|---|
| Baixo | até 3,9 | `#2F5A0E` |
| Médio | 4,0 a 6,9 | `#7A4A06` |
| Alto | 7,0 a 8,9 | `#8A3510` |
| Crítico | acima de 8,9 | `#7A1414` |

Bolinhas de estado (pequenas, ~7–8px):

| Uso | Verde | Amarelo | Vermelho | Cinza |
|---|---|---|---|---|
| Status do ativo | Ativo | Em manutenção | Inativo | — |
| Status de tratamento | Corrigida | Em tratamento | Aberta | Aceita |

Valores: verde `#3B7A17`, amarelo `#C98A0B`, vermelho `#B42318`, cinza `#8A8A85`.

Erro da API: fundo `#7A1414`, texto branco.

## 3. Tipografia

- Fonte: **Inter** em todos os sistemas, com os arquivos `woff2` dentro do projeto (licença SIL OFL), com eixo de tamanho óptico (`opsz`). Não usar SF Pro: a licença da Apple não permite usá-la num site.
- Pesos: 300 nos títulos grandes e números de destaque, 400 no corpo, 500 para ênfase e rótulos. Nada acima de 500.
- Números de dados (tabelas, contadores, CVSS, riscos) com algarismos tabulares (`font-variant-numeric: tabular-nums`).
- Escala: saudação 52px / 300 (40px no celular), com a data e a frase do mais urgente em 18px / `letter-spacing: -0.02em`; título de tela 32px / 300; título de seção 20px / 500; corpo 15px / 400 / `line-height: 1.5`; apoio 13px; legenda 12px.
- Números grandes (faixa da Início, riscos, ranking): peso 200–300, como o "10" fino de r6-01.
- Frases em português, com tom simples e direto. Botões dizem a ação ("Vincular", "Salvar ativo"). Sem ponto final em rótulos e títulos.

## 4. Ícones

Linha fina, traço uniforme, sem quadrado de fundo (r3-01). Conjunto único: Lucide, com os SVGs copiados para dentro do projeto. Tipos: notebook, servidor, roteador e impressora, cada um com um ícone fixo.

Ícones do menu, escolhidos pelo que cada tela faz:
- **Início:** mostrador (`gauge`)
- **Ativos:** monitor e celular (`monitor-smartphone`)
- **Vulnerabilidades:** inseto (`bug`)
- **Vínculos:** cabo (`cable`)
- **Ranking de riscos:** lista numerada (`list-ordered`)

## 5. Componentes-assinatura

### 5.1 Controle segmentado (duas variações, sem seletor aninhado)

As duas variações têm todas as opções com a mesma largura, ocupando quase toda a largura disponível. O cartão desliza até a opção escolhida com `transform: translateX`, em ~260–280ms, com `cubic-bezier(0.77, 0, 0.175, 1)`.

- **Padrão** (filtros e ordenação):
  - faixa `--campo` com raio ~12px e cartão branco com raio ~9px (cantos concêntricos) e sombra leve
  - na opção escolhida, texto `--tinta` peso 500; nas outras, texto `--texto-secundario`
- **Troca de modo** (Lista | Mapa, Por ativo | Por vulnerabilidade):
  - faixa `--campo` em pílula e cartão **preto** em pílula
  - só texto, sem ícone antes da palavra
  - na opção escolhida, texto **branco**; o texto nunca some sob o cartão: ele fica por cima, em branco
  - nas outras, texto em cinza (r7-01)

O GIF de segmentado aninhado ("Free / Premium") foi testado e rejeitado.

### 5.2 Contador

Usado para portas e RAM (r6-01):
- **Pílula:** inteira preta, com cerca de 58px de altura.
- **Sinais:** − e + finos e brancos, sempre visíveis.
- **Número:** branco, grande, peso 300, digitável direto no preto. Ao clicar, o número fica selecionado para digitar por cima. Não pode haver nenhuma caixa, fundo branco ou borda no meio.
- **Unidade:** "GB" fica fora da pílula, em cinza.
- **Ao pressionar:** os sinais encolhem para `scale(0.9)`.

### 5.3 Campos

- **Formato:** pílula `--campo`, sem borda (r4-01).
- **Foco:** contorno preto, nunca azul.
- **Menu suspenso** (setor, status): abre embaixo do campo, saindo dele (r4-02).
- **Escolher ativo ou vulnerabilidade:** menu com campo de busca no topo, em que cada item mostra o nome e o ID (r4-02).
- **Ajuda:** texto cinza embaixo da linha. Um ícone "i" com explicação ao passar o mouse aparece só em campos que exigem conceito (CVSS, fator de exposição, fração da dependência).

### 5.4 Campo de CVSS

- **Fundo:** muda para a cor do nível enquanto se digita (tabela da seção 2).
- **Número:** branco cheio, em negrito.
- **Ao lado:** só o nome do nível ("Crítico"), em peso 500, na cor do nível.
- **Sem régua de barras.**
- **Fora de 0,1 a 10:** o campo volta ao cinza e aparece a ajuda "Use de 0,1 a 10".

### 5.5 Botões

- **Principal:** pílula preta com texto branco.
- **Secundário:** pílula branca com contorno fino (r4-01).
- **Ao pressionar:** `scale(0.97)`.
- **Hover:** só dentro de `@media (hover: hover) and (pointer: fine)`.
- **Quantidade:** um botão principal por área.

### 5.6 Pílulas de status

- **Status do ativo:** a pílula fica neutra, só com contorno, contendo o texto e uma bolinha colorida. A pílula em si não é colorida.
- **Status de tratamento:** mesmo desenho. Clicar abre o menu para trocar o status ali mesmo.

### 5.7 Avisos

- **Excluir:** um balão sai do próprio botão Excluir: "Excluir Servidor web? Os vínculos e as dependências dele também serão removidos." Tem Cancelar e um botão Excluir vermelho (`#B42318`).
- **Desvincular:** o "x" de um vínculo abre o mesmo balão, saindo do próprio "x": "Desvincular Log4Shell de Servidor web? O status de tratamento deste vínculo será perdido." Tem Cancelar e um botão Desvincular vermelho. Só depois de confirmar o vínculo é apagado. Vale para a janela do ativo e para a tela de Vínculos.
- **Remover dependência:** o "x" de "Depende de" abre o mesmo balão: "Remover a dependência de Banco de dados? Servidor web deixará de depender deste ativo, e a fração 0,30 será perdida." Tem Cancelar e um botão Remover vermelho.
- **Foco depois de confirmar:** quando o item some (desvincular ou remover dependência), o foco vai para o "x" do item que ficou no lugar dele (o seguinte, ou o anterior se era o último). Se não sobrar nenhum, o foco vai para a janela ou para a tela.
- **Sucesso:** uma pílula preta sobe de baixo, perto do Cadastrar, com o texto "Ativo cadastrado", "Vulnerabilidade excluída" etc., e some sozinha em ~3s.
- **Erro da API:** faixa `#7A1414` com texto branco no topo do formulário, mostrando a mensagem de `{"erro": ...}`. O campo relacionado, quando dá para saber qual é, fica em destaque.

## 6. Navegação

### Desktop

- **Faixa de ícones:** sempre visível à esquerda, branca, com uma linha preta vertical marcando a tela ativa (r3-01).
- **Painel lateral:** a faixa abre um painel com os nomes das telas. O painel cobre a faixa e começa junto da borda esquerda da tela, sem espaço reservado para a faixa. O fundo da página fica atrás do `--veu`. Não há contadores.
- **Submenus do painel:** Ativos e Vulnerabilidades são grupos que começam fechados; clicar no nome abre as subopções logo abaixo, com uma linha fina à esquerda e uma seta que gira. Só um grupo fica aberto por vez. Início, Vínculos e Ranking de riscos têm uma tela só e continuam sendo links diretos.
  - **Ativos:** Lista de ativos, Cadastrar ativo e Mapa de grafos.
  - **Vulnerabilidades:** Lista de vulnerabilidades e Cadastrar vulnerabilidade.
  - **Tela atual:** o grupo dela fica em preto e peso 500, e a subopção dela ganha o fundo `--campo`. A lista também vale para as janelas de detalhes abertas por cima dela.
  - **Animação:** as subopções abrem e fecham em ~220ms com ease-out forte; com `prefers-reduced-motion`, a troca é direta. Fechadas, elas não recebem o foco do Tab.
- **Faixa de ícones:** continua com os links diretos para as 5 telas, sem submenus.
- **Cadastrar:**
  - pílula preta flutuando embaixo, no centro da tela, com um "+" num círculo branco
  - ao clicar, abre um balão que sai do botão, com "Novo ativo" e "Nova vulnerabilidade"
  - some nas telas de formulário (Novo ativo, Editar ativo, Nova vulnerabilidade e Editar vulnerabilidade), que já têm Salvar e Cancelar no topo
  - cada opção leva à tela de cadastro dela

### Celular

- **Botão do meio embaixo:** abre o menu lateral; dentro dele, Cadastrar aparece em destaque, com o círculo do "+" menor (24px) que no computador.
- **Layout:** uma coluna.
- **Janelas:** continuam sendo um cartão flutuante sobre o véu, como no computador, com uma margem pequena em volta (24px em cima e embaixo, 12px dos lados).

## 7. Telas

Rotas com `#`: `/#/`, `/#/ativos`, `/#/ativos/mapa`, `/#/ativos/<id>`, `/#/ativos/novo`, `/#/ativos/<id>/editar`, `/#/vulnerabilidades`, `/#/vulnerabilidades/<id>`, `/#/vulnerabilidades/novo`, `/#/vulnerabilidades/<id>/editar`, `/#/vinculos`, `/#/ranking`.

### 7.1 Início

Organização de desktop inspirada em r2-01 e r2-02: título grande à esquerda, números grandes soltos e gráficos finos.

- **Alinhamento:** a data, a saudação e a frase do mais urgente ficam alinhadas à esquerda, umas embaixo das outras. O resto (faixa de números, gráficos e mais urgentes) fica centralizado na página, com no máximo 1280px de largura: em notebooks comuns ele ocupa quase toda a largura e começa praticamente alinhado com a saudação.
- **Tamanhos:** números da faixa em 66px (56px entre 768 e 1200px de largura), rótulos em 17px, títulos de seção em 26px, meia lua com até 400px de largura e porcentagem em 58px, barras dos setores com 180px de altura e 14px de largura, nomes dos setores e legendas em 17px, e linhas dos mais urgentes com nome em 18px e número em 21px. No celular, os tamanhos voltam a ser menores.

1. **Data e saudação:** a data aparece pequena acima. A saudação é "Bom dia, Anakin" das 5h às 11h59, "Boa tarde, Anakin" das 12h às 17h59 e "Boa noite, Anakin" das 18h às 4h59, sempre no fuso `America/Sao_Paulo`.
2. **Frase do mais urgente:** uma frase curta logo abaixo, com o número em destaque. Exemplo: "**3** vulnerabilidades críticas abertas".
   - **Sem críticas abertas:** a frase desce para o nível mais grave que ainda tem abertas ("**2** vulnerabilidades altas abertas") e, uma linha abaixo, aparece "Nenhuma vulnerabilidade crítica aberta".
   - **Sem nenhuma aberta:** só "Nenhuma vulnerabilidade aberta".
3. **Faixa de números:** total de ativos, vulnerabilidades abertas, críticas abertas e ativos em manutenção, com divisórias finas. No celular, vira uma grade de 2 por 2.
   - **Contagem por vínculo:** as abertas e as críticas abertas contam cada vínculo (Log4Shell aberta em 3 servidores conta 3), igual à meia lua e aos setores.
4. **Meia lua dos vínculos:**
   - **Desktop:** arco fino dividido pelos 4 status de tratamento, com a porcentagem de corrigidas no centro e uma legenda com bolinhas embaixo.
   - **Celular:** só a porcentagem de corrigidas.
   - **Contagem:** é feita por vínculo (ativo × vulnerabilidade), não pelo catálogo.
5. **Setores:**
   - **Dados:** barras finas com a quantidade de vulnerabilidades críticas e altas não corrigidas em cada setor.
   - **Cores:** o pior setor em vermelho, o mais seguro em verde e os outros em cinza.
   - **Desempate:** não precisa de regra especial; com quantidades iguais, vale a ordem dos setores.
   - **Desenho:** barras verticais finas, da maior para a menor, com o número em cima e o nome do setor embaixo.
   - **Todos iguais:** quando todos os setores têm a mesma quantidade (por exemplo, todos com zero), nenhuma barra fica vermelha ou verde.
6. **Mais urgentes:** os 5 primeiros ativos do ranking de risco efetivo, nas mesmas linhas compactas do Ranking (posição, nome, barra e número), com o link "Ver ranking". Clicar num ativo abre os detalhes dele por cima da Início.
7. **Prévia do mapa:** fica solta no fundo, sem borda, no canto superior direito da página, saindo pela borda da tela e se apagando aos poucos em direção ao conteúdo (máscara de transparência, sem gradiente de cor). É um pedaço do próprio mapa, com a mesma posição das bolinhas, em 80% do tamanho e sem ícones nem nomes; mostra a parte mais cheia do mapa. Ao passar o mouse, o mapa chega 12px para a esquerda e aparece "Abrir o mapa". No celular, fica no fim da página, ocupando a largura toda. Ao clicar, o mapa é puxado para o centro (ease-in-out forte, até ~500ms) e vira `/#/ativos/mapa`: o desenho sai do lugar da prévia e cresce até o lugar dele na tela do mapa, enquanto o título e a legenda aparecem. Com `prefers-reduced-motion`, a troca é direta.
8. **Sem ranking (409):** os números, a meia lua e os setores continuam; em "Mais urgentes" aparece a mensagem da API, e a prévia fica sem as marcas dos maiores riscos.

Regra de "aberta" em todos os números: tudo que não está Corrigida (Aberta, Em tratamento e Aceita). Aceitar não elimina o risco.

### 7.2 Ativos: Lista

- **Linha de cada ativo** (estilo app): ícone do tipo à esquerda; nome; uma linha pequena com ID, tipo, responsável e setor; pílula de status; seta à direita. No celular, a pílula fica à direita da linha pequena, na mesma altura dela, e a linha pequena quebra quando não cabe.
- **Busca:** por nome.
- **Filtros:**
  - **Tipo:** pílulas com ícone e nome; a selecionada fica preenchida de preto.
  - **Status:** pílulas só com contorno, com a bolinha do status.
  - **Setor:** pílulas só com contorno, com o nome do setor. Como a API não filtra por setor, esse filtro é aplicado no JavaScript, em cima da resposta.
  - **Compartilhados:** a Lista e o Mapa usam os mesmos filtros (busca, tipo, status e setor). Trocar de Lista para Mapa mantém o que estiver escolhido.
  - **Ordenação:** segmentado padrão com ID | Nome | Vulnerabilidades, usando os parâmetros `ordenar=id|nome|vulnerabilidades` da API.
  - **No celular:** o nome do grupo (Tipo, Status e Setor) fica acima das pílulas, e as pílulas ficam menores (34px de altura, texto de 12px, ícone de 12px) para cada grupo caber numa linha só a partir de 390px de largura, sem rolar para o lado; em telas mais estreitas, o que não cabe desce para a linha seguinte. Vale também para o Mapa.
- **Troca Lista | Mapa:** segmentado de troca de modo, no topo.
- **Clique numa linha:** abre a janela de detalhes.

### 7.3 Ativos: Mapa

- **Filtros:** os mesmos da Lista (tipo, status e setor), sem a ordenação. O mapa mostra só os ativos que passam nos filtros e as dependências entre eles; a contagem vira "12 de 36 ativos".
- **Busca por nome:** mostra o ativo encontrado, com contorno preto, e todos os ativos ligados diretamente a ele (os de que ele depende e os que dependem dele), mesmo que não passem nos outros filtros, porque a busca serve para ver as dependências. Só as setas que tocam o ativo buscado aparecem.
- **Sem resultado:** "Nenhum ativo com esses filtros" com o botão "Limpar filtros".
- **Bolinhas e linhas:** cada bolinha é um ativo, limpa, com o ícone do tipo; as linhas são as dependências (seta de quem depende para o ativo do qual depende, com espessura leve proporcional à fração).
- **Tamanho:** cresce com o risco efetivo, mas com tamanho mínimo e máximo próximos (por exemplo, de 36px a 64px de diâmetro). A diferença é pequena de propósito.
- **Marca dos maiores riscos:** os 3 primeiros do ranking de risco efetivo ganham, no canto superior direito da bolinha, um círculo vermelho escuro (`--nivel-critico`, `#7A1414`) com a posição deles (1, 2 ou 3) em branco. Os outros ativos não têm marca: o tamanho da bolinha já mostra o risco.
  - **Por que não verde, amarelo e vermelho:** as bolinhas coloridas por terço do ranking foram testadas e retiradas, porque usavam as mesmas cores do status do ativo (Ativo, Em manutenção, Inativo) e pareciam mostrar o status.
  - **Risco zero:** um ativo com risco efetivo zero não recebe marca, mesmo estando entre os 3 primeiros.
- **Clique numa bolinha:** abre os detalhes do ativo, por cima do mapa.
- **Arrastar o mapa:** as bolinhas ficam fixas; o que se arrasta é o mapa todo. O mapa cresce com a quantidade de ativos (cerca de 190×190px de espaço por ativo no computador e 150×150px no celular) e, quando passa do tamanho da tela, arrastar o fundo mostra o resto. No computador o mapa cresce nas duas direções; no celular, só para os lados, e deslizar para cima ou para baixo continua rolando a página. Um arrasto que começa em cima de uma bolinha não abre o ativo. Com o teclado, focar uma bolinha fora da tela leva o mapa até ela. A dica "Arraste o fundo do mapa para ver o resto" só aparece quando dá para arrastar.
- **Desenho:** SVG próprio com um layout de forças simples, sem biblioteca externa. O cálculo não usa sorteio, então a prévia da Início e o mapa saem iguais. As posições seguem a proporção do mapa (que depende da tela e da quantidade de ativos). As setas ficam em `--estado-cinza`, mais claras que os nomes. O desenho é centralizado sem ser esticado: um mapa cheio ocupa o espaço todo, e um grupo pequeno (como o resultado de uma busca) fica junto no meio, com cerca de 200px entre as bolinhas.
- **Nomes:** embaixo de cada bolinha, com um contorno da cor do fundo para as setas não cortarem o texto.
- **Legenda:** embaixo do mapa, explica o tamanho, a marca dos 3 maiores riscos e o sentido das setas.
- **Sem ranking (409):** aparece a mensagem da API acima do mapa, e as bolinhas ficam do mesmo tamanho e sem a marca dos maiores riscos.

### 7.4 Janelas de detalhes

- **Posição:** centralizadas, estilo janela do macOS, sobre o `--veu`.
- **Como fechar:** Esc, clique fora, "x" ou o botão Voltar do navegador (a janela tem rota própria).
- **Navegação interna:** não existe janela dentro de janela. Clicar numa vulnerabilidade dentro dos detalhes do ativo troca o conteúdo na mesma janela, com uma seta de voltar.
- **Botões:** Editar e Excluir ficam no canto superior direito, ao lado do nome. No celular, continuam na mesma linha do nome, só com os ícones (lápis e lixeira, 44px), e o nome fica em 24px; o leitor de tela continua lendo "Editar" e "Excluir".

**Detalhes do ativo:**
- **Topo:** nome grande; tipo, setor e responsável pequenos embaixo.
- **Ficha:** logo abaixo, numa linha pequena em cinza, a pílula de status do ativo, o fator de exposição e os campos do tipo (ex.: "32 GB de RAM", "4 TB de armazenamento").
- **Risco:** três números soltos (próprio, herdado e efetivo), em peso leve, cada um com o seu rótulo centralizado embaixo. Trocar o status de um vínculo ou desvincular recalcula os números ao vivo (seção 8).
- **Vulnerabilidades vinculadas:** bolinha e nome do nível, nome, CVSS e pílula de status de tratamento, que pode ser trocada ali mesmo. Cada uma tem um "x" para desvincular, que pede confirmação no balão (seção 5.7). O nome é um link que abre os detalhes da vulnerabilidade na mesma janela, com a seta de voltar. Sem vulnerabilidades, aparece o botão "Vincular vulnerabilidade", que abre a tela de Vínculos com o ativo já escolhido (`/#/vinculos?ativo=<id>`).
- **Colunas alinhadas:** o CVSS e a pílula de status ficam em colunas de largura fixa, para as pílulas se alinharem de uma linha para outra.
- **Dependências:**
  - **Mini mapa:** só dos vizinhos. Quem depende do ativo fica à esquerda e os ativos dos quais ele depende ficam à direita, com as setas indo da esquerda para a direita. Clicar num vizinho abre os detalhes dele na mesma janela, com a seta de voltar.
  - **Muitos vizinhos:** cada lado mostra até 6 vizinhos; quando há mais, o 7º lugar vira uma bolinha cinza "+N outros". As listas logo abaixo continuam mostrando todos.
  - **Listas:** "Dependem dele" à esquerda e "Depende de" à direita, na mesma ordem do mini mapa, cada item com o ícone do tipo, o nome e a fração.
  - **Adicionar:** o botão "Adicionar dependência" abre uma linha ali mesmo, com o menu com busca do ativo, o controle deslizante da fração e o aviso "A fração precisa ser menor que 0,3" (o valor restante é calculado).
  - **Remover:** cada item de "Depende de" tem um "x" para remover a dependência, que pede confirmação no balão (seção 5.7). A fração não é editada na janela.

**Detalhes da vulnerabilidade:**
- **Topo:** nome grande; CVSS e nível em destaque.
- **Afetados agora:** os ativos com status Aberta, Em tratamento ou Aceita, cada um com o seu status.
- **Já corrigida em:** os ativos com status Corrigida, em `--texto-apagado`.
- **Clique num ativo:** abre os detalhes dele.

### 7.5 Vulnerabilidades

- **Lista:** cada linha tem ID, nome, CVSS e a bolinha do nível, com o nome do nível na cor dele, na ordem do ID. No celular: nome e ID em cima, e embaixo o nível à esquerda e o CVSS à direita, na mesma linha.
- **Clique:** abre a janela de detalhes.
- **Formulário:** Nome e o campo de CVSS (seção 5.4). O ID é criado pelo sistema, então não há campo de ID. Depois de salvar, abre a janela da vulnerabilidade salva, igual aos ativos.

### 7.6 Vínculos

- **Topo:** uma linha para criar o vínculo, com ativo (menu com busca), vulnerabilidade (menu com busca), status (menu) e o botão preto "Vincular".
- **Agrupamento:** segmentado de troca de modo "Por ativo | Por vulnerabilidade", que abre em "Por ativo".
- **Cada item:** bolinha de gravidade, nome, CVSS, pílula de status (troca ali mesmo) e um "x" para desvincular, que pede confirmação no balão (seção 5.7).
- **Por ativo:** um grupo por ativo que tem vínculos, com o ícone e o nome do ativo no topo; dentro, as vulnerabilidades da mais grave para a menos grave.
- **Por vulnerabilidade:** um grupo por vulnerabilidade, da mais grave para a menos grave, com a bolinha, o nome, o CVSS e a quantidade de ativos no topo; dentro, cada ativo com o ícone do tipo, o nome, a pílula de status e o "x".
- **Validação:** ativo e vulnerabilidade são obrigatórios, e o vínculo repetido é avisado antes de chamar a API ("Esta vulnerabilidade já está vinculada a este ativo."). O status começa em Aberta.
- **Sem ativos ou sem vulnerabilidades:** no lugar da linha de criação, aparece o aviso "Para vincular, cadastre pelo menos um ativo e uma vulnerabilidade." com os botões do que falta.

### 7.7 Ranking de riscos

- **Linha:** a posição bem grande à esquerda, como peça tipográfica; o nome com o ícone do tipo; uma barra horizontal com o risco próprio em preto e o herdado em cinza (o comprimento total é o efetivo); e o número do efetivo.
- **Destaque:** os 3 primeiros têm nome e barra maiores, com o nome, o ícone do tipo e o número do risco efetivo em vermelho escuro (`--nivel-critico`, `#7A1414`), em todos os tamanhos de tela, e o resto da lista fica mais compacto embaixo.
- **Escala:** a barra usa o maior risco efetivo como 100%.
- **Legenda:** no topo, à direita: "Risco próprio" (preto), "Risco herdado" (cinza) e "Número: risco efetivo".
- **Clique numa linha:** abre os detalhes do ativo por cima do Ranking.
- **Celular:** a posição fica à esquerda, o nome e o número na primeira linha e a barra embaixo, ocupando a largura toda.
- **Sem ranking (409):** a mensagem da API com o botão "Tentar de novo".

### 7.8 Formulários: Novo ativo, Nova vulnerabilidade e Editar

São telas normais, não janelas.

- **Estilo:** Ajustes do macOS, com linhas agrupadas, o nome do campo à esquerda e o valor à direita.
- **Botões:** Salvar (pílula preta) e Cancelar (contorno) no topo, à direita, sempre visíveis.
- **Tipo do ativo:**
  - **Escolha:** quatro blocos com ícone, lado a lado (r1-01).
  - **Ao escolher:** os outros blocos perdem opacidade, e os campos próprios do tipo aparecem abaixo.
- **Campos próprios de cada tipo:**
  - **Contador:** portas e RAM.
  - **Campo de número comum:** velocidade, tela e armazenamento.
- **Fator de exposição:** controle deslizante de 0 a 2, começando no padrão do tipo (o valor vem de `/opcoes`), com o número ao lado.
- **Setor e status:** menu que abre embaixo do campo.
- **ID do ativo:** no Novo ativo, campo vazio e obrigatório, preenchido pelo usuário (número inteiro maior que zero), sem sugestão pronta. Se o ID já existir, a mensagem da API aparece na faixa vermelha e o campo fica em destaque. No Editar, o ID aparece só como texto, embaixo do título.
- **Validação:** o formulário evita erros antes de enviar (`required`, faixas de valor, opções vindas de `/opcoes`), com as mesmas mensagens do domínio. Cada campo com erro mostra a mensagem embaixo dele, e o erro some assim que o campo é alterado. O erro da API aparece na faixa vermelha (5.7).
- **Editar:** usa a mesma tela, já preenchida. Ao trocar o tipo, o fator volta ao padrão do tipo novo, que é a mesma regra do menu do terminal.
- **Depois de salvar:** volta para a lista de ativos com a janela de detalhes do ativo salvo aberta por cima, e o aviso de sucesso sobe ("Ativo cadastrado" ou "Ativo atualizado").
- **Cancelar:** volta para a tela anterior (a lista ou a janela do ativo).

## 8. Animação

Valores das skills emil-design-eng e animate:
- **Quando animar:** só em resposta a uma ação, ou seja, ao abrir o balão do Cadastrar, os menus suspensos, as janelas e o menu lateral, ao mover o cartão do segmentado, ao puxar o mapa para o centro, ao mostrar o aviso de sucesso e ao recontar os números de risco.
- **Números de risco ao vivo:** quando o status de um vínculo muda ou uma vulnerabilidade é desvinculada, os números de risco contam rapidinho até o valor novo, subindo ou descendo (~450ms, saída suave, algarismos tabulares). Ao abrir a tela ou a janela, o número já aparece pronto, sem contar a partir do zero. Com `prefers-reduced-motion`, o número só troca.
- **Balões e menus suspensos:**
  - **Origem:** saem do botão que os abriu (`transform-origin` no botão).
  - **Movimento:** de `scale(0.95)` com `opacity: 0` até o tamanho normal, em 150–250ms, com `cubic-bezier(0.23, 1, 0.32, 1)`.
- **Janelas:** centralizadas; abrem de `scale(0.97)` com `opacity: 0`, em ~220ms, com ease-out forte. O véu aparece junto.
- **Movimentos na tela** (segmentado e mapa): `cubic-bezier(0.77, 0, 0.175, 1)`.
- **Propriedades:** só `transform` e `opacity`, além de `backdrop-filter` no véu. Nunca `transition: all`, nunca `scale(0)` e nunca `ease-in`.
- **Movimento reduzido:** com `prefers-reduced-motion`, ficam só as transições de opacidade.
- **Sem animação de entrada** em seções ao carregar a página.

## 9. Responsivo

Larguras de referência: 1440, 1024, 768 e 390px.
- **Desktop:** a Início usa várias colunas (a meia lua ao lado das barras de setores; a prévia do mapa solta no canto).
- **Abaixo de 768px:** uma coluna, menu pelo botão do meio, janelas como cartão flutuante e meia lua só com a porcentagem.
- **Títulos de tela no celular:** 44px, com a contagem embaixo ("36 ativos") em 20px e um respiro maior no topo da página.
- **Toque:** áreas de toque com pelo menos 44px no celular. Exceção pedida pelo Cadu: as pílulas de filtro têm 34px, para cada grupo caber numa linha só (o mínimo do WCAG é 24px).
- **Janelas no celular:** o cartão nunca passa da altura da tela e rola por dentro, do topo até a última seção.
- **Detalhes no celular:** os três números de risco ficam lado a lado em 32px, e os nomes das vulnerabilidades quebram de linha em vez de serem cortados.

## 10. API usada (não muda)

- `GET /saude`
- `GET /opcoes`: tipos com o fator padrão; setores; status do ativo; status de tratamento; cores; tecnologias.
- `GET /ativos?tipo=&status=&nome=&ordenar=id|nome|vulnerabilidades` · `POST /ativos` · `GET /ativos/<id>` · `PUT /ativos/<id>` · `DELETE /ativos/<id>`
- `GET /ativos/<id>/vulnerabilidades` · `POST /ativos/<id>/vulnerabilidades` · `PUT /ativos/<id>/vulnerabilidades/<id_vuln>` · `DELETE /ativos/<id>/vulnerabilidades/<id_vuln>`
- `GET /ativos/<id>/dependencias` · `POST /ativos/<id>/dependencias` · `PUT /ativos/<id>/dependencias/<id_dep>` · `DELETE /ativos/<id>/dependencias/<id_dep>`
- `GET /vulnerabilidades` · `POST /vulnerabilidades` · `GET /vulnerabilidades/<id>` (com `nivel`) · `PUT /vulnerabilidades/<id>` · `DELETE /vulnerabilidades/<id>`
- `GET /riscos`: ranking com `risco_proprio`, `risco_herdado` e `risco_efetivo`; devolve 409 se os dados impedem a análise.
- **Erros:** sempre `{"erro": "..."}`, com 400, 404, 405 ou 500.

As contas da Início (setores, meia lua, faixa de números) são feitas no JavaScript, a partir dessas rotas.
