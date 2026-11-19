# Docker — Trabalho 2 (S4_16, S4_17 e S4_05)

Este documento registra a conteinerização do sistema de gerenciamento de ativos e vulnerabilidades: a construção da imagem Docker (S4_16), a configuração com Docker Compose, com volume, política de reinício e healthcheck (S4_17), e a troca do menu interativo pelo servidor da API HTTP como processo principal do container (S4_05), junto com as evidências de execução e dos testes.

**Aluno:** Cadu Lugaresi — Cibersegurança UFU, Turma 2
**Ambiente:** MacBook Air (Apple Silicon) com Docker Desktop v4.98.0 e Docker 29.9.2

---

## ✨ O que o container executa

O container executa o **servidor da API** (`iniciar_api.py`), e não mais o menu interativo. O servidor escuta em `0.0.0.0:5000` e responde às rotas HTTP do sistema (`/saude`, `/ativos`, `/vulnerabilidades`, `/riscos`...), sem precisar de terminal nem de teclado.

O menu (`main.py`) continua existindo, mas só para uso local no terminal, com `python3 main.py`. Ele não entra na imagem: se o menu gravasse no mesmo banco enquanto a API está no ar, os dados que a API carregou na memória ficariam desatualizados. No container, só o servidor da API escreve no banco.

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
[EVIDÊNCIA: colar a saída de docker build -t inventario:2.0 .]
```

### 2. Tamanho da imagem

```bash
docker images inventario
```

```
[EVIDÊNCIA: colar a saída de docker images inventario]
```

### 3. Execução da API no container

Com o container do Compose parado (`docker compose down`), para não haver conflito de nome nem de porta:

```bash
docker run -d -p 5000:5000 --name inventario inventario:2.0
curl http://localhost:5000/saude
curl http://localhost:5000/ativos
```

```
[EVIDÊNCIA: colar a saída de curl http://localhost:5000/saude]
```

```
[EVIDÊNCIA: colar a saída de curl http://localhost:5000/ativos]
```

### 4. Usuário sem privilégios

Com o container em execução:

```bash
docker exec inventario whoami
```

```
[EVIDÊNCIA: colar a saída de docker exec inventario whoami]
```

### 5. Healthcheck

```bash
docker ps
```

Logo após a inicialização, e de novo depois de 30 segundos:

```
[EVIDÊNCIA: colar as duas saídas de docker ps, com o STATUS passando de health: starting para healthy]
```

O status `healthy` confirma que a API respondeu à rota `/saude` dentro do container.

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
[EVIDÊNCIA: colar a saída de docker compose up -d --build]
```

```bash
docker compose ps
```

```
[EVIDÊNCIA: colar a saída de docker compose ps]
```

```bash
curl http://localhost:5000/saude
```

```
[EVIDÊNCIA: colar a saída de curl http://localhost:5000/saude]
```

### 2. Teste de persistência

Cadastro de um ativo pela API:

```bash
curl -X POST http://localhost:5000/ativos \
  -H "Content-Type: application/json" \
  -d '{"tipo": "Notebook", "id": 10, "nome": "Notebook do Rafael", "setor": 1, "responsavel": "Rafael Torres", "status": 1, "sistema_operacional": "Linux", "tela": 14.0}'
```

```
[EVIDÊNCIA: colar a saída do POST /ativos, com o ativo cadastrado]
```

Remoção do container com `down`:

```bash
docker compose down
docker ps -a
docker volume ls
```

```
[EVIDÊNCIA: colar as saídas de docker compose down, docker ps -a e docker volume ls]
```

Criação de um container novo e busca do ativo:

```bash
docker compose up -d
curl http://localhost:5000/ativos/10
```

```
[EVIDÊNCIA: colar a saída de curl http://localhost:5000/ativos/10]
```

**Resultado esperado:** o ativo cadastrado no container anterior aparece no container novo, porque o banco ficou guardado no volume.

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
[EVIDÊNCIA: colar a saída de docker compose ps, mostrando o container criado há mais tempo do que está em execução]
```

```
[EVIDÊNCIA: colar a saída de docker inspect -f '{{.RestartCount}}' inventario]
```

**Resultado esperado:** a contagem de reinícios aumenta em 1, e o container volta a responder em `/saude`, já como `healthy`.
