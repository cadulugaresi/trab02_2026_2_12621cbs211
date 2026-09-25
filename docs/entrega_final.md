# Entrega Final — Trabalho 1 (Sprint 2)

Versão: v1.0

## Definição de Pronto

- [x] CRUD de ativos funcional (cadastro, listagem, busca, edição, exclusão);
- [x] Vulnerabilidades associadas a ativos (cadastro, listagem, remoção);
- [x] Persistência em `ativos.json`;
- [x] Validação de entradas com mensagens seguras;
- [x] Tratamento global de erro (Ctrl+C / Ctrl+D);
- [x] Busca por ID e por nome (parcial, case-insensitive);
- [x] Filtros por categoria e status;
- [x] Edição de responsável, status, setor e categoria;
- [x] Política de exclusão documentada no README;
- [x] Testes automatizados (32 testes, todos passando);
- [x] Documentação de requisitos, validações, critérios de aceitação e especificação.

## Rastreabilidade

- `docs/requisitos.md` — requisitos funcionais e não funcionais
- `docs/validacoes.md` — matriz campo × regra × mensagem
- `docs/criterios_aceitacao.md` — cenários Dado-Quando-Então
- `docs/especificacao.md` — especificação consolidada
- `docs/relatorio_testes.md` — falhas e correções
- `testes.py` — suíte de testes

## Novos aprendizados

Praticamente todo o Python que usei foi aprendido do zero durante a sprint:

- Estruturas de dados: listas, dicionários, tuplas, sets;
- Classes, atributos, métodos, `__init__`, `self`;
- Enum (`Enum`) para valores fixos;
- Serialização com `json.dump` / `json.load`;
- Tratamento de exceções (`try`/`except`/`else`/`finally`, exceções customizadas);
- Hierarquia de exceções (`Exception` vs `BaseException`, `KeyboardInterrupt`, `EOFError`);
- Diferença entre `raise` e captura, princípio "raise low, catch high";
- Funções com parâmetros, retorno, escopo;
- Separação entre regra de negócio e I/O;
- `unittest`: `TestCase`, `setUp`, `assertEqual`, `assertRaises`, `assertIsNone`;
- List comprehension (aprendido, optei por não usar em favor do `for` explícito);
- `dict.get()` como alternativa segura a `dict[chave]`;
- Git: branches, commits, push, pull, PR, merge, `cherry-pick`, `reset`, `reflog`, `.gitignore`;
- Fluxo GitHub: issue → branch → commit → PR → revisão → merge.

O que eu já sabia antes: operações matemáticas, `print`, `input` e condicionais simples.

## Como executar

```bash
git https://github.com/cadulugaresi/it-asset-vulnerability-manager.git
cd it-asset-vulnerability-manager
python3 "main code s1.py"