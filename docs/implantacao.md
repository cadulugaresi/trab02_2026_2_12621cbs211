# Implantação no servidor da faculdade — Trabalho 2 (S5_20)

Roteiro para colocar o sistema no ar no servidor compartilhado da faculdade e comprovar o funcionamento contínuo por, no mínimo, 24 horas.

## ✨ Identificação do projeto

Seguindo a padronização do card S5_20 (`trab02_2026_2_MATRICULA`, em letras minúsculas, sem pontos ou traços):

- **Identificador:** `trab02_2026_2_12621cbs211`
- **Repositório:** `https://github.com/cadulugaresi/trab02_2026_2_12621cbs211`
- **Diretório no servidor:** `~/trab02_2026_2_12621cbs211`
- **Projeto Compose, imagem e container:** `trab02_2026_2_12621cbs211` (definidos no `compose.yaml`)
- **Volume dos dados:** `trab02_2026_2_12621cbs211_dados` (o Compose usa o nome do projeto como prefixo)
- **Porta externa:** 2211 (2000 + os três últimos dígitos da matrícula), ligada à porta 5000 de dentro do container

## 🫧 Antes de começar

- A implantação só acontece depois da liberação do docente.
- O servidor (`10.0.99.150`) tem endereço privado: o acesso é feito de dentro da rede da faculdade.
- Todos os comandos abaixo rodam dentro da pasta do projeto, para não interferir nos projetos dos outros alunos. Nunca usar comandos que afetam o Docker inteiro, como `docker system prune` ou `docker stop $(docker ps -q)`.

## ✨ Passo a passo

### 1. Acessar o servidor e trocar a senha inicial

```bash
ssh MATRICULA@10.0.99.150
passwd
```

A senha inicial é a própria matrícula, que também aparece no identificador do projeto. Trocá-la no primeiro acesso impede que alguém que leia o repositório entre no servidor com o seu usuário.

### 2. Conferir o Docker

```bash
docker --version
docker compose version
```

Se algum dos dois comandos falhar, registrar a mensagem e avisar o docente antes de continuar.

### 3. Baixar o código com o nome padronizado

```bash
cd ~
git clone https://github.com/cadulugaresi/trab02_2026_2_12621cbs211.git trab02_2026_2_12621cbs211
cd trab02_2026_2_12621cbs211
```

### 4. Construir a imagem e subir o container

```bash
docker compose up -d --build
docker compose ps
```

O container `trab02_2026_2_12621cbs211` deve aparecer como `healthy`, com a porta `2211->5000`.

### 5. Testar

No próprio servidor:

```bash
curl http://localhost:2211/saude
```

A resposta esperada é `{"status":"ok"}`. De um computador da rede da faculdade, o sistema abre no navegador em `http://10.0.99.150:2211`.

## 🫧 Evidências das 24 horas

Logo depois de subir e de novo depois de 24 horas, rodar os comandos abaixo e guardar a saída:

```bash
date
docker compose ps
docker inspect -f 'Iniciado em {{.State.StartedAt}} · reinícios: {{.RestartCount}}' trab02_2026_2_12621cbs211
curl http://localhost:2211/saude
docker compose logs --tail 20
```

- `docker compose ps` mostra há quanto tempo o container está no ar (por exemplo, `Up 25 hours (healthy)`).
- `StartedAt` igual nas duas medições prova que o container não foi recriado no meio do período.
- `RestartCount` mostra quantas vezes o Docker precisou reiniciar o processo sozinho, pela política `unless-stopped`.

## ✨ Atualizar o sistema no servidor

```bash
cd ~/trab02_2026_2_12621cbs211
git pull
docker compose up -d --build
```

Os dados continuam, porque ficam no volume. O container é recriado, então a contagem das 24 horas recomeça a partir dessa atualização.
