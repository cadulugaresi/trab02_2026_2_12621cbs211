from flask import Blueprint, request

from inventario.dominio.enums import StatusDaVuln
from inventario.dominio.excecoes import DadoInvalidoError
from inventario.dominio.validacoes import validar_inteiro_positivo
from inventario.servicos.vulnerabilidades import vincular_vulnerabilidade


def criar_rotas_de_vinculos(repositorio, ativos, catalogo):
    rotas = Blueprint("vinculos", __name__)

    @rotas.post("/ativos/<int:id_ativo>/vulnerabilidades")
    def vincular_vulnerabilidade_ao_ativo(id_ativo):
        corpo = request.get_json(silent=True)
        try:
            status_da_vuln = StatusDaVuln(validar_inteiro_positivo(corpo["status_tratamento"]))
            vincular_vulnerabilidade(
                repositorio,
                ativos,
                catalogo,
                id_ativo,
                corpo["id_vulnerabilidade"],
                status_da_vuln,
            )
        except DadoInvalidoError as erro:
            return {"erro": str(erro)}, 400
        except (KeyError, ValueError, TypeError):
            return {"erro": "Dados incompletos ou inválidos."}, 400
        return ativos[id_ativo].para_dicionario(), 201

    return rotas
