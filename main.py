from inventario.interface.menu import menu_principal
from inventario.persistencia.arquivos_json import carregar_catalogo, carregar_dados
from inventario.dominio.excecoes import PersistenciaError

if __name__ == "__main__":

    try:
        ativos = carregar_dados()
        catalogo = carregar_catalogo()

    except PersistenciaError as erro:
        print(erro)
        raise SystemExit(
            "Erro de Persistência: Não foi possível carregar os dados do arquivo. Encerrando o programa."
        )

    menu_principal(ativos, catalogo)
