# IT Asset & Vulnerability Manager

*[Ler em português](./docs/README.pt-br.md)*

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
Vulnerabilities live in a single **catalog**, independent of the assets. Each asset stores only a **reference** (the vulnerability ID) and the **treatment status** of that vulnerability on that specific asset. This way, the same vulnerability can be open on one asset and fixed on another, and correcting its data in the catalog updates every linked asset at once.

- **Catalog registration**: name and **CVSS score** (0.1 to 10.0, accepting a comma as the decimal separator and rounded to one decimal place), with an automatically generated ID
- **Severity level**: calculated from the CVSS score using the official ranges (Low / Medium / High / Critical), so it never contradicts the score
- **Linking**: link a catalog vulnerability to an asset, with a treatment status (Open / In treatment / Fixed / Accepted)
- **Listing**: view the whole catalog, or the vulnerabilities of a specific asset with their status on it
- **Status update**: change the treatment status of a vulnerability on a specific asset
- **Unlinking**: remove a vulnerability from an asset, keeping it in the catalog
- **Catalog editing**: fix the name or the CVSS score
- **Catalog deletion**: remove a vulnerability from the catalog and from every linked asset, with confirmation

> **In development:** integration with CVE for identifying known vulnerabilities.

### Risk Analysis (in development)
Model based on linear algebra that estimates the risk of each asset from its vulnerabilities and dependencies between assets. The catalog and the links are the basis of the incidence matrix `M` and of the severity vector `v` used to compute each asset's own risk (`b = Mv`).

### General
- **Data persistence**: assets and their links are saved to `ativos.json`, and the catalog to `vulnerabilidades.json`, both as a list of JSON objects, and reloaded on every run
- **ID index**: assets and catalog vulnerabilities are stored in dictionaries indexed by ID, allowing efficient constant-time search (O(1))
- **Global error handling**: Ctrl+C and Ctrl+D anywhere in the program exit cleanly, without a traceback

## 🫧 Tech Stack

- Python 3.8+
- Standard library modules: `json`, `enum`
- Tests: `unittest` and `pytest`; linting: `flake8` and `black`; CI with GitHub Actions
- **In development**: linear algebra library (TBD), Docker

## ✨ Architecture

- **Class hierarchy**: `Ativo` (base) + `Notebook`, `Servidor`, `Roteador`, `Impressora` (subclasses)
- **Polymorphism**: each subclass overrides `exibir_detalhes()` and adds its own specific attributes
- **Vulnerability catalog**: `Vulnerabilidade` objects stored in a `catalogo[id]` dictionary; each asset keeps a `{id_vulnerabilidade: StatusDaVuln}` dictionary of links (reference, not copy)
- **Calculated level**: `Vulnerabilidade.nivel()` derives the severity level from the CVSS score
- **Serialization / deserialization**: `para_dicionario()` converts objects to dictionaries; `de_dicionario()` (class method) rebuilds objects from dictionaries
- **ID index**: `ativos[id]` and `catalogo[id]` dictionaries for O(1) search
- **Separation of responsibilities**: functions that change data (e.g., `vincular_vulnerabilidade()`) only validate and raise `DadoInvalidoError`, while the menu handles all user interaction; pure functions (e.g., `listar_ativos_por_tipo()`) are kept apart from the I/O layer

## ✨ Project Structure

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

> The data files `ativos.json` and `vulnerabilidades.json` are generated automatically on first run and are not version-controlled.

## 🫧 Getting Started

Requirement: Python 3.8 or higher installed.

```bash
git clone https://github.com/cadulugaresi/it-asset-vulnerability-manager.git
cd it-asset-vulnerability-manager
python3 main.py
```

> On Windows, use `python` instead of `python3`.

The program opens an interactive menu in the terminal. Follow the numbered options to register assets, manage vulnerabilities, and persist data.

### Main menu

```
1 - Cadastrar ativo
2 - Listar ativo
3 - Excluir ativo
4 - Menu de vulnerabilidades
5 - Editar ativo
6 - Sair
```

Inside option 4 (Menu de vulnerabilidades), a submenu manages the catalog and the links between vulnerabilities and assets:

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

Inside option 5 (Editar ativo), a submenu lets you update the owner, status, department, or type-specific attributes of an asset.

### Running the tests

```bash
python3 -m unittest tests/testes.py tests/test_vulnerabilidades.py
python3 -m pytest tests/test_exemplos.py
python3 -m flake8 main.py inventario
```

## ✨ Deletion Policy

The system uses **physical deletion**:
- When an **asset** is removed, the record is permanently erased from `ativos.json`, along with its links. The vulnerabilities themselves remain in the catalog.
- When a **vulnerability** is removed from the catalog, it is permanently erased from `vulnerabilidades.json` and unlinked from every asset, so no asset is left pointing to a vulnerability that no longer exists.

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