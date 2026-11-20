from werkzeug.serving import WSGIRequestHandler

from inventario.persistencia.banco_sqlite import RepositorioSQLite
from inventario.dominio.excecoes import PersistenciaError
from inventario.interface.api import criar_app

SEGUNDOS_DE_ESPERA_POR_CONEXAO_PARADA = 1


class AtendenteDeRequisicoesComTempoLimite(WSGIRequestHandler):
    timeout = SEGUNDOS_DE_ESPERA_POR_CONEXAO_PARADA


if __name__ == "__main__":

    try:
        repositorio = RepositorioSQLite()
        ativos = repositorio.carregar_ativos()
        catalogo = repositorio.carregar_catalogo()

    except PersistenciaError as erro:
        print(erro)
        raise SystemExit(
            "Erro de Persistência: Não foi possível carregar os dados do banco de dados. "
            "O servidor não foi iniciado."
        )

    app = criar_app(repositorio, ativos, catalogo)
    app.run(
        host="0.0.0.0",
        port=5000,
        threaded=False,
        request_handler=AtendenteDeRequisicoesComTempoLimite,
    )
