import os
import unittest

from inventario.persistencia.banco_sqlite import RepositorioSQLite
from tests.contrato_repositorio import ContratoDoRepositorio
from inventario.dominio.excecoes import PersistenciaError


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

    def test_banco_corrompido_lanca_persistencia_error(self):
        with open(self.caminho_banco_de_dados, "w", encoding="utf-8") as arquivo:
            arquivo.write("isto não é um banco de dados, é só um texto qualquer")

        with self.assertRaises(PersistenciaError):
            RepositorioSQLite(self.caminho_banco_de_dados)
