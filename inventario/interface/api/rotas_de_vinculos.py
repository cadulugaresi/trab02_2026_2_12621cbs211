from flask import Blueprint, request

from inventario.dominio.enums import StatusDaVuln
from inventario.dominio.validacoes import validar_inteiro_positivo
from inventario.interface.api.respostas import vulnerabilidade_para_resposta
from inventario.servicos.ativos import obter_ativo
from inventario.servicos.vulnerabilidades import (
    atualizar_status_vulnerabilidade,
    desvincular_vulnerabilidade,
    vincular_vulnerabilidade,
)

MENSAGEM_DE_DADOS_INVALIDOS = "Dados incompletos ou inválidos."


def criar_rotas_de_vinculos(repositorio, ativos, catalogo):
    rotas = Blueprint("vinculos", __name__)

    @rotas.get("/ativos/<int:id_ativo>/vulnerabilidades")
    def listar_vulnerabilidades_do_ativo(id_ativo):
        ativo = obter_ativo(ativos, id_ativo)
        vulnerabilidades_do_ativo = []
        for id_vulnerabilidade, status_tratamento in ativo.vulnerabilidades.items():
            vulnerabilidade = vulnerabilidade_para_resposta(catalogo[id_vulnerabilidade])
            vulnerabilidade["status_tratamento"] = status_tratamento.value
            vulnerabilidades_do_ativo.append(vulnerabilidade)
        return vulnerabilidades_do_ativo

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
        except (KeyError, ValueError, TypeError):
            return {"erro": MENSAGEM_DE_DADOS_INVALIDOS}, 400
        return ativos[id_ativo].para_dicionario(), 201

    @rotas.put("/ativos/<int:id_ativo>/vulnerabilidades/<int:id_vulnerabilidade>")
    def atualizar_status_do_vinculo(id_ativo, id_vulnerabilidade):
        corpo = request.get_json(silent=True)
        try:
            novo_status = StatusDaVuln(validar_inteiro_positivo(corpo["status_tratamento"]))
            atualizar_status_vulnerabilidade(
                repositorio, ativos, id_ativo, id_vulnerabilidade, novo_status
            )
        except (KeyError, ValueError, TypeError):
            return {"erro": MENSAGEM_DE_DADOS_INVALIDOS}, 400
        return ativos[id_ativo].para_dicionario()

    @rotas.delete("/ativos/<int:id_ativo>/vulnerabilidades/<int:id_vulnerabilidade>")
    def desvincular_vulnerabilidade_do_ativo(id_ativo, id_vulnerabilidade):
        desvincular_vulnerabilidade(repositorio, ativos, id_ativo, id_vulnerabilidade)
        return "", 204

    return rotas
