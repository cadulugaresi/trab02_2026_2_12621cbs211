from flask import Blueprint

from inventario.dominio.ativo import MAPA_DE_TIPOS
from inventario.dominio.enums import Cor, Setor, StatusDaVuln, StatusDoAtivo, Tecnologia


def listar_opcoes_do_enum(enum):
    opcoes = []
    for membro in enum:
        opcoes.append({"valor": membro.value, "nome": membro.name})
    return opcoes


def criar_rotas_de_opcoes():
    rotas = Blueprint("opcoes", __name__)

    @rotas.get("/opcoes")
    def listar_opcoes():
        tipos = []
        for nome_do_tipo, classe in MAPA_DE_TIPOS.items():
            tipos.append(
                {"nome": nome_do_tipo, "fator_exposicao_padrao": classe.FATOR_EXPOSICAO_PADRAO}
            )

        return {
            "tipos": tipos,
            "setores": listar_opcoes_do_enum(Setor),
            "status_do_ativo": listar_opcoes_do_enum(StatusDoAtivo),
            "status_de_tratamento": listar_opcoes_do_enum(StatusDaVuln),
            "cores": listar_opcoes_do_enum(Cor),
            "tecnologias": listar_opcoes_do_enum(Tecnologia),
        }

    return rotas
