from enum import Enum


class StatusDoAtivo(Enum):
    ATIVO = 1
    INATIVO = 2
    EM_MANUTENCAO = 3


class NivelDaVulnerabilidade(Enum):
    BAIXO = 1
    MEDIO = 2
    ALTO = 3
    CRITICO = 4


class Setor(Enum):
    TI = 1
    FINANCEIRO = 2
    MARKETING = 3
    RH = 4
    JURIDICO = 5


class Cor(Enum):
    COLORIDA = 1
    PRETA_E_BRANCA = 2


class Tecnologia(Enum):
    TINTA = 1
    LASER = 2


class StatusDaVuln(Enum):
    ABERTA = 1
    EM_TRATAMENTO = 2
    CORRIGIDA = 3
    ACEITA = 4
