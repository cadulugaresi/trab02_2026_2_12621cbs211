import os
import sqlite3
from inventario.persistencia.repositorio import Repositorio
from inventario.dominio.vulnerabilidade import Vulnerabilidade

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

    def carregar_catalogo(self):
        todas_as_vulnerabilidades = self.conexao.execute(
            """SELECT id_vulnerabilidade,
            nome_vulnerabilidade,
            cvss FROM vulnerabilidades"""
        ).fetchall()

        catalogo = {}

        for registro in todas_as_vulnerabilidades:
            id_vulnerabilidade, nome_vulnerabilidade, cvss = registro
            vulnerabilidade = Vulnerabilidade(id_vulnerabilidade, nome_vulnerabilidade, cvss)
            catalogo[id_vulnerabilidade] = vulnerabilidade

        return catalogo

    def adicionar_ativo(self, ativo):
        pass

    def atualizar_ativo(self, ativo):
        pass

    def remover_ativo(self, id_ativo):
        pass

    def adicionar_vulnerabilidade(self, vulnerabilidade):
        with self.conexao:
            self.conexao.execute(
                """INSERT INTO vulnerabilidades
                (id_vulnerabilidade, nome_vulnerabilidade, cvss)
                VALUES (?, ?, ?)""",
                (vulnerabilidade.id_vulnerabilidade,
                vulnerabilidade.nome_vulnerabilidade,
            vulnerabilidade.cvss,)
            ,)

    def atualizar_vulnerabilidade(self, vulnerabilidade):
        with self.conexao:
            self.conexao.execute(
                """UPDATE vulnerabilidades
                SET nome_vulnerabilidade = ?, cvss = ?
                WHERE id_vulnerabilidade = ?""",
                (vulnerabilidade.nome_vulnerabilidade,
                vulnerabilidade.cvss,
            vulnerabilidade.id_vulnerabilidade,)
        ,)

    def remover_vulnerabilidade(self, id_vulnerabilidade):
        with self.conexao:
            self.conexao.execute(
                """DELETE FROM vulnerabilidades
                WHERE id_vulnerabilidade = ?""",
                (id_vulnerabilidade,),
            )

    def vincular(self, id_ativo, id_vulnerabilidade, status):
        pass

    def atualizar_status_vinculo(self, id_ativo, id_vulnerabilidade, status):
        pass

    def desvincular(self, id_ativo, id_vulnerabilidade):
        pass
