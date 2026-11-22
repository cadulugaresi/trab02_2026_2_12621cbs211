import unittest

from inventario.interface.api import criar_app
from inventario.persistencia.banco_sqlite import RepositorioSQLite
from semear_demonstracao import (
    ATIVOS,
    VULNERABILIDADES,
    DemonstracaoRecusadaError,
    carregar_demonstracao,
)


class ClienteDeTeste:

    def __init__(self, cliente_do_flask):
        self.cliente_do_flask = cliente_do_flask

    def buscar(self, caminho):
        return self.cliente_do_flask.get(caminho).get_json()

    def enviar(self, caminho, corpo):
        resposta = self.cliente_do_flask.post(caminho, json=corpo)
        if resposta.status_code >= 400:
            raise DemonstracaoRecusadaError(f"{caminho}: {resposta.get_json()['erro']}")
        return resposta.get_json()


class TesteDaDemonstracao(unittest.TestCase):

    def criar_cliente(self):
        repositorio = RepositorioSQLite(":memory:")
        self.addCleanup(repositorio.conexao.close)
        return ClienteDeTeste(criar_app(repositorio, {}, {}).test_client())

    def contar_vinculos(self, cliente):
        quantidade = 0
        for ativo in cliente.buscar("/ativos"):
            quantidade += len(ativo["vulnerabilidades"])
        return quantidade

    def test_carrega_todos_os_ativos_e_vulnerabilidades_pela_api(self):
        cliente = self.criar_cliente()

        carregar_demonstracao(cliente)

        self.assertEqual(len(cliente.buscar("/ativos")), len(ATIVOS))
        self.assertEqual(len(cliente.buscar("/vulnerabilidades")), len(VULNERABILIDADES))

    def test_o_ranking_de_risco_pode_ser_calculado_com_os_dados_da_demonstracao(self):
        cliente = self.criar_cliente()

        carregar_demonstracao(cliente)
        ranking = cliente.buscar("/riscos")

        self.assertEqual(len(ranking), len(ATIVOS))
        self.assertGreater(ranking[0]["risco_efetivo"], 0)

    def test_gera_sempre_os_mesmos_vinculos(self):
        primeiro_cliente = self.criar_cliente()
        segundo_cliente = self.criar_cliente()

        carregar_demonstracao(primeiro_cliente)
        carregar_demonstracao(segundo_cliente)

        self.assertEqual(
            self.contar_vinculos(primeiro_cliente), self.contar_vinculos(segundo_cliente)
        )

    def test_recusa_um_banco_que_ja_tem_ativos_sem_cadastrar_nada(self):
        cliente = self.criar_cliente()
        cliente.enviar(
            "/ativos",
            {
                "tipo": "Notebook",
                "id": 1,
                "nome": "Notebook do Rafael",
                "setor": 1,
                "responsavel": "Rafael Torres",
                "status": 1,
                "sistema_operacional": "Linux",
                "tela": 14,
            },
        )

        with self.assertRaises(DemonstracaoRecusadaError):
            carregar_demonstracao(cliente)

        self.assertEqual(len(cliente.buscar("/ativos")), 1)
        self.assertEqual(cliente.buscar("/vulnerabilidades"), [])


if __name__ == "__main__":
    unittest.main()
