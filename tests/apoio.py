import os
import unittest

import inventario.persistencia


class TesteComArquivosTemporarios(unittest.TestCase):  # base: troca os JSON reais por temporários

    arquivo_dados = "teste_ativos_tmp.json"
    arquivo_catalogo = "teste_catalogo_tmp.json"

    def setUp(self):
        self.originais = (
            inventario.persistencia.ARQUIVO_DADOS,
            inventario.persistencia.ARQUIVO_CATALOGO,
        )
        inventario.persistencia.ARQUIVO_DADOS = self.arquivo_dados  # não mexe nos arquivos reais
        inventario.persistencia.ARQUIVO_CATALOGO = self.arquivo_catalogo

    def tearDown(self):
        for arquivo in (self.arquivo_dados, self.arquivo_catalogo):
            if os.path.exists(arquivo):
                os.remove(arquivo)  # apaga o que o teste criou
        inventario.persistencia.ARQUIVO_DADOS, inventario.persistencia.ARQUIVO_CATALOGO = (
            self.originais
        )
