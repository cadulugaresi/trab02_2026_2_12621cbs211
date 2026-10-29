# Gerenciador de Ativos e Vulnerabilidades de TI

*[Read in English](../README.md)*

Aplicação CLI em Python para cadastro e gestão de ativos de TI e suas vulnerabilidades, com análise de risco baseada em álgebra linear (em desenvolvimento). Projeto de estudo do curso de Cibersegurança da UFU, com foco em boas práticas de código: nomenclatura clara, funções com responsabilidade única, separação entre regras de negócio e entrada/saída, programação orientada a objetos e tratamento de erros sem exposição de dados internos.

## ✨ Funcionalidades

### Ativos
Cada tipo de ativo é uma **subclasse própria** de `Ativo`, com atributos específicos:

- **Notebook**: sistema operacional, tamanho de tela
- **Servidor**: quantidade de RAM, armazenamento
- **Roteador**: quantidade de portas, velocidade
- **Impressora**: cor (colorida / preto e branco), tecnologia (tinta / laser)

**Operações disponíveis:**
- **Cadastro**: ID, nome, tipo, setor (TI / Financeiro / Marketing / RH / Jurídico), responsável, status (Ativo / Inativo / Em manutenção) e atributos específicos do tipo escolhido, todos com validação de entradas.
- **Listagem**: permite exibir todos os ativos, buscar por **ID**, por **nome/hostname** (busca parcial, case-insensitive) ou por **tipo** (busca parcial, case-insensitive).
- **Edição**: atualiza responsável, status, setor e atributos específicos
- **Exclusão**: remove um ativo pelo ID, com confirmação antes da exclusão

### Vulnerabilidades
As vulnerabilidades ficam em um **catálogo** único, independente dos ativos. Cada ativo guarda apenas uma **referência** (o ID da vulnerabilidade) e o **status de tratamento** daquela vulnerabilidade nele. Assim, uma mesma vulnerabilidade pode estar aberta em um ativo e corrigida em outro, e corrigir seus dados no catálogo atualiza todos os ativos vinculados de uma vez.

- **Cadastro no catálogo**: nome e **nota CVSS** (de 0.1 a 10.0, aceitando vírgula como separador decimal e arredondada para uma casa), com ID gerado automaticamente
- **Nível de severidade**: calculado a partir da nota CVSS pelas faixas oficiais (Baixo / Médio / Alto / Crítico), então nunca contradiz a nota
- **Vínculo**: liga uma vulnerabilidade do catálogo a um ativo, com status de tratamento (Aberta / Em tratamento / Corrigida / Aceita)
- **Listagem**: exibe o catálogo inteiro, ou as vulnerabilidades de um ativo com o status de cada uma nele
- **Atualização de status**: muda o status de tratamento de uma vulnerabilidade em um ativo específico
- **Desvínculo**: tira uma vulnerabilidade de um ativo, mantendo-a no catálogo
- **Edição no catálogo**: corrige o nome ou a nota CVSS
- **Exclusão do catálogo**: remove uma vulnerabilidade do catálogo e de todos os ativos vinculados, com confirmação

> **Em desenvolvimento:** integração com o CVE para identificação de vulnerabilidades conhecidas.

### Análise de Risco (em desenvolvimento)
Modelo baseado em álgebra linear que estima o risco de cada ativo a partir de suas vulnerabilidades e das dependências entre ativos. O catálogo e os vínculos são a base da matriz de incidência `M` e do vetor de severidade `v`, usados para calcular o risco próprio de cada ativo (`b = Mv`).

### Geral
- **Persistência de dados**: os ativos e seus vínculos são salvos em `ativos.json`, e o catálogo em `vulnerabilidades.json`, ambos como lista de objetos JSON, e recarregados a cada execução
- **Índice por ID**: ativos e vulnerabilidades do catálogo são armazenados em dicionários indexados por ID, permitindo busca eficiente e em tempo constante (O(1))
- **Tratamento de erro global**: Ctrl+C e Ctrl+D em qualquer ponto do programa encerram de forma limpa, sem traceback

## 🫧 Tecnologias

- Python 3.8+
- Módulos da biblioteca padrão: `json`, `enum`
- Testes: `unittest` e `pytest`; padronização: `flake8` e `black`; integração contínua com GitHub Actions
- **Em desenvolvimento**: biblioteca de álgebra linear (a definir), Docker

## ✨ Arquitetura

- **Hierarquia de classes**: `Ativo` (base) + `Notebook`, `Servidor`, `Roteador`, `Impressora` (subclasses)
- **Polimorfismo**: cada subclasse sobrescreve `exibir_detalhes()` e adiciona seus atributos específicos
- **Catálogo de vulnerabilidades**: objetos `Vulnerabilidade` guardados no dicionário `catalogo[id]`; cada ativo mantém um dicionário de vínculos `{id_vulnerabilidade: StatusDaVuln}` (referência, não cópia)
- **Nível calculado**: `Vulnerabilidade.nivel()` obtém o nível de severidade a partir da nota CVSS
- **Serialização / desserialização**: `para_dicionario()` converte objetos em dicionários; `de_dicionario()` (método de classe) reconstrói objetos a partir de dicionários
- **Índice por ID**: dicionários `ativos[id]` e `catalogo[id]` para busca O(1)
- **Separação de responsabilidades**: as funções que alteram dados (ex.: `vincular_vulnerabilidade()`) apenas validam e levantam `DadoInvalidoError`, enquanto o menu cuida de toda a interação com o usuário; funções puras (ex.: `listar_ativos_por_tipo()`) ficam separadas da camada de I/O

## ✨ Estrutura do projeto

```
.
├── main.py
├── inventario/
│   ├── enums.py
│   ├── excecoes.py
│   ├── validacoes.py
│   ├── entradas.py
│   ├── persistencia.py
│   ├── modelos/
│   │   ├── ativo.py
│   │   └── vulnerabilidade.py
│   └── operacoes/
│       ├── ativos.py
│       └── vulnerabilidades.py
├── tests/
│   ├── testes.py
│   ├── test_vulnerabilidades.py
│   └── test_exemplos.py
├── docs/
│   ├── README.pt-br.md
│   ├── requisitos.md
│   ├── validacoes.md
│   ├── criterios_aceitacao.md
│   ├── especificacao.md
│   ├── relatorio_testes.md
│   └── entrega_final.md
├── .github/workflows/testes.yml
├── .flake8
├── pyproject.toml
├── .gitignore
└── README.md
```

> Os arquivos de dados `ativos.json` e `vulnerabilidades.json` são gerados automaticamente na primeira execução e não são versionados.

## 🫧 Como executar

Pré-requisito: Python 3.8 ou superior instalado.

```bash
git clone https://github.com/cadulugaresi/it-asset-vulnerability-manager.git
cd it-asset-vulnerability-manager
python3 main.py
```

> No Windows, use `python` no lugar de `python3`.

O programa abre um menu interativo no terminal. Basta seguir as opções numeradas para cadastrar ativos, gerenciar vulnerabilidades e salvar os dados.

### Menu principal

```
1 - Cadastrar ativo
2 - Listar ativo
3 - Excluir ativo
4 - Menu de vulnerabilidades
5 - Editar ativo
6 - Sair
```

Dentro da opção 4 (Menu de vulnerabilidades), um submenu gerencia o catálogo e os vínculos entre vulnerabilidades e ativos:

```
1 - Cadastrar vulnerabilidade
2 - Listar catálogo de vulnerabilidades
3 - Vincular vulnerabilidade a um ativo
4 - Listar vulnerabilidades de um ativo
5 - Atualizar status da vulnerabilidade em um ativo
6 - Desvincular vulnerabilidade de um ativo
7 - Excluir vulnerabilidade do catálogo
8 - Editar vulnerabilidade no catálogo
9 - Voltar ao menu principal
```

Dentro da opção 5 (Editar ativo), um submenu permite atualizar responsável, status, setor ou atributos específicos de um ativo.

### Rodando os testes

```bash
python3 -m unittest tests/testes.py tests/test_vulnerabilidades.py
python3 -m pytest tests/test_exemplos.py
python3 -m flake8 main.py inventario
```

## ✨ Política de Exclusão

O sistema adota **exclusão física**:
- Ao remover um **ativo**, o registro é apagado permanentemente do arquivo `ativos.json`, junto com seus vínculos. As vulnerabilidades em si continuam no catálogo.
- Ao remover uma **vulnerabilidade** do catálogo, ela é apagada permanentemente do arquivo `vulnerabilidades.json` e desvinculada de todos os ativos, para que nenhum ativo fique apontando para uma vulnerabilidade que não existe mais.

**Justificativa:**
- O escopo do projeto não exige auditoria ou histórico de remoções;
- Manter registros deletados aumentaria a complexidade sem benefício claro;
- O usuário deve confirmar a exclusão antes de removê-la (mitigação de remoção acidental).

**Exclusão lógica** (marcar como inativo em vez de apagar) foi considerada, mas descartada por não estar no escopo.

## ✅ Requisitos atendidos

### Trabalho 1 (Sprints 1 e 2)
- [x] Classes representam entidades do domínio
- [x] Funções com responsabilidade única
- [x] Regras de negócio separadas da entrada/saída
- [x] Persistência em JSON
- [x] Índice por ID (busca O(1))
- [x] Branches e merge no Git

## ✅ Requisitos do Trabalho 2

| # | Requisito | Status |
|---|---|---|
| 1 | Ativos como objetos individuais (subclasses) | ✅ |
| 2 | Persistência em JSON | ✅ |
| 3 | Execução em container Docker | ⏳ |
| 4 | Cálculo de risco (álgebra linear) | ⏳ |

## 🫧 Licença

Projeto de estudo, livre para uso educacional.