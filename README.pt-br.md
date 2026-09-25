📄 **README.pt-br.md**

# Gerenciador de Ativos e Vulnerabilidades de TI

*[Read in English](./README.md)*

Aplicação de linha de comando (CLI) em Python para cadastro e gerenciamento de ativos de TI e suas respectivas vulnerabilidades de segurança. Desenvolvido como projeto de estudo do curso de Cibersegurança, aplicando boas práticas de código (nomenclatura clara, funções com responsabilidade única, separação entre regras de negócio e entrada/saída, tratamento de erros sem exposição de dados internos).

## ✨ Funcionalidades

### Ativos
- **Cadastro**: ID, nome, categoria (Notebook / Servidor / Roteador / Impressora), setor (TI / Financeiro / Marketing / RH / Jurídico), responsável e status (Ativo / Inativo / Em manutenção), com validação de entradas
- **Listagem**: exibe todos os ativos cadastrados, ou busca por **ID** ou **nome/hostname** (busca parcial, case-insensitive)
- **Edição**: atualiza responsável, status, setor ou categoria
- **Exclusão**: remove um ativo pelo ID

### Vulnerabilidades
- **Cadastro**: descrição, tipo (texto livre), severidade (Baixo / Médio / Alto) e status de tratamento (Aberta / Em tratamento / Corrigida / Aceita)
- **Listagem**: exibe todas as vulnerabilidades, ou filtra por ativo
- **Exclusão**: remove uma vulnerabilidade de um ativo pelo nome

### Geral
- **Persistência de dados**: os dados são salvos automaticamente em um arquivo `ativos.json` e recarregados a cada execução
- **Tratamento de erro global**: Ctrl+C e Ctrl+D em qualquer ponto do programa encerram de forma limpa, sem traceback

## 🫧 Tecnologias

- Python 3.8+
- Módulos da biblioteca padrão: `json`, `enum`

## ✨ Estrutura do projeto

```
.
├── main code s1.py
├── funcoes_s1.py
├── testes.py
├── docs/
│   ├── requisitos.md
│   ├── validacoes.md
│   ├── criterios_aceitacao.md
│   ├── especificacao.md
│   └── relatorio_testes.md
├── .gitignore
├── README.md
└── README.pt-br.md
```

> O arquivo `ativos.json` (dados salvos) é gerado automaticamente na primeira execução e não é versionado.

## 🫧 Como executar

Pré-requisito: Python 3.8 ou superior instalado.

```
git clone https://github.com/cadulugaresi/it-asset-vulnerability-manager.git
cd it-asset-vulnerability-manager
python "main code s1.py"
```

O programa abre um menu interativo no terminal. Basta seguir as opções numeradas para cadastrar ativos, gerenciar vulnerabilidades e salvar os dados.

✨ Menu principal

MENU
1 - Cadastrar ativo
2 - Listar ativos
3 - Excluir ativo
4 - Editar vulnerabilidades
5 - Editar ativo
6 - Sair

Dentro da opção 4 (Editar vulnerabilidades), um submenu permite listar, adicionar e remover vulnerabilidades de um ativo específico.

Dentro da opção 5 (Editar ativo), um submenu permite atualizar responsável, status, setor ou categoria de um ativo.

🫧 Status do projeto

Projeto em desenvolvimento incremental (por sprints) durante minhas primeiras semanas na graduação em Cibersegurança na Universidade Federal de Uberlândia, com foco em:

Nomenclatura clara e expressiva
Funções com responsabilidade única
Separação entre regras de negócio e entrada/saída
Tratamento de erros sem exposição de dados internos
Validação de entradas do usuário

✨ Política de Exclusão

O sistema adota **exclusão física**: ao remover um ativo, o registro é apagado permanentemente do arquivo `ativos.json`, junto com suas vulnerabilidades associadas.

**Justificativa:**
- O escopo do projeto não exige auditoria ou histórico de remoções;
- Manter registros deletados aumentaria a complexidade sem benefício claro;
- O usuário deve confirmar a exclusão antes de removê-la (mitigação de remoção acidental).

**Exclusão lógica** (marcar como inativo em vez de apagar) foi considerada, mas descartada por não estar no escopo do Trabalho 1.

🫧 Licença

Projeto de estudo, livre para uso educacional.