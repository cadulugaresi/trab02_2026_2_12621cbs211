import os
import unittest

from inventario.persistencia.banco_sqlite import RepositorioSQLite
from tests.contrato_repositorio import ContratoDoRepositorio


class TestRepositorioSQLite(ContratoDoRepositorio, unittest.TestCase):

    caminho_banco_de_dados = "teste_inventario_tmp.db"

    def setUp(self):
        self.repositorios_abertos = []
        super().setUp()

    def tearDown(self):
        for repositorio in self.repositorios_abertos:
            repositorio.conexao.close()

        if os.path.exists(self.caminho_banco_de_dados):
            os.remove(self.caminho_banco_de_dados)

    def criar_repositorio(self):
        repositorio = RepositorioSQLite(self.caminho_banco_de_dados)
        self.repositorios_abertos.append(repositorio)
        return repositorio
