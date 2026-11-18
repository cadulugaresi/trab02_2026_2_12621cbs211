from flask import Flask, request
from inventario.persistencia.banco_sqlite import RepositorioSQLite
from inventario.dominio.excecoes import DadoInvalidoError, PersistenciaError
from inventario.dominio.ativo import MAPA_DE_TIPOS
from inventario.servicos.ordenacao import listar_ativos_ordenados, por_id
from inventario.servicos.riscos import AnaliseDeRisco
from inventario.servicos.ativos import encontrar_ativo_por_id, registrar_ativo_no_inventario
from inventario.servicos.vulnerabilidades import registrar_vulnerabilidade_no_catalogo

app = Flask(__name__)

try:
    repositorio = RepositorioSQLite()
    ativos = repositorio.carregar_ativos()
    catalogo = repositorio.carregar_catalogo()

except PersistenciaError as erro:
    print(erro)
    raise SystemExit(
        "Erro de Persistência: Não foi possível carregar os dados do banco de dados. O servidor não foi iniciado."
    )


@app.get("/saude")
def verificar_saude():
    return {"status": "ok"}


@app.get("/ativos")
def listar_ativos():
    ativos_em_dicionario = []
    for ativo in listar_ativos_ordenados(ativos, por_id):
        ativos_em_dicionario.append(ativo.para_dicionario())
    return ativos_em_dicionario


@app.get("/vulnerabilidades")
def listar_vulnerabilidades():
    vulnerabilidades_em_dicionario = []
    for vulnerabilidade in catalogo.values():
        vulnerabilidades_em_dicionario.append(vulnerabilidade.para_dicionario())
    return vulnerabilidades_em_dicionario


@app.post("/vulnerabilidades")
def cadastrar_vulnerabilidade():
    corpo = request.get_json()
    try:
        vulnerabilidade = registrar_vulnerabilidade_no_catalogo(
            repositorio, catalogo, corpo["nome"], corpo["cvss"]
        )
    except DadoInvalidoError as erro:
        return {"erro": str(erro)}, 400
    except (KeyError, TypeError):
        return {"erro": "Dados da vulnerabilidade incompletos ou inválidos."}, 400
    return vulnerabilidade.para_dicionario(), 201


@app.get("/riscos")
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


@app.get("/ativos/<int:id_ativo>")
def buscar_ativo(id_ativo):
    ativo = encontrar_ativo_por_id(ativos, id_ativo)
    if ativo is None:
        return {"erro": "Ativo não encontrado."}, 404
    return ativo.para_dicionario()


@app.post("/ativos")
def cadastrar_ativo():
    corpo = request.get_json()
    try:
        ativo = MAPA_DE_TIPOS[corpo["tipo"]].de_dicionario(corpo)
        registrar_ativo_no_inventario(repositorio, ativos, ativo)
    except DadoInvalidoError as erro:
        return {"erro": str(erro)}, 400
    except (KeyError, ValueError, TypeError):
        return {"erro": "Dados do ativo incompletos ou inválidos."}, 400
    return ativo.para_dicionario(), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
