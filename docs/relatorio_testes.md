# Relatório de Testes

UID: S2_18 (atualizado na S4_01)

## ✨ Situação atual (S4_01)

| Arquivo                          | Ferramenta                    | Testes  |
| -------------------------------- | ----------------------------- | ------- |
| `tests/testes.py`                | `unittest`                    | 92      |
| `tests/test_vulnerabilidades.py` | `unittest`                    | 92      |
| `tests/test_exemplos.py`         | `pytest` (com parametrização) | 7       |
| **Total**                        |                               | **191** |

Resultado atual: OK (todos passam). O CI (`.github/workflows/testes.yml`) roda `flake8`, `unittest` e `pytest` a cada push e pull request na `main`.

**Execução:**

```bash
python3 -m unittest tests/testes.py tests/test_vulnerabilidades.py
python3 -m pytest tests/test_exemplos.py -v
python3 -m flake8 main.py inventario
```

**Cobertura por camada:**
- **Domínio:** exibição e serialização das subclasses de `Ativo` e de `Vulnerabilidade`, nível calculado pelo CVSS, `validar_nome_responsavel` e `validar_cvss` (incluindo fronteiras como 0.04, 0.1, 10 e 10.1)
- **Serviços:** registro, atualização (inclusive troca de tipo mantendo vínculos) e remoção de ativos; buscas por ID, nome, status e tipo; catálogo (`proximo_id`, registro, edição e exclusão); vínculo, desvínculo e atualização de status
- **Persistência:** salvar e recarregar ativos, vínculos e catálogo; arquivo inexistente devolve dados vazios
- **Interface:** funções `pedir_*` e conversões do menu, cadastro, edição e exclusão de ativos, edição de vulnerabilidade e vínculo logo após o cadastro, simulando a digitação com `unittest.mock.patch`

**Isolamento dos dados:** os testes que salvam dados herdam de `TesteComArquivosTemporarios` (`tests/apoio.py`), que troca `ativos.json` e `vulnerabilidades.json` por arquivos temporários no `setUp` e os apaga no `tearDown`. Os arquivos reais nunca são tocados pelos testes.

## 🫧 Registro histórico (S2_18)

Na S2_18, a suíte tinha 32 testes no arquivo `testes.py`, executados com `python3 -m unittest testes.py`, cobrindo a criação e a serialização de `Ativo` e `Vulnerabilidade`, as validações de entrada, a busca por ID e por nome e os filtros por categoria e status.

### Falha observada

Testes `TestFiltros.test_encontrar_ativos_por_categ_*` e `TestFiltros.test_encontrar_ativos_por_status_*` falharam.

**Comportamento esperado:** a função deveria retornar uma lista com todos os ativos que casassem com o filtro.

**Comportamento observado:**
- `AttributeError: 'dict' object has no attribute 'categoria'` — a função usava `ativos.categoria` em vez de `ativo.categoria`;
- Mesmo corrigindo o nome, o `return` estava dentro do loop, retornando após o primeiro match;
- Nos casos sem match, a função retornava `None` em vez de lista vazia.

### Correção

```python
def encontrar_ativos_por_categ(categoria, ativos):
    encontrados = []
    for ativo in ativos.values():
        if ativo.categoria == categoria:
            encontrados.append(ativo)
    return encontrados
```

> A categoria do ativo foi substituída depois pelas subclasses (`Notebook`, `Servidor`...). Hoje, o filtro equivalente é `encontrar_ativos_por_tipo(ativos, classe)`, em `inventario/servicos/ativos.py`, e segue o mesmo padrão corrigido.
