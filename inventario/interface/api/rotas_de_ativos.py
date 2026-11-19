from flask import Blueprint, request

from inventario.dominio.ativo import MAPA_DE_TIPOS
from inventario.dominio.excecoes import DadoInvalidoError
from inventario.servicos.ativos import encontrar_ativo_por_id, registrar_ativo_no_inventario
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
        ativo = encontrar_ativo_por_id(ativos, id_ativo)
        if ativo is None:
            return {"erro": "Ativo não encontrado."}, 404
        return ativo.para_dicionario()

    @rotas.post("/ativos")
    def cadastrar_ativo():
        corpo = request.get_json(silent=True)
        try:
            ativo = MAPA_DE_TIPOS[corpo["tipo"]].de_dicionario(corpo)
            registrar_ativo_no_inventario(repositorio, ativos, ativo)
        except DadoInvalidoError as erro:
            return {"erro": str(erro)}, 400
        except (KeyError, ValueError, TypeError):
            return {"erro": "Dados do ativo incompletos ou inválidos."}, 400
        return ativo.para_dicionario(), 201

    return rotas
