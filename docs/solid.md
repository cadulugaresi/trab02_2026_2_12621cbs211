# Relatório SOLID — Trabalho 2 (S4_02)

**Autor:** Cadu Lugaresi · Cibersegurança, Turma 2 · UFU
**Branch:** `repositorio`

Este relatório lista as violações dos princípios SOLID encontradas no Trabalho 2, as correções aplicadas e o princípio envolvido em cada uma. A principal mudança foi a criação de uma interface de repositório com duas implementações (JSON e SQLite), de modo que os serviços deixaram de depender de um formato de armazenamento específico.

## ✨ Visão geral

```
interface ──► servicos ──► Repositorio (abstração)
                              ├── RepositorioJSON    (arquivos_json.py)
                              └── RepositorioSQLite  (banco_sqlite.py)

main.py escolhe a implementação e a injeta na cadeia menu → interface → serviços.
```

## 🫧 1. Serviços presos ao JSON → DIP

**Violação:** os serviços (`servicos/ativos.py` e `servicos/vulnerabilidades.py`) importavam `salvar_dados` e `salvar_catalogo` direto de `persistencia/arquivos_json.py`. A regra de negócio dependia de um detalhe de armazenamento.

**Correção:** criação da classe abstrata `Repositorio` (`persistencia/repositorio.py`, com `abc.ABC` e `@abstractmethod`). Toda função de serviço que grava dados recebe um `repositorio` como primeiro parâmetro e chama só os métodos da abstração (ex.: `repositorio.adicionar_ativo(ativo)`). Nenhum arquivo de `servicos/` ou `interface/` importa mais a camada de persistência.

**Princípio:** Inversão de Dependência (DIP), com injeção de dependência por parâmetro. O `main.py` é o único ponto que conhece a implementação concreta.

## ✨ 2. Trocar o armazenamento exigiria editar os serviços → OCP

**Violação:** para passar de JSON para banco de dados, seria preciso abrir e alterar todos os serviços que gravavam dados.

**Correção:** um novo armazenamento entra como uma nova subclasse de `Repositorio`. O `RepositorioSQLite` foi criado assim, e a troca no programa foi uma linha no `main.py` (`RepositorioJSON()` → `RepositorioSQLite()`). Serviços, menus e telas não mudaram.

**Princípio:** Aberto/Fechado (OCP).

## 🫧 3. Cadeias de if/elif por tipo de ativo → OCP

**Violação:** código que dependia do tipo do ativo precisaria de um `if/elif` por tipo, editado a cada tipo novo.

**Correção:**
- `MAPA_DE_TIPOS` (domínio) liga o nome do tipo à classe. A reconstrução dos objetos (`MAPA_DE_TIPOS[tipo].de_dicionario(...)`) e as opções do menu (`TIPOS_DE_ATIVOS`) são geradas a partir dele.
- `TABELAS_DOS_TIPOS` (persistência) liga cada tipo à sua tabela no banco e às suas colunas. O mesmo código grava, atualiza e carrega os quatro tipos, sem nenhum `if/elif`.

Um tipo novo pede a subclasse, uma linha em cada mapa e a tabela no `esquema.sql`, sem alterar nenhum método existente. Os dois mapas ficam separados de propósito: o domínio diz *o que* é um tipo, e a persistência diz *onde* ele é guardado.

**Princípio:** Aberto/Fechado (OCP).

## ✨ 4. Uma implementação pode substituir a outra? → LSP

**Verificação:** a suíte `tests/contrato_repositorio.py` reúne 17 testes de contrato que gravam, recarregam com um repositório novo e conferem o resultado. A mesma suíte roda nas duas implementações (`tests/test_repositorio.py` e `tests/test_repositorio_sqlite.py`) e passa nas duas. Isso mostra que o `RepositorioSQLite` substitui o `RepositorioJSON` sem mudar o comportamento esperado pelos serviços.

As subclasses de `Ativo` (Notebook, Servidor, Roteador, Impressora) também respeitam o princípio: elas estendem `exibir_detalhes` e `para_dicionario` chamando `super()`, sem mudar o que a classe base promete.

**Princípio:** Substituição de Liskov (LSP).

## 🫧 5. Funções com mais de uma responsabilidade → SRP

**Violações e correções:**
- `salvar_dados` transformava os ativos em dicionários **e** gravava o arquivo. A gravação segura (arquivo `.tmp` + `os.replace`) foi recortada em `salvar_seguro`, usada pelas duas funções de salvar.
- A camada de persistência mostrava mensagens com `print`. Agora ela lança `PersistenciaError`, e só a interface fala com o usuário.
- No `RepositorioSQLite`, a gravação dos dados próprios de cada tipo foi recortada em `inserir_dados_do_tipo`, usada por `adicionar_ativo` e `atualizar_ativo`. A tradução dos erros do `sqlite3` para `PersistenciaError` ficou num único método, `executar`, por onde passam todos os comandos.

**Princípio:** Responsabilidade Única (SRP).

## ✨ 6. Interface do repositório → ISP

**Análise:** o `Repositorio` tem 11 métodos (carregar, adicionar, atualizar e remover ativos e vulnerabilidades, e as operações de vínculo). Todos são usados pelos serviços e implementados pelas duas classes, então nenhuma implementação é obrigada a ter métodos que não usa.

**Decisão:** a interface não foi dividida. Uma divisão possível, se o projeto crescer, seria separar `RepositorioDeAtivos` e `RepositorioDeVulnerabilidades`, para que cada serviço dependa só do que usa.

**Princípio:** Segregação de Interfaces (ISP).

## 🫧 Decisões e melhorias futuras

- **Operações diretas em vez de sincronização:** a primeira versão do repositório salvava o estado inteiro (`salvar_ativos(ativos)`). No SQLite, isso exigia comparar o banco com a memória para apagar registros removidos e corria o risco de disparar o `ON DELETE CASCADE` nos vínculos. A interface passou a ter uma operação por entidade, e cada método virou um comando SQL.
- **Transações:** toda escrita no SQLite usa `with self.conexao:`, então comandos que dependem um do outro (ex.: gravar o ativo e a tabela do seu tipo) são confirmados juntos ou desfeitos juntos.
- **Consultas N+1:** o `carregar_ativos` busca os vínculos de cada ativo numa consulta separada. Para inventários grandes, uma evolução seria buscar todos os vínculos em uma consulta só.