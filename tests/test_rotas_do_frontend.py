import unittest

from inventario.interface.api import criar_app
from inventario.persistencia.banco_sqlite import RepositorioSQLite

MENSAGEM_DE_ROTA_NAO_ENCONTRADA = {"erro": "Rota não encontrada."}


class TesteDasRotasDoFrontend(unittest.TestCase):

    def setUp(self):
        self.repositorio = RepositorioSQLite(":memory:")
        aplicacao = criar_app(self.repositorio, {}, {})
        self.cliente = aplicacao.test_client()

    def tearDown(self):
        self.repositorio.conexao.close()

    def buscar(self, caminho):
        resposta = self.cliente.get(caminho)
        resposta.get_data()
        resposta.close()
        return resposta

    def test_raiz_entrega_a_pagina_do_frontend(self):
        resposta = self.buscar("/")

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.mimetype, "text/html")
        self.assertIn(b'<script type="module" src="/web/js/principal.js">', resposta.data)

    def test_entrega_o_javascript_como_javascript(self):
        resposta = self.buscar("/web/js/principal.js")

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.mimetype, "text/javascript")

    def test_entrega_o_tema_com_as_variaveis_de_cor(self):
        resposta = self.buscar("/web/estilos/tema-macos.css")

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.mimetype, "text/css")
        self.assertIn(b"--fundo: #FBFBFA;", resposta.data)

    def test_entrega_a_fonte_inter_de_dentro_do_projeto(self):
        resposta = self.buscar("/web/fontes/InterVariable.woff2")

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.mimetype, "font/woff2")

    def test_entrega_os_icones_de_dentro_do_projeto(self):
        resposta = self.buscar("/web/icones/server.svg")

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.mimetype, "image/svg+xml")

    def test_entrega_as_licencas_da_fonte_e_dos_icones(self):
        licenca_da_fonte = self.buscar("/web/fontes/LICENSE.txt")
        licenca_dos_icones = self.buscar("/web/icones/LICENSE.txt")

        self.assertEqual(licenca_da_fonte.status_code, 200)
        self.assertIn(b"SIL Open Font License", licenca_da_fonte.data)
        self.assertEqual(licenca_dos_icones.status_code, 200)
        self.assertIn(b"ISC License", licenca_dos_icones.data)

    def test_arquivo_inexistente_devolve_404_em_json(self):
        resposta = self.buscar("/web/js/arquivo_que_nao_existe.js")

        self.assertEqual(resposta.status_code, 404)
        self.assertEqual(resposta.get_json(), MENSAGEM_DE_ROTA_NAO_ENCONTRADA)

    def test_nao_entrega_arquivos_de_fora_da_pasta_do_frontend(self):
        resposta = self.buscar("/web/..%2f..%2fdominio%2fativo.py")

        self.assertEqual(resposta.status_code, 404)
        self.assertEqual(resposta.get_json(), MENSAGEM_DE_ROTA_NAO_ENCONTRADA)
        self.assertNotIn(b"class Ativo", resposta.data)

    def test_raiz_so_aceita_get(self):
        resposta = self.cliente.post("/")

        self.assertEqual(resposta.status_code, 405)
        self.assertEqual(resposta.get_json(), {"erro": "Método não permitido para esta rota."})

    def test_rotas_da_api_continuam_respondendo_em_json(self):
        saude = self.buscar("/saude")
        ativos = self.buscar("/ativos")

        self.assertEqual(saude.get_json(), {"status": "ok"})
        self.assertEqual(ativos.get_json(), [])


if __name__ == "__main__":
    unittest.main()
