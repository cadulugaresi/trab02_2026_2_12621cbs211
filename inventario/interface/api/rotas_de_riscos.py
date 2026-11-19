from flask import Blueprint

from inventario.dominio.excecoes import DadoInvalidoError
from inventario.servicos.riscos import AnaliseDeRisco


def criar_rotas_de_riscos(ativos, catalogo):
    rotas = Blueprint("riscos", __name__)

    @rotas.get("/riscos")
    def listar_riscos():
        if len(ativos) == 0:
            return []

        try:
            analise = AnaliseDeRisco(ativos, catalogo)
        except DadoInvalidoError as erro:
            return {"erro": str(erro)}, 409

        ranking_de_risco = []

        for posicao, id_ativo in enumerate(analise.ranking(), start=1):
            ativo = ativos[id_ativo]
            ranking_de_risco.append(
                {
                    "posicao": posicao,
                    "id": ativo.id,
                    "nome": ativo.nome,
                    "tipo": type(ativo).__name__,
                    "fator_exposicao": ativo.fator_exposicao,
                    "risco_proprio": round(analise.risco_proprio_do_ativo(id_ativo), 2),
                    "risco_herdado": round(analise.risco_herdado_do_ativo(id_ativo), 2),
                    "risco_efetivo": round(analise.risco_efetivo_do_ativo(id_ativo), 2),
                }
            )
        return ranking_de_risco

    return rotas
