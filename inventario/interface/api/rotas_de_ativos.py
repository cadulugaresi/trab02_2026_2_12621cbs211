from flask import Blueprint, request

from inventario.dominio.ativo import MAPA_DE_TIPOS
from inventario.servicos.ativos import (
    atualizar_ativo_no_inventario,
    obter_ativo,
    registrar_ativo_no_inventario,
    remover_ativo_do_inventario,
)
from inventario.servicos.ordenacao import listar_ativos_ordenados, por_id


def criar_rotas_de_ativos(repositorio, ativos):
    rotas = Blueprint("ativos", __name__)

    @rotas.get("/ativos")
    def listar_ativos():
        ativos_em_dicionario = []
        for ativo in listar_ativos_ordenados(ativos, por_id):
            ativos_em_dicionario.append(ativo.para_dicionario())
        return ativos_em_dicionario

    @rotas.get("/ativos/<int:id_ativo>")
    def buscar_ativo(id_ativo):
        return obter_ativo(ativos, id_ativo).para_dicionario()

    @rotas.post("/ativos")
    def cadastrar_ativo():
        corpo = request.get_json(silent=True)
        try:
            ativo = MAPA_DE_TIPOS[corpo["tipo"]].de_dicionario(corpo)
            registrar_ativo_no_inventario(repositorio, ativos, ativo)
        except (KeyError, ValueError, TypeError):
            return {"erro": "Dados do ativo incompletos ou inválidos."}, 400
        return ativo.para_dicionario(), 201

    @rotas.put("/ativos/<int:id_ativo>")
    def editar_ativo(id_ativo):
        ativo_atual = obter_ativo(ativos, id_ativo)
        corpo = request.get_json(silent=True)
        try:
            corpo["id"] = id_ativo
            tipo_continua_o_mesmo = corpo["tipo"] == type(ativo_atual).__name__
            if tipo_continua_o_mesmo and corpo.get("fator_exposicao") is None:
                corpo["fator_exposicao"] = ativo_atual.fator_exposicao
            ativo_editado = MAPA_DE_TIPOS[corpo["tipo"]].de_dicionario(corpo)
            atualizar_ativo_no_inventario(repositorio, ativos, ativo_editado)
        except (KeyError, ValueError, TypeError):
            return {"erro": "Dados do ativo incompletos ou inválidos."}, 400
        return ativo_editado.para_dicionario()

    @rotas.delete("/ativos/<int:id_ativo>")
    def excluir_ativo(id_ativo):
        remover_ativo_do_inventario(repositorio, ativos, id_ativo)
        return "", 204

    return rotas
