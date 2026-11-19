from flask import Blueprint, request

from inventario.dominio.ativo import MAPA_DE_TIPOS
from inventario.dominio.enums import StatusDoAtivo
from inventario.servicos.ativos import (
    atualizar_ativo_no_inventario,
    encontrar_ativos_por_nome,
    encontrar_ativos_por_status,
    encontrar_ativos_por_tipo,
    obter_ativo,
    registrar_ativo_no_inventario,
    remover_ativo_do_inventario,
)
from inventario.servicos.ordenacao import CRITERIOS_DE_ORDENACAO, listar_ativos_ordenados


def indexar_por_id(lista_de_ativos):
    ativos_por_id = {}
    for ativo in lista_de_ativos:
        ativos_por_id[ativo.id] = ativo
    return ativos_por_id


def filtrar_ativos(ativos, filtros):
    ativos_filtrados = ativos
    if "tipo" in filtros:
        classe = MAPA_DE_TIPOS[filtros["tipo"]]
        ativos_filtrados = indexar_por_id(encontrar_ativos_por_tipo(ativos_filtrados, classe))
    if "status" in filtros:
        status = StatusDoAtivo(int(filtros["status"]))
        ativos_filtrados = indexar_por_id(encontrar_ativos_por_status(ativos_filtrados, status))
    if "nome" in filtros:
        ativos_filtrados = indexar_por_id(
            encontrar_ativos_por_nome(ativos_filtrados, filtros["nome"])
        )
    return ativos_filtrados


def criar_rotas_de_ativos(repositorio, ativos):
    rotas = Blueprint("ativos", __name__)

    @rotas.get("/ativos")
    def listar_ativos():
        try:
            ativos_filtrados = filtrar_ativos(ativos, request.args)
            criterio = CRITERIOS_DE_ORDENACAO[request.args.get("ordenar", "id")]
        except (KeyError, ValueError):
            return {"erro": "Filtro inválido."}, 400

        ativos_em_dicionario = []
        for ativo in listar_ativos_ordenados(ativos_filtrados, criterio):
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
