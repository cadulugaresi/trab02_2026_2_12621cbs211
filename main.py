from inventario.interface.menu import menu_principal
from inventario.persistencia.banco_sqlite import RepositorioSQLite
from inventario.dominio.excecoes import PersistenciaError

if __name__ == "__main__":

    try:
        repositorio = RepositorioSQLite()
        ativos = repositorio.carregar_ativos()
        catalogo = repositorio.carregar_catalogo()

    except PersistenciaError as erro:
        print(erro)
        raise SystemExit(
            "Erro de Persistência: Não foi possível carregar os dados do banco de dados. Encerrando o programa."
        )

    menu_principal(repositorio, ativos, catalogo)
