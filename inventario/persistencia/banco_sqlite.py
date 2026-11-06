import os
import sqlite3
from inventario.persistencia.repositorio import Repositorio

ARQUIVO_BANCO_DE_DADOS = "inventario.db"
ESQUEMA_SQL = os.path.join(os.path.dirname(__file__), "esquema.sql")


class RepositorioSQLite(Repositorio):
    def __init__(self, caminho_banco_de_dados=ARQUIVO_BANCO_DE_DADOS):
        self.conexao = sqlite3.connect(caminho_banco_de_dados)
        self.conexao.execute("PRAGMA foreign_keys = ON")

        with open(ESQUEMA_SQL, encoding="utf-8") as arquivo:
            self.conexao.executescript(arquivo.read())

    def carregar_ativos(self):
        pass

    def salvar_ativos(self, ativos):
        pass

    def carregar_catalogo(self):
        pass

    def salvar_catalogo(self, catalogo):
        pass
