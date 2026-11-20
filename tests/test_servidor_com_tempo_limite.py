import socket
import threading
import time
import unittest
import urllib.error
import urllib.request

from werkzeug.serving import WSGIRequestHandler, make_server

from iniciar_api import AtendenteDeRequisicoesComTempoLimite
from inventario.interface.api import criar_app
from inventario.persistencia.banco_sqlite import RepositorioSQLite

SEGUNDOS_PARA_DESISTIR_DA_REQUISICAO = 5
SEGUNDOS_PARA_PROVAR_O_TRAVAMENTO = 2


class TesteDoServidorComConexaoParada(unittest.TestCase):

    def iniciar_servidor(self, atendente):
        repositorio = RepositorioSQLite(":memory:")
        aplicacao = criar_app(repositorio, {}, {})
        servidor = make_server("127.0.0.1", 0, aplicacao, request_handler=atendente)
        threading.Thread(target=servidor.serve_forever, daemon=True).start()
        self.addCleanup(repositorio.conexao.close)
        self.addCleanup(servidor.server_close)
        self.addCleanup(servidor.shutdown)
        return servidor.server_port

    def abrir_conexao_parada(self, porta):
        conexao_parada = socket.create_connection(("127.0.0.1", porta))
        self.addCleanup(conexao_parada.close)
        time.sleep(0.2)

    def buscar_saude(self, porta, segundos_de_espera):
        endereco = f"http://127.0.0.1:{porta}/saude"
        with urllib.request.urlopen(endereco, timeout=segundos_de_espera) as resposta:
            return resposta.status, resposta.read()

    def test_responde_mesmo_com_uma_conexao_parada_aberta(self):
        porta = self.iniciar_servidor(AtendenteDeRequisicoesComTempoLimite)
        self.abrir_conexao_parada(porta)

        inicio = time.monotonic()
        status, corpo = self.buscar_saude(porta, SEGUNDOS_PARA_DESISTIR_DA_REQUISICAO)
        duracao = time.monotonic() - inicio

        self.assertEqual(status, 200)
        self.assertIn(b'"status":"ok"', corpo.replace(b" ", b""))
        self.assertLess(duracao, 3)

    def test_sem_tempo_limite_a_conexao_parada_trava_o_servidor(self):
        porta = self.iniciar_servidor(WSGIRequestHandler)
        self.abrir_conexao_parada(porta)

        with self.assertRaises((TimeoutError, urllib.error.URLError)):
            self.buscar_saude(porta, SEGUNDOS_PARA_PROVAR_O_TRAVAMENTO)


if __name__ == "__main__":
    unittest.main()
