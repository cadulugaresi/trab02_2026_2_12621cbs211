# IT Asset & Vulnerability Manager

*[Ler em português](./README.pt-br.md)*

A command-line (CLI) application in Python for registering and managing IT assets and their associated security vulnerabilities, with risk analysis based on linear algebra (in development). Built as a study project for a Cybersecurity course at UFU, applying clean code practices: expressive naming, single-responsibility functions, separation between business rules and I/O, object-oriented programming, and error handling that doesn't leak internal details.

## ✨ Features

### Assets
Each asset type is a **subclass** of `Ativo`, with its own specific attributes:

- **Notebook**: operating system, screen size
- **Server**: RAM amount, storage
- **Router**: number of ports, speed
- **Printer**: color (color / black and white), technology (inkjet / laser)

**Available operations:**
- **Registration**: ID, name, type, department (IT / Finance / Marketing / HR / Legal), owner, status (Active / Inactive / Under maintenance), and type-specific attributes, all with input validation.
- **Listing**: view all assets, or search by **ID**, by **name/hostname** (partial, case-insensitive), or by **type** (partial, case-insensitive).
- **Editing**: update owner, status, department, and type-specific attributes.
- **Deletion**: remove an asset by ID, with confirmation before deletion.

### Vulnerabilities
- **Registration**: description/name, type (free text), severity (Low / Medium / High), and treatment status (Open / In treatment / Fixed / Accepted)
- **Listing**: view all vulnerabilities, or filter by asset
- **Deletion**: remove a vulnerability from an asset by name

> **In development:** integration with industry-standard classifications (CVSS for severity, CVE for identifying known vulnerabilities).

### Risk Analysis (in development)
Model based on linear algebra that estimates the risk of each asset from its vulnerabilities and dependencies between assets.

### General
- **Data persistence**: data is automatically saved to an `ativos.json` file and reloaded on every run
- **ID index**: assets are stored in a dictionary indexed by ID, allowing efficient constant-time search (O(1))
- **Global error handling**: Ctrl+C and Ctrl+D anywhere in the program exit cleanly, without a traceback

## 🫧 Tech Stack

- Python 3.8+
- Standard library modules: `json`, `enum`
- **In development**: linear algebra library (TBD), Docker

## ✨ Architecture

- **Class hierarchy**: `Ativo` (base) + `Notebook`, `Servidor`, `Roteador`, `Impressora` (subclasses)
- **Polymorphism**: each subclass overrides `exibir_detalhes()` and adds its own specific attributes
- **Serialization / deserialization**: `para_dicionario()` converts objects to dictionaries; `de_dicionario()` (class method) rebuilds objects from dictionaries
- **ID index**: `ativos[id]` dictionary for O(1) search
- **Separation of responsibilities**: pure functions (e.g., `filtrar_ativos_por_tipo`) separated from the I/O layer

## ✨ Project Structure
.
├── main_code_t2.py
├── funcoes_s1.py
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

> The `ativos.json` file (saved data) is generated automatically on first run and is not version-controlled.

## 🫧 Getting Started

Requirement: Python 3.8 or higher installed.

git clone https://github.com/cadulugaresi/it-asset-vulnerability-manager.git
cd it-asset-vulnerability-manager
python main_code_t2.py

The program opens an interactive menu in the terminal. Follow the numbered options to register assets, manage vulnerabilities, and persist data.

### Main menu

1 - Cadastrar ativo
2 - Listar ativos
3 - Excluir ativo
4 - Editar vulnerabilidades
5 - Editar ativo
6 - Sair

Inside option 4 (Editar vulnerabilidades), a submenu lets you list, add, and remove vulnerabilities for a specific asset.

Inside option 5 (Editar ativo), a submenu lets you update the owner, status, department, or type-specific attributes of an asset.

## ✨ Deletion Policy

The system uses **physical deletion**: when an asset is removed, the record is permanently erased from `ativos.json`, along with its associated vulnerabilities.

**Rationale:**
- The project scope does not require audit or removal history;
- Keeping deleted records would increase complexity without clear benefit;
- The user must confirm deletion before removal (mitigation against accidental deletion).

**Logical deletion** (marking as inactive instead of erasing) was considered but discarded as it is outside the project scope.

## ✅ Requirements Met

### Assignment 1 (Sprints 1 and 2)
- [x] Classes represent domain entities
- [x] Single-responsibility functions
- [x] Business rules separated from I/O
- [x] JSON persistence
- [x] ID index (O(1) search)
- [x] Git branches and merge

## ✅ Assignment 2 Requirements

| # | Requirement | Status |
|---|---|---|
| 1 | Assets as individual objects (subclasses) | ✅ |
| 2 | JSON persistence | ✅ |
| 3 | Docker container execution | ⏳ |
| 4 | Risk calculation (linear algebra) | ⏳ |

## 🫧 License

Study project, free to use for educational purposes.