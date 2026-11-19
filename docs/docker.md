# Docker — Trabalho 2 (S4_16, S4_17 e S4_05)

Este documento registra a conteinerização do sistema de gerenciamento de ativos e vulnerabilidades: a construção da imagem Docker (S4_16), a configuração com Docker Compose, com volume, política de reinício e healthcheck (S4_17), e a troca do menu interativo pelo servidor da API HTTP como processo principal do container (S4_05), junto com as evidências de execução e dos testes.

**Aluno:** Cadu Lugaresi — Cibersegurança UFU, Turma 2
**Ambiente:** MacBook Air (Apple Silicon) com Docker Desktop v4.98.0 e Docker 29.9.2

---

## ✨ O que o container executa

O container executa o **servidor da API** (`iniciar_api.py`), e não mais o menu interativo. O servidor escuta em `0.0.0.0:5000` e responde às rotas HTTP do sistema (`/saude`, `/ativos`, `/vulnerabilidades`, `/riscos`...), sem precisar de terminal nem de teclado.

O menu (`main.py`) continua existindo, mas só para uso local no terminal, com `python3 main.py`. Ele não entra na imagem: se o menu gravasse no mesmo banco enquanto a API está no ar, os dados que a API carregou na memória ficariam desatualizados. No container, só o servidor da API escreve no banco.

**Por que o servidor usa `threaded=False`:** o `iniciar_api.py` liga o servidor com `app.run(host="0.0.0.0", port=5000, threaded=False)`. Por padrão, o servidor do Flask atende cada requisição numa thread nova. A conexão do `RepositorioSQLite` é criada uma vez, na thread principal, quando o servidor parte, e o módulo `sqlite3` do Python não permite usar uma conexão numa thread diferente da que a criou: com as threads ligadas, toda requisição que grava no banco (os `POST`) falhava com `sqlite3.ProgrammingError` e devolvia 500. Com `threaded=False`, todas as requisições são atendidas uma por vez, na mesma thread em que a conexão foi criada. Isso também impede que duas requisições alterem ao mesmo tempo os dicionários `ativos` e `catalogo`, que ficam na memória do servidor. Os testes da API não pegavam o problema porque o `test_client()` executa as requisições na mesma thread do teste. Para o volume de uso deste trabalho, atender uma requisição por vez não é uma limitação.

**Por que o menu não servia como processo do container:** um container permanece em execução enquanto o seu processo principal estiver rodando. O menu passa a maior parte do tempo parado no `input()`, esperando alguém digitar. Sem um terminal ligado ao container, não existe essa entrada, e mantê-lo vivo exigia `stdin_open`, `tty` e `docker attach`. O servidor da API não depende de entrada: ele fica escutando a porta e atendendo requisições enquanto o container existir.

## 🫧 Dockerfile

```dockerfile
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

RUN useradd --create-home inventario && mkdir -p /app/dados && chown inventario /app/dados

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY iniciar_api.py .
COPY inventario/ inventario/

USER inventario

WORKDIR /app/dados

HEALTHCHECK CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/saude')"

EXPOSE 5000
CMD ["python3", "/app/iniciar_api.py"]
```

### Decisões

- **Imagem base `python:3.13-slim`:** mesma versão do Python usada no workflow de testes do GitHub Actions, numa variante enxuta da imagem oficial.
- **Dependências em `requirements.txt`:** o programa usa `numpy` (cálculo de risco) e `flask` (servidor da API). O `requirements.txt` é copiado e instalado **antes** do código: como as dependências mudam bem menos que o código, a camada do `pip install` é reaproveitada do cache na maior parte das construções.
- **Ordem das instruções:** a criação do usuário e da pasta de dados e a instalação das dependências vêm antes da cópia do código. Assim, alterações no código não invalidam o cache dessas camadas, e só as camadas a partir do `COPY` do código são reconstruídas.
- **Só o ponto de entrada da API entra na imagem:** o `COPY iniciar_api.py .` substituiu o `COPY main.py .`, pelo motivo explicado em "O que o container executa".
- **Usuário sem privilégios:** o programa roda com o usuário `inventario`, e não como `root`. Se a aplicação for comprometida, o invasor não tem privilégios de administrador dentro do container.
- **Pasta de dados `/app/dados`:** o banco SQLite é criado no diretório de trabalho (`inventario.db`). Executar o programa a partir de `/app/dados` separa os dados do código sem alterar nenhuma linha da aplicação. A pasta pertence ao usuário `inventario`, que precisa de permissão de escrita para gravar o banco.
- **`PYTHONDONTWRITEBYTECODE=1`:** evita a criação de arquivos `__pycache__` dentro do container.
- **`PYTHONUNBUFFERED=1`:** antes, essa variável era necessária para o menu interativo aparecer no terminal. Com a API, ela continua útil por outro motivo: quando a saída do Python não está ligada a um terminal, como num container em segundo plano, o `print` guarda as mensagens num buffer e só as escreve em blocos. Com a variável, mensagens como o erro de persistência impresso pelo `iniciar_api.py` aparecem na hora em `docker compose logs`, e não se perdem se o processo terminar antes de o buffer ser esvaziado.
- **`EXPOSE 5000`:** documenta a porta em que o servidor escuta dentro do container. A publicação da porta para fora é feita no `compose.yaml`.
- **Healthcheck:** faz uma requisição à rota `GET /saude` da própria API. Se o servidor não responder, ou responder com um status de erro, o `urlopen` levanta uma exceção, o comando termina com código diferente de zero e a verificação falha. A imagem slim não tem `curl`, então o teste usa o próprio Python, sem instalar nenhum pacote a mais.

## ✨ .dockerignore

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

## 🫧 Evidências de execução da imagem

> As evidências da versão com o menu interativo (S4_16) continuam registradas no histórico do Git deste arquivo.

### 1. Construção da imagem

```bash
docker build -t inventario:2.0 .
```

```
#0 building with "desktop-linux" instance using docker driver

#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 540B 0.0s done
#1 DONE 0.0s

[... trecho omitido: metadados da imagem base, .dockerignore e contexto ...]

#6 [2/8] RUN useradd --create-home inventario && mkdir -p /app/dados && chown inventario /app/dados
#6 CACHED

#7 [3/8] WORKDIR /app
#7 CACHED

#8 [4/8] COPY requirements.txt .
#8 CACHED

#9 [5/8] RUN pip install --no-cache-dir -r requirements.txt
#9 CACHED

#10 [6/8] COPY iniciar_api.py .
#10 DONE 0.0s

#11 [7/8] COPY inventario/ inventario/
#11 DONE 0.0s

#12 [8/8] WORKDIR /app/dados
#12 DONE 0.0s

#13 exporting to image
#13 exporting layers 0.0s done
#13 exporting manifest sha256:7538a187e3d00127b1677c1ca28701a202dbdb5ba8500ff2a85e4134aeca04e5 done
#13 exporting config sha256:b4c7ef13c2921b34686f3ccab41ca3eaf1b8464fb172b371ab4302a56429137d done
#13 exporting attestation manifest sha256:f35a85b5e1898549f839977df78ad3319b2a740dc4f2aa4cb6561836772ffd85 done
#13 exporting manifest list sha256:0ade52cb9bae09888a43953c1189bde47bb73259b94dd30ab6cdde58b36243e2 done
#13 naming to docker.io/library/inventario:2.0 done
#13 unpacking to docker.io/library/inventario:2.0 0.0s done
#13 DONE 0.1s
```

As etapas 2 a 5, inclusive o `pip install`, foram reaproveitadas do cache (`CACHED`). Só as camadas a partir do `COPY iniciar_api.py` foram refeitas, porque apenas o código mudou: é o efeito de copiar e instalar o `requirements.txt` antes do código.

### 2. Tamanho da imagem

```bash
docker images inventario
```

```
IMAGE            ID             DISK USAGE   CONTENT SIZE   EXTRA
inventario:1.0   82670bec2eec        202MB         43.4MB        
inventario:2.0   0ade52cb9bae        296MB         64.5MB        
```

A imagem `2.0` é maior que a `1.0` (a versão com o menu, do S4_16) porque passou a instalar as dependências do `requirements.txt`, `numpy` e `flask`.

### 3. Execução da API no container

Com o container do Compose parado (`docker compose down`), para não haver conflito de nome nem de porta:

```bash
docker run -d -p 5000:5000 --name inventario inventario:2.0
curl http://localhost:5000/saude
curl http://localhost:5000/ativos
```

```
{"status":"ok"}
```

```
[]
```

A API respondeu de fora do container, pela porta publicada. A lista de ativos está vazia porque este container não tem volume: o banco foi criado do zero dentro dele.

### 4. Usuário sem privilégios

Com o container em execução:

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
CONTAINER ID   IMAGE            COMMAND                  CREATED         STATUS                           PORTS                                         NAMES
41f762faa02e   inventario:2.0   "python3 /app/inicia…"   2 seconds ago   Up 1 second (health: starting)   0.0.0.0:5000->5000/tcp, [::]:5000->5000/tcp   inventario
```

Após o primeiro intervalo de verificação (30 segundos):

```
CONTAINER ID   IMAGE            COMMAND                  CREATED          STATUS                    PORTS                                         NAMES
41f762faa02e   inventario:2.0   "python3 /app/inicia…"   46 seconds ago   Up 45 seconds (healthy)   0.0.0.0:5000->5000/tcp, [::]:5000->5000/tcp   inventario
```

O status passou de `health: starting` para `healthy`, confirmando que a API respondeu à rota `/saude` dentro do container.

Depois dessas evidências, o container avulso foi removido (`docker stop inventario` e `docker rm inventario`), para liberar o nome e a porta para o Compose.

---

## ✨ Limitação da imagem sozinha

Após remover o container com `docker rm` e criar um novo a partir da mesma imagem, os ativos cadastrados anteriormente não aparecem mais na listagem. O banco `inventario.db` é criado dentro do container, em `/app/dados`, e é apagado junto com ele. A configuração com Docker Compose resolve isso montando um volume nessa pasta.

---

## 🫧 compose.yaml

```yaml
services:
  inventario:
    build: .
    container_name: inventario
    restart: unless-stopped
    ports:
      - "5000:5000"
    volumes:
      - "dados:/app/dados"
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:5000/saude')"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s

volumes:
  dados:
```

### Decisões

- **`build: .`:** a imagem é construída a partir do Dockerfile do projeto, então o Compose sempre usa a versão atual do código.
- **Sem `stdin_open` e `tty`:** essas opções existiam para manter o `input()` do menu aberto no container. O servidor da API não lê do teclado, então elas foram removidas, junto com o uso de `docker attach` e do atalho Ctrl + P, Ctrl + Q para se desconectar do menu.
- **`ports: "5000:5000"`:** publica a porta no formato `PORTA_DO_COMPUTADOR:PORTA_DO_CONTAINER`. O container tem a própria rede, e sem essa linha nenhuma requisição de fora chegaria à API. O servidor escuta em `0.0.0.0`, e não em `localhost`, justamente para aceitar as requisições que chegam por essa porta publicada: dentro do container, `localhost` seria só o próprio container.
- **Volume nomeado `dados` em `/app/dados`:** é a pasta onde o banco SQLite é criado. O volume é gerenciado pelo Docker e existe independentemente do container, então os dados sobrevivem quando o container é removido ou recriado.
- **Política de reinício `unless-stopped`:** um servidor não termina sozinho em funcionamento normal. Se o processo principal parar, por uma exceção não tratada, por ter sido interrompido ou porque o Docker ou a máquina reiniciaram, o Docker inicia o container de novo. A exceção é quando o container é parado manualmente, o que permite desligá-lo de propósito para manutenção. É essa política que sustenta o requisito de manter a aplicação no ar por 24 horas. A política `on-failure` reinicia apenas quando o processo termina com código de erro, e um serviço que precisa ficar no ar não deve depender do motivo pelo qual parou. A política `always` não respeitaria uma parada manual depois de o Docker reiniciar.
- **Healthcheck:** o mesmo teste do Dockerfile (requisição a `GET /saude`), com os parâmetros explícitos: verificação a cada 30 segundos, limite de 5 segundos por verificação, 3 falhas seguidas para marcar o container como `unhealthy` e 10 segundos de tolerância na inicialização. O healthcheck **não reinicia** o container: ele só informa o estado (`healthy` ou `unhealthy`) em `docker ps`. O reinício é feito pela política `unless-stopped`, quando o processo principal termina. As duas configurações se complementam: o healthcheck detecta uma API que está rodando mas não responde, e a política de reinício traz de volta uma API que parou.

---

## ✨ Evidências do Docker Compose

> As evidências da versão com o menu interativo (S4_17), feitas com `docker attach`, continuam registradas no histórico do Git deste arquivo.

### 1. Subida da aplicação

```bash
docker compose up -d --build
```

```
 Image it-asset-vulnerability-manager-inventario Building 
#1 [internal] load local bake definitions
#1 reading from stdin 640B done
#1 DONE 0.0s

[... trecho omitido: as mesmas etapas de construção da imagem mostradas na seção anterior ...]

 Image it-asset-vulnerability-manager-inventario Built 
 Network it-asset-vulnerability-manager_default Creating 
 Network it-asset-vulnerability-manager_default Creating 
 Network it-asset-vulnerability-manager_default Created 
 Network it-asset-vulnerability-manager_default Created 
 Container inventario Creating 
 Container inventario Created 
 Container inventario Starting 
 Container inventario Started 
```

```bash
docker compose ps
```

```
NAME         IMAGE                                       COMMAND                  SERVICE      CREATED         STATUS                   PORTS
inventario   it-asset-vulnerability-manager-inventario   "python3 /app/inicia…"   inventario   6 seconds ago   Up 5 seconds (healthy)   0.0.0.0:5000->5000/tcp, [::]:5000->5000/tcp
```

```bash
curl http://localhost:5000/saude
```

```
{"status":"ok"}
```

O Compose construiu a imagem, criou a rede e iniciou o container, que já aparece como `healthy` e com a porta 5000 publicada. O volume `dados` não aparece sendo criado porque já existia de execuções anteriores.

### 2. Teste de persistência

Cadastro de um ativo pela API:

```bash
curl -X POST http://localhost:5000/ativos \
  -H "Content-Type: application/json" \
  -d '{"tipo": "Notebook", "id": 10, "nome": "Notebook do Rafael", "setor": 1, "responsavel": "Rafael Torres", "status": 1, "sistema_operacional": "Linux", "tela": 14.0}'
```

```
{"dependencias":[],"fator_exposicao":1.2,"id":10,"nome":"Notebook do Rafael","responsavel":"Rafael Torres","setor":1,"sistema_operacional":"Linux","status":1,"tela":14.0,"tipo":"Notebook","vulnerabilidades":[]}
```

O ativo foi gravado e devolvido com o fator de exposição padrão do Notebook (1.2), já que o corpo não informou um.

Remoção do container com `down`:

```bash
docker compose down
docker ps -a
docker volume ls
```

```
 Container inventario Stopping 
 Container inventario Stopped 
 Container inventario Removing 
 Container inventario Removed 
 Network it-asset-vulnerability-manager_default Removing 
 Network it-asset-vulnerability-manager_default Removed 
```

```
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

```
DRIVER    VOLUME NAME
local     it-asset-vulnerability-manager_dados
```

O container e a rede foram removidos, mas o volume continua existindo.

Criação de um container novo e busca do ativo:

```bash
docker compose up -d
curl http://localhost:5000/ativos/10
```

```
{"dependencias":[],"fator_exposicao":1.2,"id":10,"nome":"Notebook do Rafael","responsavel":"Rafael Torres","setor":1,"sistema_operacional":"Linux","status":1,"tela":14.0,"tipo":"Notebook","vulnerabilidades":[]}
```

**Resultado:** o ativo cadastrado no container anterior aparece no container novo. Os dados foram preservados no volume.

### 3. Teste de reinício automático

Interrupção do processo principal da API, de dentro do container:

```bash
docker exec inventario sh -c "kill -INT 1"
```

O processo principal do container tem o PID 1. O sinal `INT` é o mesmo que o Ctrl + C envia, e faz o servidor terminar.

Logo em seguida:

```bash
docker compose ps
docker inspect -f '{{.RestartCount}}' inventario
```

```
NAME         IMAGE                                       COMMAND                  SERVICE      CREATED          STATUS                   PORTS
inventario   it-asset-vulnerability-manager-inventario   "python3 /app/inicia…"   inventario   35 seconds ago   Up 6 seconds (healthy)   0.0.0.0:5000->5000/tcp, [::]:5000->5000/tcp
```

```
1
```

**Resultado:** o container foi criado há 35 segundos, mas está em execução há apenas 6. O processo principal terminou e o Docker o reiniciou automaticamente, como mostra a contagem de reinícios igual a 1. O container voltou já como `healthy`.
