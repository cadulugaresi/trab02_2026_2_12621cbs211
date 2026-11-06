from inventario.interface.menu import menu_principal
from inventario.persistencia.arquivos_json import RepositorioJSON
from inventario.dominio.excecoes import PersistenciaError

if __name__ == "__main__":

    repositorio = RepositorioJSON()

    try:
        ativos = repositorio.carregar_ativos()
        catalogo = repositorio.carregar_catalogo()

    except PersistenciaError as erro:
        print(erro)
        raise SystemExit(
            "Erro de Persistência: Não foi possível carregar os dados do arquivo. Encerrando o programa."
        )

    menu_principal(repositorio, ativos, catalogo)
