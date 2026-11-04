import os
import unittest

from inventario.persistencia import arquivos_json


class TesteComArquivosTemporarios(unittest.TestCase):

    arquivo_dados = "teste_ativos_tmp.json"
    arquivo_catalogo = "teste_catalogo_tmp.json"

    def setUp(self):
        self.originais = (arquivos_json.ARQUIVO_DADOS, arquivos_json.ARQUIVO_CATALOGO)
        arquivos_json.ARQUIVO_DADOS = self.arquivo_dados
        arquivos_json.ARQUIVO_CATALOGO = self.arquivo_catalogo

    def tearDown(self):
        for arquivo in (self.arquivo_dados, self.arquivo_catalogo):
            if os.path.exists(arquivo):
                os.remove(arquivo)
        arquivos_json.ARQUIVO_DADOS, arquivos_json.ARQUIVO_CATALOGO = self.originais
