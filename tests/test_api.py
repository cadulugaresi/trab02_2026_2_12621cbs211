import unittest

from inventario.interface.api import criar_app
from inventario.persistencia.banco_sqlite import RepositorioSQLite


def criar_corpo_de_notebook(id_ativo=2):
    return {
        "tipo": "Notebook",
        "id": id_ativo,
        "nome": "Notebook do Rafael",
        "setor": 1,
        "responsavel": "Rafael Torres",
        "status": 1,
        "sistema_operacional": "Linux",
        "tela": 14.0,
    }


class TesteDaApi(unittest.TestCase):

    def setUp(self):
        self.repositorio = RepositorioSQLite(":memory:")
        self.ativos = {}
        self.catalogo = {}
        aplicacao = criar_app(self.repositorio, self.ativos, self.catalogo)
        self.cliente = aplicacao.test_client()

    def tearDown(self):
        self.repositorio.conexao.close()

    def cadastrar_notebook(self, id_ativo=2):
        return self.cliente.post("/ativos", json=criar_corpo_de_notebook(id_ativo))

    def cadastrar_vulnerabilidade(self, nome="Log4Shell", cvss=10):
        corpo = {"nome_vulnerabilidade": nome, "cvss": cvss}
        return self.cliente.post("/vulnerabilidades", json=corpo)

    def vincular(self, id_ativo, id_vulnerabilidade, status_tratamento=1):
        corpo = {"id_vulnerabilidade": id_vulnerabilidade, "status_tratamento": status_tratamento}
        return self.cliente.post(f"/ativos/{id_ativo}/vulnerabilidades", json=corpo)


class TesteDaSaude(TesteDaApi):

    def test_saude_responde_ok(self):
        resposta = self.cliente.get("/saude")

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.get_json(), {"status": "ok"})


class TesteDeAtivos(TesteDaApi):

    def test_listar_sem_ativos_devolve_lista_vazia(self):
        resposta = self.cliente.get("/ativos")

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.get_json(), [])

    def test_listar_devolve_ativos_ordenados_por_id(self):
        self.cadastrar_notebook(3)
        self.cadastrar_notebook(1)

        resposta = self.cliente.get("/ativos")

        ids_na_resposta = []
        for ativo in resposta.get_json():
            ids_na_resposta.append(ativo["id"])
        self.assertEqual(ids_na_resposta, [1, 3])

    def test_cadastrar_ativo_devolve_201_com_fator_padrao_do_tipo(self):
        resposta = self.cadastrar_notebook()

        self.assertEqual(resposta.status_code, 201)
        self.assertEqual(resposta.get_json()["responsavel"], "Rafael Torres")
        self.assertEqual(resposta.get_json()["fator_exposicao"], 1.2)

    def test_cadastrar_ativo_grava_no_banco(self):
        self.cadastrar_notebook()

        ativos_no_banco = self.repositorio.carregar_ativos()

        self.assertIn(2, ativos_no_banco)

    def test_cadastrar_ativo_com_id_repetido_devolve_400(self):
        self.cadastrar_notebook()

        resposta = self.cadastrar_notebook()

        self.assertEqual(resposta.status_code, 400)
        self.assertEqual(resposta.get_json()["erro"], "Já existe um ativo cadastrado com este ID.")

    def test_cadastrar_ativo_com_tipo_inexistente_devolve_400(self):
        corpo = criar_corpo_de_notebook()
        corpo["tipo"] = "Tablet"

        resposta = self.cliente.post("/ativos", json=corpo)

        self.assertEqual(resposta.status_code, 400)

    def test_cadastrar_ativo_sem_campo_obrigatorio_devolve_400(self):
        corpo = criar_corpo_de_notebook()
        del corpo["tela"]

        resposta = self.cliente.post("/ativos", json=corpo)

        self.assertEqual(resposta.status_code, 400)

    def test_cadastrar_ativo_com_setor_inexistente_devolve_400(self):
        corpo = criar_corpo_de_notebook()
        corpo["setor"] = 99

        resposta = self.cliente.post("/ativos", json=corpo)

        self.assertEqual(resposta.status_code, 400)

    def test_cadastrar_ativo_com_fator_fora_do_limite_devolve_400(self):
        corpo = criar_corpo_de_notebook()
        corpo["fator_exposicao"] = 7

        resposta = self.cliente.post("/ativos", json=corpo)

        self.assertEqual(resposta.status_code, 400)
        self.assertEqual(
            resposta.get_json()["erro"],
            "O fator de exposição deve ser maior que 0 e no máximo 2.",
        )

    def test_cadastrar_ativo_com_responsavel_vazio_devolve_400(self):
        corpo = criar_corpo_de_notebook()
        corpo["responsavel"] = ""

        resposta = self.cliente.post("/ativos", json=corpo)

        self.assertEqual(resposta.status_code, 400)
        self.assertNotIn(2, self.ativos)

    def test_buscar_ativo_existente_devolve_200(self):
        self.cadastrar_notebook()

        resposta = self.cliente.get("/ativos/2")

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.get_json()["nome"], "Notebook do Rafael")

    def test_buscar_ativo_inexistente_devolve_404(self):
        resposta = self.cliente.get("/ativos/99")

        self.assertEqual(resposta.status_code, 404)
        self.assertEqual(resposta.get_json(), {"erro": "Ativo não encontrado."})


class TesteDeVulnerabilidades(TesteDaApi):

    def test_cadastrar_vulnerabilidade_devolve_201_com_id_gerado(self):
        resposta = self.cadastrar_vulnerabilidade()

        self.assertEqual(resposta.status_code, 201)
        self.assertEqual(
            resposta.get_json(),
            {"id_vulnerabilidade": 1, "nome_vulnerabilidade": "Log4Shell", "cvss": 10},
        )

    def test_cadastrar_vulnerabilidade_grava_no_banco(self):
        self.cadastrar_vulnerabilidade()

        catalogo_no_banco = self.repositorio.carregar_catalogo()

        self.assertIn(1, catalogo_no_banco)

    def test_listar_vulnerabilidades_mostra_a_cadastrada(self):
        self.cadastrar_vulnerabilidade()

        resposta = self.cliente.get("/vulnerabilidades")

        self.assertEqual(len(resposta.get_json()), 1)
        self.assertEqual(resposta.get_json()[0]["nome_vulnerabilidade"], "Log4Shell")

    def test_cadastrar_vulnerabilidade_com_cvss_fora_do_limite_devolve_400(self):
        resposta = self.cadastrar_vulnerabilidade(cvss=15)

        self.assertEqual(resposta.status_code, 400)
        self.assertEqual(resposta.get_json()["erro"], "O CVSS deve estar entre 0.1 e 10.")

    def test_cadastrar_vulnerabilidade_com_cvss_em_texto_devolve_400(self):
        resposta = self.cadastrar_vulnerabilidade(cvss="abc")

        self.assertEqual(resposta.status_code, 400)

    def test_cadastrar_vulnerabilidade_com_nome_vazio_devolve_400(self):
        resposta = self.cadastrar_vulnerabilidade(nome="")

        self.assertEqual(resposta.status_code, 400)
        self.assertEqual(self.catalogo, {})

    def test_cadastrar_vulnerabilidade_sem_cvss_devolve_400(self):
        resposta = self.cliente.post("/vulnerabilidades", json={"nome_vulnerabilidade": "X"})

        self.assertEqual(resposta.status_code, 400)


class TesteDeVinculos(TesteDaApi):

    def setUp(self):
        super().setUp()
        self.cadastrar_notebook()
        self.cadastrar_vulnerabilidade()

    def test_vincular_devolve_201_com_o_vinculo_no_ativo(self):
        resposta = self.vincular(2, 1)

        self.assertEqual(resposta.status_code, 201)
        self.assertEqual(
            resposta.get_json()["vulnerabilidades"],
            [{"id_vulnerabilidade": 1, "status_tratamento": 1}],
        )

    def test_vincular_duas_vezes_devolve_400(self):
        self.vincular(2, 1)

        resposta = self.vincular(2, 1)

        self.assertEqual(resposta.status_code, 400)
        self.assertEqual(
            resposta.get_json()["erro"], "Esta vulnerabilidade já está vinculada a este ativo."
        )

    def test_vincular_a_ativo_inexistente_devolve_400(self):
        resposta = self.vincular(99, 1)

        self.assertEqual(resposta.status_code, 400)
        self.assertEqual(resposta.get_json()["erro"], "Ativo não encontrado.")

    def test_vincular_vulnerabilidade_inexistente_devolve_400(self):
        resposta = self.vincular(2, 99)

        self.assertEqual(resposta.status_code, 400)
        self.assertEqual(resposta.get_json()["erro"], "Vulnerabilidade não encontrada no catálogo.")

    def test_vincular_com_status_inexistente_devolve_400(self):
        resposta = self.vincular(2, 1, status_tratamento=9)

        self.assertEqual(resposta.status_code, 400)


class TesteDeRiscos(TesteDaApi):

    def test_riscos_sem_ativos_devolve_lista_vazia(self):
        resposta = self.cliente.get("/riscos")

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.get_json(), [])

    def test_riscos_coloca_o_ativo_vulneravel_em_primeiro(self):
        self.cadastrar_notebook(1)
        self.cadastrar_notebook(2)
        self.cadastrar_vulnerabilidade()
        self.vincular(2, 1)

        resposta = self.cliente.get("/riscos")

        primeiro_do_ranking = resposta.get_json()[0]
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(primeiro_do_ranking["posicao"], 1)
        self.assertEqual(primeiro_do_ranking["id"], 2)
        self.assertEqual(primeiro_do_ranking["tipo"], "Notebook")


if __name__ == "__main__":
    unittest.main()
