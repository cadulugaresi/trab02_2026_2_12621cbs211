import json
import unittest
from unittest.mock import patch

from inventario.dominio.excecoes import PersistenciaError
from inventario.interface.api import criar_app
from inventario.persistencia.banco_sqlite import RepositorioSQLite
from inventario.servicos.dependencias import cadastrar_dependencia
from tests.apoio import estado_em_dicionarios

MENSAGEM_DE_DADOS_DO_ATIVO_INVALIDOS = "Dados do ativo incompletos ou inválidos."
MENSAGEM_DE_DADOS_DA_VULNERABILIDADE_INVALIDOS = (
    "Dados da vulnerabilidade incompletos ou inválidos."
)
MENSAGEM_DE_DADOS_DO_VINCULO_INVALIDOS = "Dados incompletos ou inválidos."


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


def criar_notebook_esperado(id_ativo=2, vulnerabilidades=None):
    if vulnerabilidades is None:
        vulnerabilidades = []

    return {
        "id": id_ativo,
        "nome": "Notebook do Rafael",
        "tipo": "Notebook",
        "setor": 1,
        "responsavel": "Rafael Torres",
        "status": 1,
        "vulnerabilidades": vulnerabilidades,
        "dependencias": [],
        "fator_exposicao": 1.2,
        "sistema_operacional": "Linux",
        "tela": 14.0,
    }


def criar_corpo_de_impressora():
    return {
        "tipo": "Impressora",
        "id": 2,
        "nome": "Impressora do Rafael",
        "setor": 1,
        "responsavel": "Rafael Torres",
        "status": 1,
        "cor": 1,
        "tecnologia": 2,
    }


def criar_log4shell_gravada():
    return {"id_vulnerabilidade": 1, "nome_vulnerabilidade": "Log4Shell", "cvss": 10}


def criar_log4shell_na_resposta():
    log4shell = criar_log4shell_gravada()
    log4shell["nivel"] = "CRITICO"
    return log4shell


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

    def cadastrar_notebook_com_campo_alterado(self, campo, valor):
        corpo = criar_corpo_de_notebook()
        corpo[campo] = valor
        return self.cliente.post("/ativos", json=corpo)

    def cadastrar_vulnerabilidade(self, nome="Log4Shell", cvss=10):
        corpo = {"nome_vulnerabilidade": nome, "cvss": cvss}
        return self.cliente.post("/vulnerabilidades", json=corpo)

    def vincular(self, id_ativo, id_vulnerabilidade, status_tratamento=1):
        corpo = {"id_vulnerabilidade": id_vulnerabilidade, "status_tratamento": status_tratamento}
        return self.cliente.post(f"/ativos/{id_ativo}/vulnerabilidades", json=corpo)

    def estado_da_memoria(self):
        return estado_em_dicionarios(self.ativos, self.catalogo)

    def estado_do_banco(self):
        return estado_em_dicionarios(
            self.repositorio.carregar_ativos(), self.repositorio.carregar_catalogo()
        )

    def conferir_memoria_e_banco(self, estado_esperado):
        self.assertEqual(self.estado_da_memoria(), estado_esperado)
        self.assertEqual(self.estado_do_banco(), estado_esperado)

    def conferir_erro_sem_alteracao(self, resposta, status_esperado, mensagem, estado_antes):
        self.assertEqual(resposta.status_code, status_esperado)
        self.assertEqual(resposta.get_json(), {"erro": mensagem})
        self.conferir_memoria_e_banco(estado_antes)


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

    def test_listar_devolve_os_ativos_completos_ordenados_por_id(self):
        self.cadastrar_notebook(3)
        self.cadastrar_notebook(1)

        resposta = self.cliente.get("/ativos")

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(
            resposta.get_json(), [criar_notebook_esperado(1), criar_notebook_esperado(3)]
        )

    def test_cadastrar_ativo_devolve_201_com_o_ativo_completo(self):
        resposta = self.cadastrar_notebook()

        self.assertEqual(resposta.status_code, 201)
        self.assertEqual(resposta.get_json(), criar_notebook_esperado())

    def test_cadastrar_ativo_grava_na_memoria_e_no_banco(self):
        self.cadastrar_notebook()

        self.conferir_memoria_e_banco({"ativos": {2: criar_notebook_esperado()}, "catalogo": {}})

    def test_cadastrar_ativo_com_id_repetido_devolve_400_sem_alterar_nada(self):
        self.cadastrar_notebook()
        estado_antes = self.estado_da_memoria()

        resposta = self.cadastrar_notebook()

        self.conferir_erro_sem_alteracao(
            resposta, 400, "Já existe um ativo cadastrado com este ID.", estado_antes
        )

    def test_cadastrar_ativo_com_tipo_inexistente_devolve_400_sem_alterar_nada(self):
        estado_antes = self.estado_da_memoria()

        resposta = self.cadastrar_notebook_com_campo_alterado("tipo", "Tablet")

        self.conferir_erro_sem_alteracao(
            resposta, 400, MENSAGEM_DE_DADOS_DO_ATIVO_INVALIDOS, estado_antes
        )

    def test_cadastrar_ativo_sem_campo_obrigatorio_devolve_400_sem_alterar_nada(self):
        estado_antes = self.estado_da_memoria()
        corpo = criar_corpo_de_notebook()
        del corpo["tela"]

        resposta = self.cliente.post("/ativos", json=corpo)

        self.conferir_erro_sem_alteracao(
            resposta, 400, MENSAGEM_DE_DADOS_DO_ATIVO_INVALIDOS, estado_antes
        )

    def test_cadastrar_ativo_com_setor_inexistente_devolve_400_sem_alterar_nada(self):
        estado_antes = self.estado_da_memoria()

        resposta = self.cadastrar_notebook_com_campo_alterado("setor", 99)

        self.conferir_erro_sem_alteracao(
            resposta, 400, MENSAGEM_DE_DADOS_DO_ATIVO_INVALIDOS, estado_antes
        )

    def test_cadastrar_ativo_com_fator_fora_do_limite_devolve_400_sem_alterar_nada(self):
        estado_antes = self.estado_da_memoria()

        resposta = self.cadastrar_notebook_com_campo_alterado("fator_exposicao", 7)

        self.conferir_erro_sem_alteracao(
            resposta,
            400,
            "O fator de exposição deve ser maior que 0 e no máximo 2.",
            estado_antes,
        )

    def test_cadastrar_ativo_com_fator_booleano_devolve_400_sem_alterar_nada(self):
        estado_antes = self.estado_da_memoria()

        resposta = self.cadastrar_notebook_com_campo_alterado("fator_exposicao", True)

        self.conferir_erro_sem_alteracao(
            resposta, 400, "Este campo precisa ser um número.", estado_antes
        )

    def test_cadastrar_ativo_com_responsavel_vazio_devolve_400_sem_alterar_nada(self):
        estado_antes = self.estado_da_memoria()

        resposta = self.cadastrar_notebook_com_campo_alterado("responsavel", "")

        self.conferir_erro_sem_alteracao(
            resposta, 400, "Este campo não pode ser vazio.", estado_antes
        )

    def test_cadastrar_ativo_com_id_em_texto_devolve_400_sem_alterar_nada(self):
        estado_antes = self.estado_da_memoria()

        resposta = self.cadastrar_notebook_com_campo_alterado("id", "abc")

        self.conferir_erro_sem_alteracao(
            resposta, 400, "Este campo precisa ser um número inteiro.", estado_antes
        )

    def test_cadastrar_ativo_com_id_negativo_devolve_400_sem_alterar_nada(self):
        estado_antes = self.estado_da_memoria()

        resposta = self.cadastrar_notebook_com_campo_alterado("id", -5)

        self.conferir_erro_sem_alteracao(
            resposta, 400, "Este campo não pode ser nulo ou negativo.", estado_antes
        )

    def test_cadastrar_ativo_com_nome_numerico_devolve_400_sem_alterar_nada(self):
        estado_antes = self.estado_da_memoria()

        resposta = self.cadastrar_notebook_com_campo_alterado("nome", 123)

        self.conferir_erro_sem_alteracao(
            resposta, 400, "Este campo precisa ser um texto.", estado_antes
        )

    def test_cadastrar_ativo_com_nome_so_com_espacos_devolve_400_sem_alterar_nada(self):
        estado_antes = self.estado_da_memoria()

        resposta = self.cadastrar_notebook_com_campo_alterado("nome", "   ")

        self.conferir_erro_sem_alteracao(
            resposta, 400, "Este campo não pode ser vazio.", estado_antes
        )

    def test_cadastrar_ativo_com_campo_do_tipo_em_texto_devolve_400_sem_alterar_nada(self):
        estado_antes = self.estado_da_memoria()

        resposta = self.cadastrar_notebook_com_campo_alterado("tela", "grande")

        self.conferir_erro_sem_alteracao(
            resposta, 400, "Este campo precisa ser um número.", estado_antes
        )

    def test_cadastrar_roteador_com_portas_fracionarias_devolve_400_sem_alterar_nada(self):
        estado_antes = self.estado_da_memoria()
        corpo = {
            "tipo": "Roteador",
            "id": 2,
            "nome": "Roteador do Rafael",
            "setor": 1,
            "responsavel": "Rafael Torres",
            "status": 1,
            "portas": 8.5,
            "velocidade": 1000,
        }

        resposta = self.cliente.post("/ativos", json=corpo)

        self.conferir_erro_sem_alteracao(
            resposta, 400, "Este campo precisa ser um número inteiro.", estado_antes
        )

    def test_cadastrar_impressora_devolve_201_com_cor_e_tecnologia(self):
        resposta = self.cliente.post("/ativos", json=criar_corpo_de_impressora())

        self.assertEqual(resposta.status_code, 201)
        self.assertEqual(
            resposta.get_json(),
            {
                "id": 2,
                "nome": "Impressora do Rafael",
                "tipo": "Impressora",
                "setor": 1,
                "responsavel": "Rafael Torres",
                "status": 1,
                "vulnerabilidades": [],
                "dependencias": [],
                "fator_exposicao": 0.9,
                "cor": 1,
                "tecnologia": 2,
            },
        )

    def conferir_campos_que_aceitam_so_inteiro(self, corpo_valido, campos):
        valores_que_nao_sao_inteiros = [True, 1.0]

        for campo in campos:
            for valor in valores_que_nao_sao_inteiros:
                with self.subTest(campo=campo, valor=valor):
                    estado_antes = self.estado_da_memoria()
                    corpo = dict(corpo_valido)
                    corpo[campo] = valor

                    resposta = self.cliente.post("/ativos", json=corpo)

                    self.conferir_erro_sem_alteracao(
                        resposta, 400, "Este campo precisa ser um número inteiro.", estado_antes
                    )

    def test_setor_e_status_aceitam_so_inteiro(self):
        self.conferir_campos_que_aceitam_so_inteiro(criar_corpo_de_notebook(), ["setor", "status"])

    def test_cor_e_tecnologia_da_impressora_aceitam_so_inteiro(self):
        self.conferir_campos_que_aceitam_so_inteiro(
            criar_corpo_de_impressora(), ["cor", "tecnologia"]
        )

    def test_buscar_ativo_existente_devolve_200_com_o_ativo_completo(self):
        self.cadastrar_notebook()

        resposta = self.cliente.get("/ativos/2")

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.get_json(), criar_notebook_esperado())

    def test_buscar_ativo_inexistente_devolve_404(self):
        resposta = self.cliente.get("/ativos/99")

        self.assertEqual(resposta.status_code, 404)
        self.assertEqual(resposta.get_json(), {"erro": "Ativo não encontrado."})


class TesteDeEdicaoDeAtivo(TesteDaApi):

    def setUp(self):
        super().setUp()
        corpo_do_notebook = criar_corpo_de_notebook(2)
        corpo_do_notebook["fator_exposicao"] = 1.7
        self.cliente.post("/ativos", json=corpo_do_notebook)
        self.cadastrar_notebook(3)
        self.cadastrar_vulnerabilidade()
        self.vincular(2, 1)
        cadastrar_dependencia(self.repositorio, self.ativos, 2, 3, 0.4)

    def editar(self, id_ativo, corpo):
        return self.cliente.put(f"/ativos/{id_ativo}", json=corpo)

    def criar_ativo_2_esperado(self, **campos_alterados):
        ativo_esperado = criar_notebook_esperado(
            2, vulnerabilidades=[{"id_vulnerabilidade": 1, "status_tratamento": 1}]
        )
        ativo_esperado["fator_exposicao"] = 1.7
        ativo_esperado["dependencias"] = [{"id_ativo_do_qual_depende": 3, "fracao": 0.4}]
        ativo_esperado.update(campos_alterados)
        return ativo_esperado

    def conferir_ativo_2_editado(self, resposta, ativo_esperado):
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.get_json(), ativo_esperado)
        self.conferir_memoria_e_banco(
            {
                "ativos": {2: ativo_esperado, 3: criar_notebook_esperado(3)},
                "catalogo": {1: criar_log4shell_gravada()},
            }
        )

    def test_editar_devolve_200_e_grava_mantendo_vinculos_e_dependencias(self):
        corpo = criar_corpo_de_notebook(2)
        corpo["status"] = 3
        corpo["tela"] = 15.6
        corpo["fator_exposicao"] = 1.7

        resposta = self.editar(2, corpo)

        self.conferir_ativo_2_editado(resposta, self.criar_ativo_2_esperado(status=3, tela=15.6))

    def test_fator_que_nao_veio_continua_o_atual_quando_o_tipo_nao_muda(self):
        for fator_enviado in ["campo ausente", None]:
            with self.subTest(fator_enviado=fator_enviado):
                corpo = criar_corpo_de_notebook(2)
                if fator_enviado is None:
                    corpo["fator_exposicao"] = None

                resposta = self.editar(2, corpo)

                self.conferir_ativo_2_editado(resposta, self.criar_ativo_2_esperado())

    def test_fator_que_nao_veio_volta_ao_padrao_quando_o_tipo_muda(self):
        corpo = {
            "tipo": "Servidor",
            "id": 2,
            "nome": "Servidor do Rafael",
            "setor": 1,
            "responsavel": "Rafael Torres",
            "status": 1,
            "ram": 32,
            "armazenamento": 4.0,
        }

        resposta = self.editar(2, corpo)

        servidor_esperado = self.criar_ativo_2_esperado(
            nome="Servidor do Rafael", tipo="Servidor", fator_exposicao=1.3, ram=32
        )
        del servidor_esperado["sistema_operacional"]
        del servidor_esperado["tela"]
        servidor_esperado["armazenamento"] = 4.0
        self.conferir_ativo_2_editado(resposta, servidor_esperado)

    def test_fator_enviado_e_o_que_vale(self):
        corpo = criar_corpo_de_notebook(2)
        corpo["fator_exposicao"] = 0.5

        resposta = self.editar(2, corpo)

        self.conferir_ativo_2_editado(resposta, self.criar_ativo_2_esperado(fator_exposicao=0.5))

    def test_o_id_da_url_vale_mais_que_o_id_do_corpo(self):
        corpo = criar_corpo_de_notebook(50)
        corpo["fator_exposicao"] = 1.7

        resposta = self.editar(2, corpo)

        self.conferir_ativo_2_editado(resposta, self.criar_ativo_2_esperado())

    def test_editar_ativo_inexistente_devolve_404_sem_alterar_nada(self):
        estado_antes = self.estado_da_memoria()

        resposta = self.editar(99, criar_corpo_de_notebook(99))

        self.conferir_erro_sem_alteracao(resposta, 404, "Ativo não encontrado.", estado_antes)

    def test_editar_com_dado_invalido_devolve_400_sem_alterar_nada(self):
        estado_antes = self.estado_da_memoria()
        corpo = criar_corpo_de_notebook(2)
        corpo["responsavel"] = ""

        resposta = self.editar(2, corpo)

        self.conferir_erro_sem_alteracao(
            resposta, 400, "Este campo não pode ser vazio.", estado_antes
        )

    def test_editar_sem_campo_obrigatorio_devolve_400_sem_alterar_nada(self):
        estado_antes = self.estado_da_memoria()
        corpo = criar_corpo_de_notebook(2)
        del corpo["tela"]

        resposta = self.editar(2, corpo)

        self.conferir_erro_sem_alteracao(
            resposta, 400, MENSAGEM_DE_DADOS_DO_ATIVO_INVALIDOS, estado_antes
        )

    def test_editar_com_corpo_que_nao_e_json_devolve_400_sem_alterar_nada(self):
        estado_antes = self.estado_da_memoria()

        resposta = self.cliente.put("/ativos/2", data="Rafael Torres", content_type="text/plain")

        self.conferir_erro_sem_alteracao(
            resposta, 400, MENSAGEM_DE_DADOS_DO_ATIVO_INVALIDOS, estado_antes
        )

    def test_falha_do_banco_ao_editar_devolve_500_sem_alterar_nada(self):
        estado_antes = self.estado_da_memoria()
        falha_do_banco = PersistenciaError("Não foi possível gravar no banco de dados.")

        with patch.object(self.repositorio, "atualizar_ativo", side_effect=falha_do_banco):
            resposta = self.editar(2, criar_corpo_de_notebook(2))

        self.conferir_erro_sem_alteracao(
            resposta, 500, "Não foi possível gravar no banco de dados.", estado_antes
        )


class TesteDeExclusaoDeAtivo(TesteDaApi):

    def setUp(self):
        super().setUp()
        self.cadastrar_notebook(2)
        self.cadastrar_notebook(3)
        self.cadastrar_vulnerabilidade()
        self.vincular(2, 1)
        cadastrar_dependencia(self.repositorio, self.ativos, 3, 2, 0.4)

    def test_excluir_devolve_204_e_tira_o_ativo_e_as_dependencias_que_apontavam_para_ele(self):
        resposta = self.cliente.delete("/ativos/2")

        self.assertEqual(resposta.status_code, 204)
        self.assertEqual(resposta.get_data(as_text=True), "")
        self.conferir_memoria_e_banco(
            {"ativos": {3: criar_notebook_esperado(3)}, "catalogo": {1: criar_log4shell_gravada()}}
        )

    def test_excluir_ativo_inexistente_devolve_404_sem_alterar_nada(self):
        estado_antes = self.estado_da_memoria()

        resposta = self.cliente.delete("/ativos/99")

        self.conferir_erro_sem_alteracao(resposta, 404, "Ativo não encontrado.", estado_antes)

    def test_falha_do_banco_ao_excluir_devolve_500_sem_alterar_nada(self):
        estado_antes = self.estado_da_memoria()
        falha_do_banco = PersistenciaError("Não foi possível gravar no banco de dados.")

        with patch.object(self.repositorio, "remover_ativo", side_effect=falha_do_banco):
            resposta = self.cliente.delete("/ativos/2")

        self.conferir_erro_sem_alteracao(
            resposta, 500, "Não foi possível gravar no banco de dados.", estado_antes
        )


class TesteDeVulnerabilidades(TesteDaApi):

    def test_cadastrar_vulnerabilidade_devolve_201_com_id_gerado(self):
        resposta = self.cadastrar_vulnerabilidade()

        self.assertEqual(resposta.status_code, 201)
        self.assertEqual(resposta.get_json(), criar_log4shell_na_resposta())

    def test_cadastrar_vulnerabilidade_grava_na_memoria_e_no_banco(self):
        self.cadastrar_vulnerabilidade()

        self.conferir_memoria_e_banco({"ativos": {}, "catalogo": {1: criar_log4shell_gravada()}})

    def test_listar_vulnerabilidades_devolve_o_catalogo_completo(self):
        self.cadastrar_vulnerabilidade()

        resposta = self.cliente.get("/vulnerabilidades")

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.get_json(), [criar_log4shell_na_resposta()])

    def test_o_nivel_acompanha_a_faixa_do_cvss(self):
        notas_e_niveis = [(3.9, "BAIXO"), (4.0, "MEDIO"), (7.0, "ALTO"), (9.0, "CRITICO")]
        for cvss, _ in notas_e_niveis:
            self.cadastrar_vulnerabilidade(nome=f"Vulnerabilidade com CVSS {cvss}", cvss=cvss)

        resposta = self.cliente.get("/vulnerabilidades")

        niveis_na_resposta = []
        for vulnerabilidade in resposta.get_json():
            niveis_na_resposta.append((vulnerabilidade["cvss"], vulnerabilidade["nivel"]))
        self.assertEqual(niveis_na_resposta, notas_e_niveis)

    def test_buscar_vulnerabilidade_existente_devolve_200_com_o_nivel(self):
        self.cadastrar_vulnerabilidade()

        resposta = self.cliente.get("/vulnerabilidades/1")

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.get_json(), criar_log4shell_na_resposta())

    def test_buscar_vulnerabilidade_inexistente_devolve_404(self):
        resposta = self.cliente.get("/vulnerabilidades/99")

        self.assertEqual(resposta.status_code, 404)
        self.assertEqual(
            resposta.get_json(), {"erro": "Vulnerabilidade não encontrada no catálogo."}
        )

    def test_cadastrar_vulnerabilidade_com_cvss_fora_do_limite_devolve_400_sem_alterar_nada(self):
        estado_antes = self.estado_da_memoria()

        resposta = self.cadastrar_vulnerabilidade(cvss=15)

        self.conferir_erro_sem_alteracao(
            resposta, 400, "O CVSS deve estar entre 0.1 e 10.", estado_antes
        )

    def test_cadastrar_vulnerabilidade_com_cvss_em_texto_devolve_400_sem_alterar_nada(self):
        estado_antes = self.estado_da_memoria()

        resposta = self.cadastrar_vulnerabilidade(cvss="abc")

        self.conferir_erro_sem_alteracao(
            resposta, 400, "Este campo precisa ser um número.", estado_antes
        )

    def test_cadastrar_vulnerabilidade_com_cvss_booleano_devolve_400_sem_alterar_nada(self):
        estado_antes = self.estado_da_memoria()

        resposta = self.cadastrar_vulnerabilidade(cvss=True)

        self.conferir_erro_sem_alteracao(
            resposta, 400, "Este campo precisa ser um número.", estado_antes
        )

    def test_cadastrar_vulnerabilidade_com_nome_vazio_devolve_400_sem_alterar_nada(self):
        estado_antes = self.estado_da_memoria()

        resposta = self.cadastrar_vulnerabilidade(nome="")

        self.conferir_erro_sem_alteracao(
            resposta, 400, "Este campo não pode ser vazio.", estado_antes
        )

    def test_cadastrar_vulnerabilidade_sem_cvss_devolve_400_sem_alterar_nada(self):
        estado_antes = self.estado_da_memoria()

        resposta = self.cliente.post(
            "/vulnerabilidades", json={"nome_vulnerabilidade": "Log4Shell"}
        )

        self.conferir_erro_sem_alteracao(
            resposta, 400, MENSAGEM_DE_DADOS_DA_VULNERABILIDADE_INVALIDOS, estado_antes
        )


class TesteDeEdicaoDeVulnerabilidade(TesteDaApi):

    def setUp(self):
        super().setUp()
        self.cadastrar_notebook(2)
        self.cadastrar_vulnerabilidade()
        self.vincular(2, 1)

    def editar(self, corpo):
        return self.cliente.put("/vulnerabilidades/1", json=corpo)

    def conferir_log4shell_editada(self, resposta, nome_esperado, cvss_esperado, nivel_esperado):
        log4shell_gravada = {
            "id_vulnerabilidade": 1,
            "nome_vulnerabilidade": nome_esperado,
            "cvss": cvss_esperado,
        }
        log4shell_na_resposta = dict(log4shell_gravada)
        log4shell_na_resposta["nivel"] = nivel_esperado
        notebook_com_vinculo = criar_notebook_esperado(
            2, vulnerabilidades=[{"id_vulnerabilidade": 1, "status_tratamento": 1}]
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.get_json(), log4shell_na_resposta)
        self.conferir_memoria_e_banco(
            {"ativos": {2: notebook_com_vinculo}, "catalogo": {1: log4shell_gravada}}
        )

    def test_editar_nome_e_cvss_devolve_200_e_recalcula_o_nivel(self):
        resposta = self.editar({"nome_vulnerabilidade": "Log4Shell (Rafael)", "cvss": 5.0})

        self.conferir_log4shell_editada(resposta, "Log4Shell (Rafael)", 5.0, "MEDIO")

    def test_cvss_que_nao_veio_continua_o_atual(self):
        resposta = self.editar({"nome_vulnerabilidade": "Log4Shell (Rafael)"})

        self.conferir_log4shell_editada(resposta, "Log4Shell (Rafael)", 10, "CRITICO")

    def test_nome_que_nao_veio_continua_o_atual(self):
        resposta = self.editar({"cvss": 7.5})

        self.conferir_log4shell_editada(resposta, "Log4Shell", 7.5, "ALTO")

    def test_campos_nulos_ou_ausentes_continuam_os_atuais(self):
        for corpo in [{}, {"nome_vulnerabilidade": None, "cvss": None}]:
            with self.subTest(corpo=corpo):
                resposta = self.editar(corpo)

                self.conferir_log4shell_editada(resposta, "Log4Shell", 10, "CRITICO")

    def test_editar_com_cvss_fora_do_limite_devolve_400_sem_alterar_nada(self):
        estado_antes = self.estado_da_memoria()

        resposta = self.editar({"cvss": 15})

        self.conferir_erro_sem_alteracao(
            resposta, 400, "O CVSS deve estar entre 0.1 e 10.", estado_antes
        )

    def test_editar_com_nome_vazio_devolve_400_sem_alterar_nada(self):
        estado_antes = self.estado_da_memoria()

        resposta = self.editar({"nome_vulnerabilidade": ""})

        self.conferir_erro_sem_alteracao(
            resposta, 400, "Este campo não pode ser vazio.", estado_antes
        )

    def test_editar_vulnerabilidade_inexistente_devolve_404_sem_alterar_nada(self):
        estado_antes = self.estado_da_memoria()

        resposta = self.cliente.put("/vulnerabilidades/99", json={"cvss": 5.0})

        self.conferir_erro_sem_alteracao(
            resposta, 404, "Vulnerabilidade não encontrada no catálogo.", estado_antes
        )

    def test_editar_com_corpo_que_nao_e_json_devolve_400_sem_alterar_nada(self):
        estado_antes = self.estado_da_memoria()

        resposta = self.cliente.put(
            "/vulnerabilidades/1", data="Rafael Torres", content_type="text/plain"
        )

        self.conferir_erro_sem_alteracao(
            resposta, 400, MENSAGEM_DE_DADOS_DA_VULNERABILIDADE_INVALIDOS, estado_antes
        )

    def test_falha_do_banco_ao_editar_devolve_500_sem_alterar_nada(self):
        estado_antes = self.estado_da_memoria()
        falha_do_banco = PersistenciaError("Não foi possível gravar no banco de dados.")

        with patch.object(
            self.repositorio, "atualizar_vulnerabilidade", side_effect=falha_do_banco
        ):
            resposta = self.editar({"cvss": 5.0})

        self.conferir_erro_sem_alteracao(
            resposta, 500, "Não foi possível gravar no banco de dados.", estado_antes
        )


class TesteDeExclusaoDeVulnerabilidade(TesteDaApi):

    def setUp(self):
        super().setUp()
        self.cadastrar_notebook(2)
        self.cadastrar_vulnerabilidade()
        self.vincular(2, 1)

    def test_excluir_devolve_204_e_desvincula_de_todos_os_ativos(self):
        resposta = self.cliente.delete("/vulnerabilidades/1")

        self.assertEqual(resposta.status_code, 204)
        self.assertEqual(resposta.get_data(as_text=True), "")
        self.conferir_memoria_e_banco({"ativos": {2: criar_notebook_esperado(2)}, "catalogo": {}})

    def test_excluir_vulnerabilidade_inexistente_devolve_404_sem_alterar_nada(self):
        estado_antes = self.estado_da_memoria()

        resposta = self.cliente.delete("/vulnerabilidades/99")

        self.conferir_erro_sem_alteracao(
            resposta, 404, "Vulnerabilidade não encontrada no catálogo.", estado_antes
        )

    def test_falha_do_banco_ao_excluir_devolve_500_sem_alterar_nada(self):
        estado_antes = self.estado_da_memoria()
        falha_do_banco = PersistenciaError("Não foi possível gravar no banco de dados.")

        with patch.object(self.repositorio, "remover_vulnerabilidade", side_effect=falha_do_banco):
            resposta = self.cliente.delete("/vulnerabilidades/1")

        self.conferir_erro_sem_alteracao(
            resposta, 500, "Não foi possível gravar no banco de dados.", estado_antes
        )


class TesteDeCorposInvalidos(TesteDaApi):

    def setUp(self):
        super().setUp()
        self.mensagem_esperada_por_rota = {
            "/ativos": MENSAGEM_DE_DADOS_DO_ATIVO_INVALIDOS,
            "/vulnerabilidades": MENSAGEM_DE_DADOS_DA_VULNERABILIDADE_INVALIDOS,
            "/ativos/2/vulnerabilidades": MENSAGEM_DE_DADOS_DO_VINCULO_INVALIDOS,
        }

    def enviar_corpo_para_cada_rota(self, corpo_em_texto, tipo_do_conteudo):
        for rota, mensagem_esperada in self.mensagem_esperada_por_rota.items():
            with self.subTest(rota=rota):
                estado_antes = self.estado_da_memoria()

                resposta = self.cliente.post(
                    rota, data=corpo_em_texto, content_type=tipo_do_conteudo
                )

                self.conferir_erro_sem_alteracao(resposta, 400, mensagem_esperada, estado_antes)

    def test_corpo_que_nao_e_json_devolve_400_em_json_sem_alterar_nada(self):
        self.enviar_corpo_para_cada_rota("Rafael Torres", "text/plain")

    def test_json_malformado_devolve_400_em_json_sem_alterar_nada(self):
        self.enviar_corpo_para_cada_rota('{"tipo": "Notebook",', "application/json")


class TesteDeNumerosNaoFinitos(TesteDaApi):

    def enviar_corpo_em_texto(self, rota, corpo):
        corpo_em_texto = json.dumps(corpo)
        return self.cliente.post(rota, data=corpo_em_texto, content_type="application/json")

    def test_o_corpo_enviado_tem_nan_e_infinity_escritos_como_texto(self):
        corpo_em_texto = json.dumps({"cvss": float("nan"), "tela": float("inf")})

        self.assertEqual(corpo_em_texto, '{"cvss": NaN, "tela": Infinity}')

    def test_cvss_nao_finito_devolve_400_sem_alterar_nada(self):
        for valor in [float("nan"), float("inf"), float("-inf")]:
            with self.subTest(cvss=valor):
                estado_antes = self.estado_da_memoria()

                resposta = self.enviar_corpo_em_texto(
                    "/vulnerabilidades", {"nome_vulnerabilidade": "Log4Shell", "cvss": valor}
                )

                self.conferir_erro_sem_alteracao(
                    resposta, 400, "Este campo precisa ser um número finito.", estado_antes
                )

    def test_fator_de_exposicao_nan_devolve_400_sem_alterar_nada(self):
        estado_antes = self.estado_da_memoria()
        corpo = criar_corpo_de_notebook()
        corpo["fator_exposicao"] = float("nan")

        resposta = self.enviar_corpo_em_texto("/ativos", corpo)

        self.conferir_erro_sem_alteracao(
            resposta, 400, "Este campo precisa ser um número finito.", estado_antes
        )

    def test_tela_infinita_devolve_400_sem_alterar_nada(self):
        estado_antes = self.estado_da_memoria()
        corpo = criar_corpo_de_notebook()
        corpo["tela"] = float("inf")

        resposta = self.enviar_corpo_em_texto("/ativos", corpo)

        self.conferir_erro_sem_alteracao(
            resposta, 400, "Este campo precisa ser um número finito.", estado_antes
        )


class TesteDeInteirosAcimaDoLimite(TesteDaApi):

    mensagem_esperada = "Este número é grande demais. O máximo aceito é 9223372036854775807."

    def test_maior_inteiro_aceito_como_id_e_gravado_na_memoria_e_no_banco(self):
        maior_inteiro_aceito = 2**63 - 1

        resposta = self.cadastrar_notebook(maior_inteiro_aceito)

        self.assertEqual(resposta.status_code, 201)
        self.conferir_memoria_e_banco(
            {
                "ativos": {maior_inteiro_aceito: criar_notebook_esperado(maior_inteiro_aceito)},
                "catalogo": {},
            }
        )

    def test_id_acima_do_limite_devolve_400_sem_alterar_nada(self):
        estado_antes = self.estado_da_memoria()

        resposta = self.cadastrar_notebook(2**63)

        self.conferir_erro_sem_alteracao(resposta, 400, self.mensagem_esperada, estado_antes)

    def test_tela_inteira_acima_do_limite_devolve_400_sem_alterar_nada(self):
        estado_antes = self.estado_da_memoria()

        resposta = self.cadastrar_notebook_com_campo_alterado("tela", 10**30)

        self.conferir_erro_sem_alteracao(resposta, 400, self.mensagem_esperada, estado_antes)

    def test_ram_do_servidor_acima_do_limite_devolve_400_sem_alterar_nada(self):
        estado_antes = self.estado_da_memoria()
        corpo = {
            "tipo": "Servidor",
            "id": 2,
            "nome": "Servidor do Rafael",
            "setor": 1,
            "responsavel": "Rafael Torres",
            "status": 1,
            "ram": 2**63,
            "armazenamento": 4.0,
        }

        resposta = self.cliente.post("/ativos", json=corpo)

        self.conferir_erro_sem_alteracao(resposta, 400, self.mensagem_esperada, estado_antes)

    def test_id_da_vulnerabilidade_acima_do_limite_no_vinculo_devolve_400_sem_alterar_nada(self):
        self.cadastrar_notebook()
        self.cadastrar_vulnerabilidade()
        estado_antes = self.estado_da_memoria()

        resposta = self.vincular(2, 2**63)

        self.conferir_erro_sem_alteracao(resposta, 400, self.mensagem_esperada, estado_antes)


class TesteDeErrosHttp(TesteDaApi):

    def test_rota_inexistente_devolve_404_em_json(self):
        resposta = self.cliente.get("/rota-que-nao-existe")

        self.assertEqual(resposta.status_code, 404)
        self.assertEqual(resposta.get_json(), {"erro": "Rota não encontrada."})

    def test_id_em_texto_na_url_devolve_404_em_json(self):
        resposta = self.cliente.get("/ativos/abc")

        self.assertEqual(resposta.status_code, 404)
        self.assertEqual(resposta.get_json(), {"erro": "Rota não encontrada."})

    def test_metodo_nao_permitido_devolve_405_em_json(self):
        resposta = self.cliente.delete("/saude")

        self.assertEqual(resposta.status_code, 405)
        self.assertEqual(resposta.get_json(), {"erro": "Método não permitido para esta rota."})

    def test_erro_inesperado_devolve_500_em_json_sem_detalhes_internos(self):
        estado_antes = self.estado_da_memoria()
        erro_inesperado = RuntimeError("detalhe interno que não pode vazar")

        with patch.object(self.repositorio, "adicionar_ativo", side_effect=erro_inesperado):
            resposta = self.cadastrar_notebook()

        self.conferir_erro_sem_alteracao(resposta, 500, "Erro interno do servidor.", estado_antes)
        self.assertNotIn("detalhe interno", resposta.get_data(as_text=True))


class TesteDeFalhaDePersistencia(TesteDaApi):

    mensagem_da_falha = "Não foi possível gravar no banco de dados."

    def banco_falhando_em(self, nome_da_operacao):
        falha_do_banco = PersistenciaError(self.mensagem_da_falha)
        return patch.object(self.repositorio, nome_da_operacao, side_effect=falha_do_banco)

    def test_falha_ao_gravar_ativo_devolve_500_sem_alterar_memoria_nem_banco(self):
        estado_antes = self.estado_da_memoria()

        with self.banco_falhando_em("adicionar_ativo"):
            resposta = self.cadastrar_notebook()

        self.conferir_erro_sem_alteracao(resposta, 500, self.mensagem_da_falha, estado_antes)

    def test_falha_ao_gravar_vulnerabilidade_devolve_500_sem_alterar_memoria_nem_banco(self):
        estado_antes = self.estado_da_memoria()

        with self.banco_falhando_em("adicionar_vulnerabilidade"):
            resposta = self.cadastrar_vulnerabilidade()

        self.conferir_erro_sem_alteracao(resposta, 500, self.mensagem_da_falha, estado_antes)

    def test_falha_ao_gravar_vinculo_devolve_500_sem_alterar_memoria_nem_banco(self):
        self.cadastrar_notebook()
        self.cadastrar_vulnerabilidade()
        estado_antes = self.estado_da_memoria()

        with self.banco_falhando_em("vincular"):
            resposta = self.vincular(2, 1)

        self.conferir_erro_sem_alteracao(resposta, 500, self.mensagem_da_falha, estado_antes)


class TesteDeVinculos(TesteDaApi):

    def setUp(self):
        super().setUp()
        self.cadastrar_notebook()
        self.cadastrar_vulnerabilidade()

    def test_vincular_devolve_201_com_o_ativo_e_o_vinculo(self):
        resposta = self.vincular(2, 1)

        self.assertEqual(resposta.status_code, 201)
        self.assertEqual(
            resposta.get_json(),
            criar_notebook_esperado(
                vulnerabilidades=[{"id_vulnerabilidade": 1, "status_tratamento": 1}]
            ),
        )

    def test_vincular_grava_na_memoria_e_no_banco(self):
        self.vincular(2, 1)

        ativo_esperado = criar_notebook_esperado(
            vulnerabilidades=[{"id_vulnerabilidade": 1, "status_tratamento": 1}]
        )
        self.conferir_memoria_e_banco(
            {"ativos": {2: ativo_esperado}, "catalogo": {1: criar_log4shell_gravada()}}
        )

    def test_vincular_duas_vezes_devolve_400_sem_alterar_nada(self):
        self.vincular(2, 1)
        estado_antes = self.estado_da_memoria()

        resposta = self.vincular(2, 1)

        self.conferir_erro_sem_alteracao(
            resposta, 400, "Esta vulnerabilidade já está vinculada a este ativo.", estado_antes
        )

    def test_vincular_a_ativo_inexistente_devolve_404_sem_alterar_nada(self):
        estado_antes = self.estado_da_memoria()

        resposta = self.vincular(99, 1)

        self.conferir_erro_sem_alteracao(resposta, 404, "Ativo não encontrado.", estado_antes)

    def test_vincular_vulnerabilidade_inexistente_devolve_404_sem_alterar_nada(self):
        estado_antes = self.estado_da_memoria()

        resposta = self.vincular(2, 99)

        self.conferir_erro_sem_alteracao(
            resposta, 404, "Vulnerabilidade não encontrada no catálogo.", estado_antes
        )

    def test_vincular_com_status_inexistente_devolve_400_sem_alterar_nada(self):
        estado_antes = self.estado_da_memoria()

        resposta = self.vincular(2, 1, status_tratamento=9)

        self.conferir_erro_sem_alteracao(
            resposta, 400, MENSAGEM_DE_DADOS_DO_VINCULO_INVALIDOS, estado_antes
        )

    def test_status_do_vinculo_aceita_so_inteiro(self):
        for valor in [True, 1.0]:
            with self.subTest(status_tratamento=valor):
                estado_antes = self.estado_da_memoria()

                resposta = self.vincular(2, 1, status_tratamento=valor)

                self.conferir_erro_sem_alteracao(
                    resposta, 400, "Este campo precisa ser um número inteiro.", estado_antes
                )

    def test_id_da_vulnerabilidade_no_vinculo_aceita_so_inteiro(self):
        for valor in [True, 1.0]:
            with self.subTest(id_vulnerabilidade=valor):
                estado_antes = self.estado_da_memoria()

                resposta = self.vincular(2, valor)

                self.conferir_erro_sem_alteracao(
                    resposta, 400, "Este campo precisa ser um número inteiro.", estado_antes
                )


class TesteDeRiscos(TesteDaApi):

    def test_riscos_sem_ativos_devolve_lista_vazia(self):
        resposta = self.cliente.get("/riscos")

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.get_json(), [])

    def test_riscos_devolve_o_ranking_completo_com_o_ativo_vulneravel_em_primeiro(self):
        self.cadastrar_notebook(1)
        self.cadastrar_notebook(2)
        self.cadastrar_vulnerabilidade()
        self.vincular(2, 1)

        resposta = self.cliente.get("/riscos")

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(
            resposta.get_json(),
            [
                {
                    "posicao": 1,
                    "id": 2,
                    "nome": "Notebook do Rafael",
                    "tipo": "Notebook",
                    "fator_exposicao": 1.2,
                    "risco_proprio": 12.0,
                    "risco_herdado": 0.0,
                    "risco_efetivo": 12.0,
                },
                {
                    "posicao": 2,
                    "id": 1,
                    "nome": "Notebook do Rafael",
                    "tipo": "Notebook",
                    "fator_exposicao": 1.2,
                    "risco_proprio": 0.0,
                    "risco_herdado": 0.0,
                    "risco_efetivo": 0.0,
                },
            ],
        )


if __name__ == "__main__":
    unittest.main()
