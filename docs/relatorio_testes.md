# Relatório de Testes — CRUD

UID: S2_18

Arquivo: `testes.py`
Total: 32 testes
Execução: `python3 -m unittest testes.py`
Resultado atual: OK (todos passam)

Cobertura:
- Criação e serialização de `Ativo` e `Vulnerabilidade`
- Validações de entrada (`validar_nome_responsavel`, `validar_status`, `validar_setor`, `validar_categoria`)
- Busca por ID e por nome (parcial, case-insensitive)
- Filtros por categoria e status
- Operações CRUD (cadastro, busca, atualização, exclusão)

## Registro de falha e correção

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