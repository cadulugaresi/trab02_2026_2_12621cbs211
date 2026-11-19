from flask import Blueprint, request

from inventario.interface.api.requisicoes import valor_enviado_ou_atual
from inventario.servicos.ativos import obter_ativo
from inventario.servicos.dependencias import (
    atualizar_dependencia,
    cadastrar_dependencia,
    garantir_que_dependencia_existe,
    remover_dependencia,
)

MENSAGEM_DE_DADOS_INVALIDOS = "Dados da dependência incompletos ou inválidos."


def criar_rotas_de_dependencias(repositorio, ativos):
    rotas = Blueprint("dependencias", __name__)

    @rotas.get("/ativos/<int:id_ativo>/dependencias")
    def listar_dependencias_do_ativo(id_ativo):
        ativo = obter_ativo(ativos, id_ativo)
        dependencias_do_ativo = []
        for id_ativo_do_qual_depende, fracao in ativo.dependencias.items():
            dependencias_do_ativo.append(
                {
                    "id_ativo_do_qual_depende": id_ativo_do_qual_depende,
                    "nome_do_ativo_do_qual_depende": ativos[id_ativo_do_qual_depende].nome,
                    "fracao": fracao,
                }
            )
        return dependencias_do_ativo

    @rotas.post("/ativos/<int:id_ativo>/dependencias")
    def cadastrar_dependencia_do_ativo(id_ativo):
        corpo = request.get_json(silent=True)
        try:
            cadastrar_dependencia(
                repositorio, ativos, id_ativo, corpo["id_ativo_do_qual_depende"], corpo["fracao"]
            )
        except (KeyError, TypeError):
            return {"erro": MENSAGEM_DE_DADOS_INVALIDOS}, 400
        return ativos[id_ativo].para_dicionario(), 201

    @rotas.put("/ativos/<int:id_ativo>/dependencias/<int:id_ativo_do_qual_depende>")
    def atualizar_dependencia_do_ativo(id_ativo, id_ativo_do_qual_depende):
        ativo = obter_ativo(ativos, id_ativo)
        garantir_que_dependencia_existe(ativo, id_ativo_do_qual_depende)
        corpo = request.get_json(silent=True)
        if type(corpo) is not dict:
            return {"erro": MENSAGEM_DE_DADOS_INVALIDOS}, 400

        atualizar_dependencia(
            repositorio,
            ativos,
            id_ativo,
            id_ativo_do_qual_depende,
            valor_enviado_ou_atual(corpo, "id_ativo_do_qual_depende", id_ativo_do_qual_depende),
            valor_enviado_ou_atual(corpo, "fracao", ativo.dependencias[id_ativo_do_qual_depende]),
        )
        return ativo.para_dicionario()

    @rotas.delete("/ativos/<int:id_ativo>/dependencias/<int:id_ativo_do_qual_depende>")
    def remover_dependencia_do_ativo(id_ativo, id_ativo_do_qual_depende):
        remover_dependencia(repositorio, ativos, id_ativo, id_ativo_do_qual_depende)
        return "", 204

    return rotas
