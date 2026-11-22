import json
import random
import sys
import urllib.error
import urllib.request

from inventario.dominio.enums import (
    Cor,
    Setor,
    SistemaOperacional,
    StatusDaVuln,
    StatusDoAtivo,
    Tecnologia,
)

ENDERECO_PADRAO = "http://localhost:5000"
SEMENTE_DO_SORTEIO = 42
RESPONSAVEL = "Rafael Torres"
ID_DO_ROTEADOR_PRINCIPAL = 1
ID_DO_CONTROLADOR_DE_DOMINIO = 12
ID_DO_SERVIDOR_DE_ARQUIVOS = 10
ID_DO_SERVIDOR_DO_ERP = 15
ID_DO_SERVIDOR_DE_IMPRESSAO = 16

TI = Setor.TI.value
FINANCEIRO = Setor.FINANCEIRO.value
MARKETING = Setor.MARKETING.value
RH = Setor.RH.value
JURIDICO = Setor.JURIDICO.value

ATIVO = StatusDoAtivo.ATIVO.value
INATIVO = StatusDoAtivo.INATIVO.value
EM_MANUTENCAO = StatusDoAtivo.EM_MANUTENCAO.value

ABERTA = StatusDaVuln.ABERTA.value
EM_TRATAMENTO = StatusDaVuln.EM_TRATAMENTO.value
CORRIGIDA = StatusDaVuln.CORRIGIDA.value
ACEITA = StatusDaVuln.ACEITA.value

WINDOWS = SistemaOperacional.WINDOWS.value
MACOS = SistemaOperacional.MACOS.value
LINUX = SistemaOperacional.LINUX.value

ROTEADOR_DE_CADA_SETOR = {TI: 6, FINANCEIRO: 2, MARKETING: 3, RH: 4, JURIDICO: 5}


class DemonstracaoRecusadaError(Exception):
    pass


class ClienteDaApi:

    def __init__(self, endereco):
        self.endereco = endereco.rstrip("/")

    def buscar(self, caminho):
        with urllib.request.urlopen(self.endereco + caminho) as resposta:
            return json.loads(resposta.read())

    def enviar(self, caminho, corpo):
        requisicao = urllib.request.Request(
            self.endereco + caminho,
            data=json.dumps(corpo).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(requisicao) as resposta:
                return json.loads(resposta.read())
        except urllib.error.HTTPError as erro:
            mensagem = json.loads(erro.read())["erro"]
            raise DemonstracaoRecusadaError(f"{caminho}: {mensagem}") from erro


def notebook(sistema_operacional, tela):
    return {"sistema_operacional": sistema_operacional, "tela": tela}


def servidor(ram, armazenamento):
    return {"ram": ram, "armazenamento": armazenamento}


def roteador(portas, velocidade):
    return {"portas": portas, "velocidade": velocidade}


def impressora(cor, tecnologia):
    return {"cor": cor.value, "tecnologia": tecnologia.value}


ATIVOS = [
    (1, "Roteador", "Roteador principal", TI, ATIVO, roteador(48, 10000)),
    (2, "Roteador", "Roteador do financeiro", FINANCEIRO, ATIVO, roteador(24, 1000)),
    (3, "Roteador", "Roteador do marketing", MARKETING, EM_MANUTENCAO, roteador(24, 1000)),
    (4, "Roteador", "Roteador do RH", RH, ATIVO, roteador(16, 1000)),
    (5, "Roteador", "Roteador do jurídico", JURIDICO, ATIVO, roteador(16, 1000)),
    (6, "Roteador", "Roteador da sala de reuniões", TI, ATIVO, roteador(8, 1000)),
    (7, "Servidor", "Servidor web", TI, ATIVO, servidor(64, 2.0)),
    (8, "Servidor", "Banco de dados", TI, ATIVO, servidor(128, 8.0)),
    (9, "Servidor", "Servidor de e-mail", TI, ATIVO, servidor(32, 4.0)),
    (10, "Servidor", "Servidor de arquivos", TI, ATIVO, servidor(32, 16.0)),
    (11, "Servidor", "Servidor de backup", TI, ATIVO, servidor(16, 32.0)),
    (12, "Servidor", "Controlador de domínio", TI, ATIVO, servidor(16, 1.0)),
    (13, "Servidor", "Servidor de VPN", TI, ATIVO, servidor(8, 0.5)),
    (14, "Servidor", "Servidor de monitoramento", TI, EM_MANUTENCAO, servidor(16, 2.0)),
    (15, "Servidor", "Servidor do ERP", FINANCEIRO, ATIVO, servidor(64, 4.0)),
    (16, "Servidor", "Servidor de impressão", TI, ATIVO, servidor(8, 0.5)),
    (17, "Notebook", "Notebook do Rafael", TI, ATIVO, notebook(LINUX, 14.0)),
    (18, "Notebook", "Notebook do suporte 1", TI, ATIVO, notebook(WINDOWS, 14.0)),
    (19, "Notebook", "Notebook do suporte 2", TI, INATIVO, notebook(WINDOWS, 14.0)),
    (20, "Notebook", "Notebook do financeiro 1", FINANCEIRO, ATIVO, notebook(WINDOWS, 14.0)),
    (21, "Notebook", "Notebook do financeiro 2", FINANCEIRO, ATIVO, notebook(WINDOWS, 14.0)),
    (22, "Notebook", "Notebook do financeiro 3", FINANCEIRO, ATIVO, notebook(WINDOWS, 15.6)),
    (23, "Notebook", "Notebook da diretoria", FINANCEIRO, ATIVO, notebook(MACOS, 16.0)),
    (24, "Notebook", "Notebook do marketing 1", MARKETING, ATIVO, notebook(MACOS, 16.0)),
    (25, "Notebook", "Notebook do marketing 2", MARKETING, ATIVO, notebook(MACOS, 14.0)),
    (26, "Notebook", "Notebook do marketing 3", MARKETING, EM_MANUTENCAO, notebook(WINDOWS, 14.0)),
    (27, "Notebook", "Notebook do RH 1", RH, ATIVO, notebook(WINDOWS, 14.0)),
    (28, "Notebook", "Notebook do RH 2", RH, ATIVO, notebook(WINDOWS, 15.6)),
    (29, "Notebook", "Notebook do jurídico 1", JURIDICO, ATIVO, notebook(WINDOWS, 14.0)),
    (30, "Notebook", "Notebook do jurídico 2", JURIDICO, INATIVO, notebook(WINDOWS, 15.6)),
    (
        31,
        "Impressora",
        "Impressora do RH",
        RH,
        ATIVO,
        impressora(Cor.PRETA_E_BRANCA, Tecnologia.LASER),
    ),
    (
        32,
        "Impressora",
        "Impressora do financeiro",
        FINANCEIRO,
        ATIVO,
        impressora(Cor.PRETA_E_BRANCA, Tecnologia.LASER),
    ),
    (
        33,
        "Impressora",
        "Impressora do marketing",
        MARKETING,
        ATIVO,
        impressora(Cor.COLORIDA, Tecnologia.TINTA),
    ),
    (
        34,
        "Impressora",
        "Impressora do jurídico",
        JURIDICO,
        ATIVO,
        impressora(Cor.PRETA_E_BRANCA, Tecnologia.LASER),
    ),
    (
        35,
        "Impressora",
        "Impressora da recepção",
        TI,
        ATIVO,
        impressora(Cor.COLORIDA, Tecnologia.LASER),
    ),
    (
        36,
        "Impressora",
        "Impressora da diretoria",
        FINANCEIRO,
        EM_MANUTENCAO,
        impressora(Cor.COLORIDA, Tecnologia.LASER),
    ),
]

VULNERABILIDADES = [
    ("Log4Shell", 10.0),
    ("SMBv1 ativo", 9.8),
    ("BlueKeep no RDP", 9.8),
    ("PrintNightmare", 8.8),
    ("Porta de gerenciamento exposta", 8.6),
    ("Senha padrão no painel", 8.1),
    ("Windows sem atualização de segurança", 7.8),
    ("Heartbleed", 7.5),
    ("SSH com senha fraca", 7.4),
    ("Compartilhamento de rede aberto", 6.8),
    ("Telnet habilitado", 6.5),
    ("Navegador desatualizado", 6.1),
    ("Antivírus desativado", 5.5),
    ("Firmware desatualizado", 5.3),
    ("Macros do Office habilitadas", 4.3),
    ("Certificado TLS expirado", 3.1),
]

VULNERABILIDADES_POSSIVEIS_DE_CADA_TIPO = {
    "Servidor": [
        "Log4Shell",
        "SMBv1 ativo",
        "Heartbleed",
        "SSH com senha fraca",
        "Certificado TLS expirado",
        "Compartilhamento de rede aberto",
        "Windows sem atualização de segurança",
    ],
    "Roteador": [
        "Senha padrão no painel",
        "Firmware desatualizado",
        "Telnet habilitado",
        "Porta de gerenciamento exposta",
        "SSH com senha fraca",
    ],
    "Notebook": [
        "Windows sem atualização de segurança",
        "Navegador desatualizado",
        "Antivírus desativado",
        "Macros do Office habilitadas",
        "BlueKeep no RDP",
        "SMBv1 ativo",
    ],
    "Impressora": [
        "PrintNightmare",
        "Firmware desatualizado",
        "Senha padrão no painel",
        "Telnet habilitado",
    ],
}

VINCULOS_FIXOS = {
    ID_DO_ROTEADOR_PRINCIPAL: [
        ("Firmware desatualizado", ABERTA),
        ("Telnet habilitado", EM_TRATAMENTO),
        ("Porta de gerenciamento exposta", ABERTA),
    ],
    ID_DO_CONTROLADOR_DE_DOMINIO: [
        ("SMBv1 ativo", ABERTA),
        ("Windows sem atualização de segurança", EM_TRATAMENTO),
        ("Certificado TLS expirado", CORRIGIDA),
    ],
}

STATUS_PARA_SORTEAR = [ABERTA] * 35 + [EM_TRATAMENTO] * 20 + [CORRIGIDA] * 35 + [ACEITA] * 10

DEPENDENCIAS_DA_INFRAESTRUTURA = [
    (2, 1, 0.4),
    (3, 1, 0.4),
    (4, 1, 0.4),
    (5, 1, 0.4),
    (6, 1, 0.4),
    (7, 1, 0.3),
    (7, 8, 0.4),
    (9, 1, 0.3),
    (9, 12, 0.2),
    (10, 1, 0.3),
    (10, 12, 0.2),
    (11, 10, 0.3),
    (11, 8, 0.3),
    (12, 1, 0.3),
    (13, 1, 0.5),
    (13, 12, 0.2),
    (14, 1, 0.3),
    (15, 8, 0.4),
    (15, 2, 0.2),
    (16, 12, 0.2),
    (16, 1, 0.2),
]


def cadastrar_ativos(cliente):
    for id_ativo, tipo, nome, setor, status, campos_do_tipo in ATIVOS:
        corpo = {
            "id": id_ativo,
            "tipo": tipo,
            "nome": nome,
            "setor": setor,
            "responsavel": RESPONSAVEL,
            "status": status,
        }
        corpo.update(campos_do_tipo)
        cliente.enviar("/ativos", corpo)


def cadastrar_vulnerabilidades(cliente):
    ids_pelo_nome = {}
    for nome, cvss in VULNERABILIDADES:
        vulnerabilidade = cliente.enviar(
            "/vulnerabilidades", {"nome_vulnerabilidade": nome, "cvss": cvss}
        )
        ids_pelo_nome[nome] = vulnerabilidade["id_vulnerabilidade"]
    return ids_pelo_nome


def vincular(cliente, id_ativo, id_vulnerabilidade, status_tratamento):
    cliente.enviar(
        f"/ativos/{id_ativo}/vulnerabilidades",
        {"id_vulnerabilidade": id_vulnerabilidade, "status_tratamento": status_tratamento},
    )


def vincular_vulnerabilidades(cliente, ids_pelo_nome, sorteio):
    for id_ativo, vinculos in VINCULOS_FIXOS.items():
        for nome_da_vulnerabilidade, status_tratamento in vinculos:
            vincular(cliente, id_ativo, ids_pelo_nome[nome_da_vulnerabilidade], status_tratamento)

    for id_ativo, tipo, _, _, _, _ in ATIVOS:
        if id_ativo in VINCULOS_FIXOS:
            continue
        menor_quantidade = 1 if tipo == "Servidor" else 0
        quantidade = sorteio.randint(menor_quantidade, 4)
        possiveis = VULNERABILIDADES_POSSIVEIS_DE_CADA_TIPO[tipo]
        for nome_da_vulnerabilidade in sorteio.sample(possiveis, quantidade):
            status_tratamento = sorteio.choice(STATUS_PARA_SORTEAR)
            vincular(cliente, id_ativo, ids_pelo_nome[nome_da_vulnerabilidade], status_tratamento)


def montar_dependencias(sorteio):
    dependencias = list(DEPENDENCIAS_DA_INFRAESTRUTURA)
    for id_ativo, tipo, _, setor, _, _ in ATIVOS:
        if tipo == "Notebook":
            dependencias.append((id_ativo, ROTEADOR_DE_CADA_SETOR[setor], 0.3))
            dependencias.append((id_ativo, ID_DO_CONTROLADOR_DE_DOMINIO, 0.1))
            if setor == FINANCEIRO:
                dependencias.append((id_ativo, ID_DO_SERVIDOR_DO_ERP, 0.2))
            elif sorteio.random() < 0.5:
                dependencias.append((id_ativo, ID_DO_SERVIDOR_DE_ARQUIVOS, 0.1))
        elif tipo == "Impressora":
            dependencias.append((id_ativo, ROTEADOR_DE_CADA_SETOR[setor], 0.2))
            dependencias.append((id_ativo, ID_DO_SERVIDOR_DE_IMPRESSAO, 0.3))
    return dependencias


def cadastrar_dependencias(cliente, dependencias):
    for id_ativo, id_ativo_do_qual_depende, fracao in dependencias:
        cliente.enviar(
            f"/ativos/{id_ativo}/dependencias",
            {"id_ativo_do_qual_depende": id_ativo_do_qual_depende, "fracao": fracao},
        )


def carregar_demonstracao(cliente):
    if cliente.buscar("/ativos"):
        raise DemonstracaoRecusadaError(
            "O banco já tem ativos. A demonstração só é carregada num banco vazio, "
            "para nunca se misturar com dados de verdade."
        )
    sorteio = random.Random(SEMENTE_DO_SORTEIO)
    cadastrar_ativos(cliente)
    ids_pelo_nome = cadastrar_vulnerabilidades(cliente)
    vincular_vulnerabilidades(cliente, ids_pelo_nome, sorteio)
    cadastrar_dependencias(cliente, montar_dependencias(sorteio))


if __name__ == "__main__":
    endereco = sys.argv[1] if len(sys.argv) > 1 else ENDERECO_PADRAO
    try:
        carregar_demonstracao(ClienteDaApi(endereco))
    except urllib.error.URLError:
        raise SystemExit(f"Não foi possível falar com a API em {endereco}. Ela está rodando?")
    except DemonstracaoRecusadaError as erro:
        raise SystemExit(f"Demonstração não carregada: {erro}")
    print(
        f"Demonstração carregada em {endereco}: {len(ATIVOS)} ativos "
        f"e {len(VULNERABILIDADES)} vulnerabilidades, com vínculos e dependências."
    )
