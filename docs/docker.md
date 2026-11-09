# Docker — Imagem do Trabalho 2 (S4_16)

Este documento registra a construção da imagem Docker do sistema de gerenciamento de ativos e vulnerabilidades e as evidências da sua execução local em container.

**Aluno:** Cadu Lugaresi — Cibersegurança UFU, Turma 2
**Ambiente:** MacBook Air (Apple Silicon) com Docker Desktop v4.98.0 e Docker 29.9.2

---

## ✨ Dockerfile

```dockerfile
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

RUN useradd --create-home inventario && mkdir -p /app/dados && chown inventario /app/dados

WORKDIR /app

COPY main.py .
COPY inventario/ inventario/

USER inventario

WORKDIR /app/dados

HEALTHCHECK CMD python3 -c "import sqlite3; sqlite3.connect('inventario.db').execute('SELECT 1')"

CMD ["python3", "/app/main.py"]
```

### Decisões

- **Imagem base `python:3.13-slim`:** mesma versão do Python usada no workflow de testes do GitHub Actions, numa variante enxuta da imagem oficial.
- **Sem `requirements.txt`:** o programa usa apenas a biblioteca padrão do Python (`sqlite3`, `os` etc.), então não há dependências externas para instalar.
- **Ordem das instruções:** a criação do usuário e da pasta de dados vem antes da cópia do código. Assim, alterações no código não invalidam o cache dessas camadas, e só as camadas a partir do `COPY` são reconstruídas.
- **Usuário sem privilégios:** o programa roda com o usuário `inventario`, e não como `root`. Se a aplicação for comprometida, o invasor não tem privilégios de administrador dentro do container.
- **Pasta de dados `/app/dados`:** o banco SQLite é criado no diretório de trabalho (`inventario.db`). Executar o programa a partir de `/app/dados` separa os dados do código sem alterar nenhuma linha da aplicação. A pasta pertence ao usuário `inventario`, que precisa de permissão de escrita para gravar o banco.
- **`PYTHONDONTWRITEBYTECODE=1`:** evita a criação de arquivos `__pycache__` dentro do container.
- **`PYTHONUNBUFFERED=1`:** faz o Python exibir a saída imediatamente, o que é necessário para o menu interativo aparecer no terminal e para os logs do container.
- **Healthcheck:** como o sistema é uma aplicação de terminal, sem endpoint HTTP, a verificação de funcionamento consiste em abrir o banco SQLite e executar uma consulta simples (`SELECT 1`).

## 🫧 .dockerignore

```
.git/
.gitignore

tests/
docs/
.github/
README.md

**/__pycache__/
**/*.py[cod]
.pytest_cache/
.coverage
htmlcov/
venv/
env/
.venv/

**/*.db
**/*.json
**/*.tmp

.vscode/
.idea/
**/.DS_Store
**/rascunhos.py

Dockerfile
.dockerignore
```

- Ficam fora da imagem os arquivos que não são necessários para executar o programa: histórico do git, testes, documentação, caches e ambientes virtuais.
- **Dados locais (`*.db` e `*.json`) nunca entram na imagem.** Isso impede que o banco de desenvolvimento, com dados reais, seja distribuído junto com a imagem.
- O prefixo `**/` aplica a regra em qualquer subpasta, e não só na raiz. Ele é necessário para arquivos que aparecem dentro de `inventario/`, como `__pycache__` e `.DS_Store`.

---

## ✨ Evidências de execução

### 1. Construção da imagem

```bash
docker build -t inventario:1.0 .
```

```
[+] Building 1.9s (12/12) FINISHED                           docker:desktop-linux
 => [internal] load build definition from Dockerfile                         0.0s
 => => transferring dockerfile: 431B                                         0.0s
 => [internal] load metadata for docker.io/library/python:3.13-slim          1.2s
 => [auth] library/python:pull token for registry-1.docker.io                0.0s
 => [internal] load .dockerignore                                            0.0s
 => => transferring context: 274B                                            0.0s
 => [1/6] FROM docker.io/library/python:3.13-slim@sha256:e4...               0.0s
 => [internal] load build context                                            0.0s
 => => transferring context: 1.38kB                                          0.0s
 => CACHED [2/6] RUN useradd --create-home inventario && mkdir -p /app/dados 0.0s
 => CACHED [3/6] WORKDIR /app                                                0.0s
 => CACHED [4/6] COPY main.py .                                              0.0s
 => [5/6] COPY inventario/ inventario/                                       0.0s
 => [6/6] WORKDIR /app/dados                                                 0.0s
 => exporting to image                                                       0.5s
 => => naming to docker.io/library/inventario:1.0                            0.0s
 => => unpacking to docker.io/library/inventario:1.0                         0.4s
```

- As etapas 2 a 4 foram reaproveitadas do cache (`CACHED`) de uma construção anterior. Apenas a etapa 5 foi refeita, porque o conteúdo copiado mudou após o ajuste do `.dockerignore`.
- O contexto enviado para a construção tem apenas **1,38 kB**, mesmo com o `inventario.db` e o `__pycache__` presentes na pasta do projeto: o `.dockerignore` os excluiu.

### 2. Tamanho da imagem

```bash
docker images inventario
```

```
IMAGE            ID             DISK USAGE   CONTENT SIZE
inventario:1.0   82670bec2eec        202MB         43.4MB
```

### 3. Execução do sistema no container

```bash
docker run -it --name inventario inventario:1.0
```

```
            MENU

            1 - Cadastrar ativo
            2 - Listar ativo
            3 - Excluir ativo
            4 - Menu de vulnerabilidades
            5 - Editar ativo
            6 - Sair

Escolha uma opção: 1
Tipos de ativo:
1 - Notebook
2 - Servidor
3 - Roteador
4 - Impressora
Digite o tipo do ativo: 3
Digite o ID do ativo: 23
Digite o nome do ativo: Callink modem
Digite o setor do ativo: 4
Digite o nome do responsável pelo ativo: Flamber
Digite o status do ativo: 2
Digite a quantidade de portas do roteador: 5
Digite a velocidade do roteador em MB: 1000
Ativo cadastrado com sucesso!

Escolha uma opção: 2
Deseja listar todos os ativos, filtrar ou mostrar apenas um?
todos/filtrar/um): todos
Ordenar por (id/nome/vulnerabilidades): id
Listando todos os ativos...

            ID: 17
            Nome: Macbook Air M1
            Tipo: Notebook
            Setor: TI
            Responsável: Cadu
            Status: ATIVO
            Sistema operacional: MacOS
            Tamanho da tela: 16.0 polegadas

            ID: 23
            Nome: Callink modem
            Tipo: Roteador
            Setor: RH
            Responsável: Flamber
            Status: INATIVO
            Qtde de portas: 5
            Velocidade: 1000MB

Escolha uma opção: 6
Saindo do programa...
```

O sistema funcionou normalmente dentro do container: cadastro de ativos, listagem e ordenação. Trechos repetidos do menu foram omitidos.

### 4. Usuário sem privilégios

Com o sistema em execução, em outro terminal:

```bash
docker exec inventario whoami
```

```
inventario
```

O processo roda com o usuário `inventario`, e não como `root`.

### 5. Healthcheck

```bash
docker ps
```

Logo após a inicialização:

```
CONTAINER ID   IMAGE            COMMAND                  CREATED          STATUS                             NAMES
a1ea448eb879   inventario:1.0   "python3 /app/main.py"   23 seconds ago   Up 23 seconds (health: starting)   inventario
```

Após o primeiro intervalo de verificação (30 segundos):

```
CONTAINER ID   IMAGE            COMMAND                  CREATED          STATUS                    NAMES
a1ea448eb879   inventario:1.0   "python3 /app/main.py"   56 seconds ago   Up 56 seconds (healthy)   inventario
```

O status passou de `health: starting` para `healthy`, confirmando que o banco de dados está acessível dentro do container.

---

## 🫧 Limitação observada

Após remover o container com `docker rm` e criar um novo a partir da mesma imagem, os ativos cadastrados anteriormente não aparecem mais na listagem. O banco `inventario.db` é criado dentro do container, em `/app/dados`, e é apagado junto com ele. A persistência dos dados entre containers depende de um volume montado nessa pasta, configurado no `compose.yaml`.