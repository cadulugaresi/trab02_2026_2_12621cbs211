# IT Asset & Vulnerability Manager

*[Ler em português](./README.pt-br.md)*

A command-line (CLI) application in Python for registering and managing IT assets and their associated security vulnerabilities. Built as a study project for a Cybersecurity course, applying clean code practices (expressive naming, single-responsibility functions, separation between business rules and I/O, error handling that doesn't leak internal details).

## ✨ Features

### Assets
- **Registration**: ID, name, category (Notebook / Server / Router / Printer), department (TI / Financeiro / Marketing / RH / Jurídico), owner, and status (Active / Inactive / Under maintenance), with input validation
- **Listing**: view all registered assets, or search by **ID** or **name/hostname** (partial, case-insensitive)
- **Editing**: update owner, status, department, or category
- **Deletion**: remove an asset by ID

### Vulnerabilities
- **Registration**: description, type (free text), severity (Low / Medium / High), and treatment status (Open / In treatment / Fixed / Accepted)
- **Listing**: view all vulnerabilities, or filter by asset
- **Deletion**: remove a vulnerability from an asset by name

### General
- **Data persistence**: data is automatically saved to an `ativos.json` file and reloaded on every run
- **Global error handling**: Ctrl+C and Ctrl+D anywhere in the program exit cleanly, without a traceback

## 🫧 Tech Stack

- Python 3.8+
- Standard library modules: `json`, `enum`

## ✨ Project Structure
.
├── main code s1.py # Entry point: interactive menu and program flow
├── funcoes_s1.py # Domain classes, validation, business logic, and persistence
├── .gitignore
├── README.md
└── README.pt-br.md

> The `ativos.json` file (saved data) is generated automatically on first run and is not version-controlled.

## 🫧 Getting Started

Requirement: Python 3.8 or higher.

```bash
git clone https://github.com/byuwarn/it-asset-vulnerability-manager.git
cd it-asset-vulnerability-manager
python "main code s1.py"

The program opens an interactive menu in the terminal. Follow the numbered options to register assets, manage vulnerabilities, and persist data.

✨ Main Menu

MENU
1 - Cadastrar ativo
2 - Listar ativos
3 - Excluir ativo
4 - Editar vulnerabilidades
5 - Editar ativo
6 - Sair

Inside option 4 (Editar vulnerabilidades), a submenu lets you list, add, and remove vulnerabilities for a specific asset.

Inside option 5 (Editar ativo), a submenu lets you update the owner, status, department, or category of an asset.

🫧 Project Status

Developed incrementally across sprints in the early weeks of my Cybersecurity degree at the Federal University of Uberlândia, with a focus on:

Clear, expressive naming
Single-responsibility functions
Separation between business rules and I/O
Error handling that doesn't expose internal details
User input validation

✨ ## Deletion Policy

The system uses **physical deletion**: when an asset is removed, the record is permanently erased from `ativos.json`, along with its associated vulnerabilities.

**Rationale:**
- The project scope does not require audit or removal history;
- Keeping deleted records would increase complexity without clear benefit;
- The user must confirm deletion before removal (mitigation against accidental deletion).

**Logical deletion** (marking as inactive instead of erasing) was considered but discarded as it is outside the scope of Assignment 1.

🫧 License

Study project, free to use for educational purposes.