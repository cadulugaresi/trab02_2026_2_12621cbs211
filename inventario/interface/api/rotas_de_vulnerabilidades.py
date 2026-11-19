from flask import Blueprint, request

from inventario.dominio.vulnerabilidade import Vulnerabilidade
from inventario.interface.api.requisicoes import valor_enviado_ou_atual
from inventario.interface.api.respostas import vulnerabilidade_para_resposta
from inventario.servicos.vulnerabilidades import (
    atualizar_vulnerabilidade_no_catalogo,
    excluir_vulnerabilidade_do_catalogo,
    obter_vulnerabilidade,
    registrar_vulnerabilidade_no_catalogo,
)

MENSAGEM_DE_DADOS_INVALIDOS = "Dados da vulnerabilidade incompletos ou inválidos."


def criar_rotas_de_vulnerabilidades(repositorio, ativos, catalogo):
    rotas = Blueprint("vulnerabilidades", __name__)

    @rotas.get("/vulnerabilidades")
    def listar_vulnerabilidades():
        vulnerabilidades_em_dicionario = []
        for vulnerabilidade in catalogo.values():
            vulnerabilidades_em_dicionario.append(vulnerabilidade_para_resposta(vulnerabilidade))
        return vulnerabilidades_em_dicionario

    @rotas.get("/vulnerabilidades/<int:id_vulnerabilidade>")
    def buscar_vulnerabilidade(id_vulnerabilidade):
        return vulnerabilidade_para_resposta(obter_vulnerabilidade(catalogo, id_vulnerabilidade))

    @rotas.post("/vulnerabilidades")
    def cadastrar_vulnerabilidade():
        corpo = request.get_json(silent=True)
        try:
            vulnerabilidade = registrar_vulnerabilidade_no_catalogo(
                repositorio, catalogo, corpo["nome_vulnerabilidade"], corpo["cvss"]
            )
        except (KeyError, TypeError):
            return {"erro": MENSAGEM_DE_DADOS_INVALIDOS}, 400
        return vulnerabilidade_para_resposta(vulnerabilidade), 201

    @rotas.put("/vulnerabilidades/<int:id_vulnerabilidade>")
    def editar_vulnerabilidade(id_vulnerabilidade):
        vulnerabilidade_atual = obter_vulnerabilidade(catalogo, id_vulnerabilidade)
        corpo = request.get_json(silent=True)
        if type(corpo) is not dict:
            return {"erro": MENSAGEM_DE_DADOS_INVALIDOS}, 400

        vulnerabilidade_editada = Vulnerabilidade(
            id_vulnerabilidade,
            valor_enviado_ou_atual(
                corpo, "nome_vulnerabilidade", vulnerabilidade_atual.nome_vulnerabilidade
            ),
            valor_enviado_ou_atual(corpo, "cvss", vulnerabilidade_atual.cvss),
        )
        atualizar_vulnerabilidade_no_catalogo(repositorio, catalogo, vulnerabilidade_editada)
        return vulnerabilidade_para_resposta(vulnerabilidade_editada)

    @rotas.delete("/vulnerabilidades/<int:id_vulnerabilidade>")
    def excluir_vulnerabilidade(id_vulnerabilidade):
        excluir_vulnerabilidade_do_catalogo(repositorio, catalogo, ativos, id_vulnerabilidade)
        return "", 204

    return rotas
