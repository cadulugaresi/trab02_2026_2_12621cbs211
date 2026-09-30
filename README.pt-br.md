# Gerenciador de Ativos e Vulnerabilidades de TI

*[Read in English](./README.md)*

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
- **Cadastro**: descrição/nome, tipo (texto livre), severidade (Baixo / Médio / Alto) e status de tratamento (Aberta / Em tratamento / Corrigida / Aceita)
- **Listagem**: exibe todas as vulnerabilidades, ou filtra por ativo
- **Exclusão**: remove uma vulnerabilidade de um ativo pelo nome

> **Em desenvolvimento:** integração com classificações padrão do setor (CVSS para severidade, CVE para identificação de vulnerabilidades conhecidas).

### Análise de Risco (em desenvolvimento)
Modelo baseado em álgebra linear que estima o risco de cada ativo a partir de suas vulnerabilidades e das dependências entre ativos. Detalhes na seção [Roadmap](#-roadmap).

### Geral
- **Persistência de dados**: os dados são salvos automaticamente em um arquivo `ativos.json` e recarregados a cada execução
- **Índice por ID**: ativos são armazenados em um dicionário indexado por ID, permitindo busca eficiente e em tempo constante (O(1))
- **Tratamento de erro global**: Ctrl+C e Ctrl+D em qualquer ponto do programa encerram de forma limpa, sem traceback

## 🫧 Tecnologias

- Python 3.8+
- Módulos da biblioteca padrão: `json`, `enum`
- **Em desenvolvimento**: biblioteca de álgebra linear (a definir), Docker

## ✨ Arquitetura

- **Hierarquia de classes**: `Ativo` (base) + `Notebook`, `Servidor`, `Roteador`, `Impressora` (subclasses)
- **Polimorfismo**: cada subclasse sobrescreve `exibir_detalhes()` e adiciona seus atributos específicos
- **Serialização / desserialização**: `para_dicionario()` converte objetos em dicionários; `de_dicionario()` (método de classe) reconstrói objetos a partir de dicionários
- **Índice por ID**: dicionário `ativos[id]` para busca O(1)
- **Separação de responsabilidades**: funções puras (ex: `filtrar_ativos_por_tipo`) separadas da camada de I/O

## ✨ Estrutura do projeto
.
├── main_code_t2.py
├── funcoes_t2.py
├── testes.py
├── docs/
│ ├── requisitos.md
│ ├── validacoes.md
│ ├── criterios_aceitacao.md
│ ├── especificacao.md
│ └── relatorio_testes.md
├── .gitignore
├── README.md
└── README.pt-br.md

> O arquivo `ativos.json` (dados salvos) é gerado automaticamente na primeira execução e não é versionado.

## 🫧 Como executar

Pré-requisito: Python 3.8 ou superior instalado.
git clone https://github.com/cadulugaresi/it-asset-vulnerability-manager.git
cd it-asset-vulnerability-manager
python main_code_t2.py

O programa abre um menu interativo no terminal. Basta seguir as opções numeradas para cadastrar ativos, gerenciar vulnerabilidades e salvar os dados.

### Menu principal

1 - Cadastrar ativo
2 - Listar ativos
3 - Excluir ativo
4 - Editar vulnerabilidades
5 - Editar ativo
6 - Sair

Dentro da opção 4 (Editar vulnerabilidades), um submenu permite listar, adicionar e remover vulnerabilidades de um ativo específico.

Dentro da opção 5 (Editar ativo), um submenu permite atualizar responsável, status, setor ou atributos específicos de um ativo.

## ✨ Política de Exclusão

O sistema adota **exclusão física**: ao remover um ativo, o registro é apagado permanentemente do arquivo `ativos.json`, junto com suas vulnerabilidades associadas.

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