# Padrões de Projeto — Trabalho 2 (S4_03)

**Autor:** Cadu Lugaresi · Cibersegurança, Turma 2 · UFU

O Trabalho 2 usa três padrões de projeto: Factory, para recriar cada ativo na subclasse certa; Repository, para isolar o armazenamento; e Strategy, para trocar o critério de ordenação dos ativos. Este documento descreve o problema que cada um resolve, onde ele está no código e os padrões que foram considerados e descartados.

## ✨ Factory

**Problema:** ao carregar os dados (do JSON ou do banco), cada registro tem só um texto no campo `tipo` (`"Notebook"`, `"Servidor"`...). O programa precisa criar o objeto da subclasse certa sem uma cadeia de `if/elif` que teria de ser editada a cada tipo novo.

**Solução:** o dicionário `MAPA_DE_TIPOS` (`inventario/dominio/ativo.py`) liga o nome do tipo à classe, e cada subclasse sabe se construir a partir de um dicionário com o método de classe `de_dicionario`:

```python
ativo = MAPA_DE_TIPOS[tipo].de_dicionario(dados_do_ativo)
```

A mesma fábrica é usada pelo `RepositorioJSON` e pelo `RepositorioSQLite`, e as opções de tipo do menu (`TIPOS_DE_ATIVOS`) também são geradas a partir dela. Um tipo novo entra com a subclasse e uma linha no mapa.

## 🫧 Repository

**Problema:** os serviços gravavam e liam dados chamando funções do módulo de arquivos JSON. Trocar o armazenamento exigiria mudar todos eles.

**Solução:** as operações de dados (carregar, adicionar, atualizar e remover ativos e vulnerabilidades, e as operações de vínculo e de dependência) ficam em classes de repositório. Há duas implementações, que oferecem as mesmas operações:

- `RepositorioSQLite` (`banco_sqlite.py`): o armazenamento do programa, em `inventario.db`;
- `RepositorioJSON` (`arquivos_json.py`): arquivos JSON com escrita atômica.

Os serviços recebem o repositório como parâmetro e não sabem qual implementação estão usando. A mesma suíte de testes de contrato roda nas duas e garante que elas continuam oferecendo as mesmas operações.

## ✨ Strategy

**Problema:** a listagem de todos os ativos pode ser ordenada de jeitos diferentes, e cada critério novo não deveria exigir mudanças na operação que ordena.

**Solução:** em `inventario/servicos/ordenacao.py`, cada critério é uma função que recebe um ativo e devolve o valor de comparação (`por_id`, `por_nome` e `por_quantidade_de_vulnerabilidades`, que coloca os mais vulneráveis primeiro). A operação recebe a estratégia pronta:

```python
def listar_ativos_ordenados(ativos, criterio):
    return sorted(ativos.values(), key=criterio)
```

O mapa `CRITERIOS_DE_ORDENACAO` reúne as estratégias disponíveis, e o menu monta as opções a partir dele. As estratégias são funções de primeira classe, e não classes: em Python, uma função já pode ser passada como valor, então uma classe por critério só acrescentaria código. Um critério novo, como a ordenação por risco, será uma função nova e uma linha no mapa, sem mudar a operação nem o menu.

## 🫧 Singleton: considerado e descartado

O Singleton garantiria uma única conexão com o banco, acessível de qualquer lugar do programa. Ele não foi adotado porque:

- **o programa já cria um único repositório**, no `main.py`, e o injeta nas outras camadas. A unicidade existe sem precisar de uma classe que a imponha;
- **um acesso global esconderia a dependência**: os serviços passariam a buscar a conexão sozinhos, voltando ao problema que a injeção de dependência resolveu (S4_02);
- **os testes precisam de vários repositórios**: a suíte de contrato cria um repositório novo, apontando para um banco temporário, para conferir o que foi gravado. Um Singleton impediria isso ou exigiria reiniciá-lo entre os testes.

Com a API do S4_05, o acesso ao banco vai acontecer em requisições diferentes, e a forma de criar a conexão será decidida nessa etapa.

## ✨ Quando não usar um padrão

Durante o S4_03 foi cogitada uma fábrica de repositórios, que escolheria entre JSON e SQLite a partir de uma variável de ambiente. Ela foi descartada: o programa usa só o SQLite, e a fábrica acrescentaria configuração e código sem resolver nenhum problema real. A troca de implementação continua sendo uma linha no `main.py`. Se um dia o programa precisar escolher o armazenamento por configuração (por exemplo, no container), a fábrica pode ser criada nesse momento.