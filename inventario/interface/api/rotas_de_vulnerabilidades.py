from flask import Blueprint, request

from inventario.dominio.excecoes import DadoInvalidoError
from inventario.servicos.vulnerabilidades import registrar_vulnerabilidade_no_catalogo


def criar_rotas_de_vulnerabilidades(repositorio, catalogo):
    rotas = Blueprint("vulnerabilidades", __name__)

    @rotas.get("/vulnerabilidades")
    def listar_vulnerabilidades():
        vulnerabilidades_em_dicionario = []
        for vulnerabilidade in catalogo.values():
            vulnerabilidades_em_dicionario.append(vulnerabilidade.para_dicionario())
        return vulnerabilidades_em_dicionario

    @rotas.post("/vulnerabilidades")
    def cadastrar_vulnerabilidade():
        corpo = request.get_json(silent=True)
        try:
            vulnerabilidade = registrar_vulnerabilidade_no_catalogo(
                repositorio, catalogo, corpo["nome_vulnerabilidade"], corpo["cvss"]
            )
        except DadoInvalidoError as erro:
            return {"erro": str(erro)}, 400
        except (KeyError, TypeError):
            return {"erro": "Dados da vulnerabilidade incompletos ou inválidos."}, 400
        return vulnerabilidade.para_dicionario(), 201

    return rotas
