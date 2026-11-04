from inventario.interface.menu import menu_principal
from inventario.persistencia.arquivos_json import carregar_catalogo, carregar_dados

if __name__ == "__main__":

    ativos = carregar_dados()
    catalogo = carregar_catalogo()

    menu_principal(ativos, catalogo)
