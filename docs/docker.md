# Docker — Trabalho 2 (S4_16 e S4_17)

Este documento registra a conteinerização do sistema de gerenciamento de ativos e vulnerabilidades: a construção da imagem Docker (S4_16) e a configuração com Docker Compose, com volume, política de reinício e healthcheck (S4_17), junto com as evidências de execução e dos testes.

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
compose.yaml
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
=== Menu principal ===

1 - Cadastrar ativo
2 - Listar ativo
3 - Excluir ativo
4 - Menu de vulnerabilidades
5 - Editar ativo
6 - Menu de dependências
7 - Análise de risco
8 - Sair
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

## 🫧 Limitação da imagem sozinha

Após remover o container com `docker rm` e criar um novo a partir da mesma imagem, os ativos cadastrados anteriormente não aparecem mais na listagem. O banco `inventario.db` é criado dentro do container, em `/app/dados`, e é apagado junto com ele. A configuração com Docker Compose resolve isso montando um volume nessa pasta.

---

## ✨ compose.yaml

```yaml
services:
  inventario:
    build: .
    container_name: inventario
    stdin_open: true
    tty: true
    restart: unless-stopped
    volumes:
      - "dados:/app/dados"
    healthcheck:
      test: ["CMD", "python3", "-c", "import sqlite3; sqlite3.connect('inventario.db').execute('SELECT 1')"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s

volumes:
  dados:
```

### Decisões

- **`build: .`:** a imagem é construída a partir do Dockerfile do projeto, então o Compose sempre usa a versão atual do código.
- **`stdin_open` e `tty`:** o sistema é um menu interativo que lê do teclado com `input()`. Sem uma entrada aberta, o `input()` falharia assim que o container iniciasse em segundo plano, o programa encerraria e o container entraria num ciclo de reinícios. Com as duas opções, o programa fica aguardando a entrada, e o usuário se conecta ao menu com `docker attach inventario` e se desconecta sem encerrar o programa com **Ctrl + P, Ctrl + Q**.
- **Volume nomeado `dados` em `/app/dados`:** é a pasta onde o banco SQLite é criado. O volume é gerenciado pelo Docker e existe independentemente do container, então os dados sobrevivem quando o container é removido ou recriado.
- **Política de reinício `unless-stopped`:** reinicia o container sempre que o processo principal termina, seja por falha ou porque o usuário escolheu "Sair" no menu, e também quando o Docker é reiniciado. A exceção é quando o container é parado manualmente, o que permite desligá-lo de propósito para manutenção. A política `on-failure` não seria suficiente, porque sair pelo menu encerra o programa com sucesso (código 0) e não dispararia o reinício. A política `always` não respeitaria uma parada manual após o Docker reiniciar.
- **Healthcheck:** o mesmo teste do Dockerfile (abrir o banco e executar `SELECT 1`), com os parâmetros explícitos: verificação a cada 30 segundos, limite de 5 segundos por verificação, 3 falhas seguidas para marcar o container como `unhealthy` e 10 segundos de tolerância na inicialização.

---

## 🫧 Evidências do Docker Compose

### 1. Subida da aplicação

```bash
docker compose up -d --build
```

```
 ✔ Image it-asset-vulnerability-manager-inventario  Built
 ✔ Network it-asset-vulnerability-manager_default   Created
 ✔ Volume it-asset-vulnerability-manager_dados      Created
 ✔ Container inventario                             Started
```

```bash
docker compose ps
```

```
NAME         IMAGE                                       COMMAND                  SERVICE      CREATED         STATUS
inventario   it-asset-vulnerability-manager-inventario   "python3 /app/main.py"   inventario   7 seconds ago   Up 7 seconds (healthy)
```

O Compose construiu a imagem, criou o volume `dados` (com o nome do projeto como prefixo) e iniciou o container, que já aparece como `healthy`.

### 2. Teste de persistência

Cadastro de um ativo pelo menu, com `docker attach inventario`:

```
Escolha uma opção: 1
Digite o tipo do ativo: 1
Digite o ID do ativo: 1
Digite o nome do ativo: aaa
Digite o setor do ativo: 1
Digite o nome do responsável pelo ativo: asss
Digite o status do ativo: 1
Digite o sistema operacional do ativo: ma
Digite o tamanho da tela em polegadas: 111
Ativo cadastrado com sucesso!
```

Remoção do container com `down`:

```bash
docker compose down
```

```
 ✔ Container inventario                           Removed
 ✔ Network it-asset-vulnerability-manager_default Removed
```

```bash
docker ps -a
docker volume ls
```

```
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

DRIVER    VOLUME NAME
local     it-asset-vulnerability-manager_dados
```

O container e a rede foram removidos, mas o volume continua existindo.

Criação de um container novo e listagem dos ativos:

```bash
docker compose up -d
docker attach inventario
```

```
Escolha uma opção: 2
Deseja listar todos os ativos, filtrar ou mostrar apenas um?
todos/filtrar/um): todos
Ordenar por (id/nome/vulnerabilidades): id
Listando todos os ativos...

            ID: 1
            Nome: aaa
            Tipo: Notebook
            Setor: TI
            Responsável: asss
            Status: ATIVO
            Sistema operacional: ma
            Tamanho da tela: 111.0 polegadas
```

**Resultado:** o ativo cadastrado no container anterior aparece no container novo. Os dados foram preservados no volume.

### 3. Teste de reinício automático

Encerramento do processo principal pela opção "Sair" do menu:

```
Escolha uma opção: 6
Saindo do programa...
```

Logo em seguida:

```bash
docker compose ps
```

```
NAME         IMAGE                                       COMMAND                  SERVICE      CREATED          STATUS
inventario   it-asset-vulnerability-manager-inventario   "python3 /app/main.py"   inventario   51 seconds ago   Up 5 seconds (healthy)
```

```bash
docker inspect -f '{{.RestartCount}}' inventario
```

```
1
```

**Resultado:** o container foi criado há 51 segundos, mas está em execução há apenas 5. O processo principal terminou e o Docker o reiniciou automaticamente, como mostra a contagem de reinícios igual a 1. O container voltou já como `healthy`.

> Ao conectar ao container com `docker attach`, a mensagem "Opção inválida" aparece porque a tecla Enter foi pressionada para exibir o menu novamente, já que ele foi impresso antes da conexão.