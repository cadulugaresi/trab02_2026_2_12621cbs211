# Relatório de Testes

UID: S2_18 (atualizado na S4_01 e na S4_05)

## ✨ Situação atual (S4_05)

| Arquivo                            | Ferramenta                    | Testes  |
| ---------------------------------- | ----------------------------- | ------- |
| `tests/testes.py`                  | `unittest`                    | 113     |
| `tests/test_vulnerabilidades.py`   | `unittest`                    | 92      |
| `tests/test_dependencias.py`       | `unittest`                    | 52      |
| `tests/test_api.py`                | `unittest`                    | 38      |
| `tests/test_risco.py`              | `unittest`                    | 26      |
| `tests/test_repositorio_sqlite.py` | `unittest`                    | 25      |
| `tests/test_repositorio.py`        | `unittest`                    | 24      |
| `tests/test_persistencia.py`       | `unittest`                    | 14      |
| **Subtotal `unittest`**            |                               | **384** |
| `tests/test_exemplos.py`           | `pytest` (com parametrização) | 7       |
| **Total**                          |                               | **391** |

Resultado atual: OK (todos passam). O subtotal de 384 é o resultado de `python3 -m unittest discover -s tests`. O CI (`.github/workflows/testes.yml`) roda `flake8`, `unittest` e `pytest` a cada push e pull request na `main`.

**Execução:**

```bash
python3 -m unittest discover -s tests
python3 -m pytest tests/test_exemplos.py -v
python3 -m flake8 main.py iniciar_api.py inventario
python3 -m black --check main.py iniciar_api.py inventario
```

**Cobertura por camada:**
- **Domínio:** exibição e serialização das subclasses de `Ativo` e de `Vulnerabilidade`, nível calculado pelo CVSS, `validar_texto_obrigatorio` e `validar_cvss` (incluindo fronteiras como 0.04, 0.1, 10 e 10.1)
- **Serviços:** registro, atualização (inclusive troca de tipo mantendo vínculos) e remoção de ativos; buscas por ID, nome, status e tipo; catálogo (`proximo_id`, registro, edição e exclusão); vínculo, desvínculo e atualização de status
- **Persistência:** salvar e recarregar ativos, vínculos e catálogo; arquivo inexistente devolve dados vazios
- **Interface (menu):** funções `pedir_*` e conversões do menu, cadastro, edição e exclusão de ativos, edição de vulnerabilidade e vínculo logo após o cadastro, simulando a digitação com `unittest.mock.patch`
- **Interface (API):** `tests/test_api.py` usa o `test_client()` do Flask, que envia requisições direto para o app, sem ligar o servidor. Os testes conferem o status e o JSON de todas as rotas: `/saude`; listagem ordenada, cadastro (201, com o fator de exposição padrão do tipo), busca (200 e 404) e gravação no banco de ativos; cadastro de vulnerabilidade com id gerado pelo servidor; vínculo; e o ranking de `/riscos`. Também conferem que cada entrada inválida responde 400 e não é gravada: tipo inexistente, campo faltando, setor ou status de tratamento fora do Enum, fator de exposição fora do limite ou booleano, responsável ou nome vazio, nome só com espaços ou numérico, id em texto ou negativo, campo próprio do tipo em texto (`"tela": "grande"`) ou fracionário onde o menu pede inteiro (portas do roteador), CVSS fora do limite, em texto ou booleano, id repetido, vínculo repetido e ativo ou vulnerabilidade inexistentes. Um corpo que não é JSON e um JSON malformado respondem 400 em JSON nas três rotas de cadastro, e uma falha do repositório (`PersistenciaError`, simulada com `unittest.mock.patch`) responde 500 em JSON, e não com uma página HTML.

**Isolamento dos dados:** os testes que salvam em JSON herdam de `TesteComArquivosTemporarios` (`tests/apoio.py`), que troca `ativos.json` e `vulnerabilidades.json` por arquivos temporários no `setUp` e os apaga no `tearDown`. Os testes da API criam o app com `criar_app` e um banco SQLite em memória (`RepositorioSQLite(":memory:")`), novo a cada teste e descartado no `tearDown`. Os arquivos reais e o `inventario.db` nunca são tocados pelos testes.

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
