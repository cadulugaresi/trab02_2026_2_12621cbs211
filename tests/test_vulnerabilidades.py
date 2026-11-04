import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from inventario.interface.entradas import pedir_cvss, pedir_float, pedir_status_vulnerabilidade
from inventario.dominio.enums import NivelDaVulnerabilidade, Setor, StatusDaVuln, StatusDoAtivo
from inventario.dominio.excecoes import DadoInvalidoError
from inventario.dominio.ativo import Notebook, Servidor
from inventario.dominio.vulnerabilidade import Vulnerabilidade
from inventario.interface.ativos import escolher_ativo_com_vulnerabilidades, perguntar_ativo
from inventario.interface.vulnerabilidades import (
    cadastrar_vulnerabilidade,
    confirmar_exclusao_vuln,
    editar_vulnerabilidade,
    encontrar_vulnerabilidade,
    mostrar_vulnerabilidade,
    mostrar_vulnerabilidades_do_ativo,
    vincular_a_um_ativo,
)
from inventario.servicos.vulnerabilidades import (
    atualizar_status_vulnerabilidade,
    desvincular_vulnerabilidade,
    excluir_vulnerabilidade_do_catalogo,
    proximo_id,
    vincular_vulnerabilidade,
)
from inventario.persistencia.arquivos_json import (
    carregar_catalogo,
    carregar_dados,
    salvar_catalogo,
    salvar_dados,
)
from inventario.interface.conversao_das_opcoes_do_menu import validar_status_vulnerabilidade
from tests.apoio import TesteComArquivosTemporarios


def criar_catalogo():
    return {
        1: Vulnerabilidade(1, "Senha padrão", 9.8),
        3: Vulnerabilidade(3, "TLS 1.0 ativo", 5.3),
    }


def criar_notebook():
    return Notebook(1, "Dell", Setor.TI, "Rafael Torres", StatusDoAtivo.ATIVO, "Linux", 15.6)


def criar_servidor():
    return Servidor(2, "PowerEdge", Setor.TI, "Rafael Torres", StatusDoAtivo.ATIVO, 32, 4)


def capturar_saida(funcao, *argumentos):
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        funcao(*argumentos)
    return buffer.getvalue()


# Classe Vulnerabilidade -------------------------


class TestNivelDaVulnerabilidade(unittest.TestCase):

    def test_baixo_abaixo_de_4(self):
        self.assertEqual(Vulnerabilidade(1, "X", 2.0).nivel(), NivelDaVulnerabilidade.BAIXO)
        self.assertEqual(Vulnerabilidade(1, "X", 3.9).nivel(), NivelDaVulnerabilidade.BAIXO)

    def test_medio_de_4_a_6_9(self):
        self.assertEqual(Vulnerabilidade(1, "X", 4.0).nivel(), NivelDaVulnerabilidade.MEDIO)
        self.assertEqual(Vulnerabilidade(1, "X", 6.9).nivel(), NivelDaVulnerabilidade.MEDIO)

    def test_alto_de_7_a_8_9(self):
        self.assertEqual(Vulnerabilidade(1, "X", 7.0).nivel(), NivelDaVulnerabilidade.ALTO)
        self.assertEqual(Vulnerabilidade(1, "X", 8.9).nivel(), NivelDaVulnerabilidade.ALTO)

    def test_critico_a_partir_de_9(self):
        self.assertEqual(Vulnerabilidade(1, "X", 9.0).nivel(), NivelDaVulnerabilidade.CRITICO)
        self.assertEqual(Vulnerabilidade(1, "X", 10.0).nivel(), NivelDaVulnerabilidade.CRITICO)


class TestSerializacaoVulnerabilidade(unittest.TestCase):

    def setUp(self):
        self.vulnerabilidade = Vulnerabilidade(3, "TLS 1.0 ativo", 5.3)

    def test_para_dicionario_tem_as_chaves_certas(self):
        dicionario = self.vulnerabilidade.para_dicionario()
        self.assertEqual(
            dicionario,
            {"id_vulnerabilidade": 3, "nome_vulnerabilidade": "TLS 1.0 ativo", "cvss": 5.3},
        )

    def test_de_dicionario_reconstroi_igual(self):
        dicionario = self.vulnerabilidade.para_dicionario()
        reconstruida = Vulnerabilidade.de_dicionario(dicionario)
        self.assertEqual(reconstruida.id_vulnerabilidade, 3)
        self.assertEqual(reconstruida.nome_vulnerabilidade, "TLS 1.0 ativo")
        self.assertEqual(reconstruida.cvss, 5.3)


class TestVinculosNoAtivo(unittest.TestCase):

    def test_ativo_comeca_sem_vinculos(self):
        self.assertEqual(criar_notebook().vulnerabilidades, {})

    def test_para_dicionario_salva_vinculos_como_lista(self):
        notebook = criar_notebook()
        notebook.vulnerabilidades[3] = StatusDaVuln.EM_TRATAMENTO
        dicionario = notebook.para_dicionario()
        self.assertEqual(
            dicionario["vulnerabilidades"],
            [{"id_vulnerabilidade": 3, "status_tratamento": 2}],  # ID número e status pelo .value
        )


# Entradas e validações --------------------------


class TestValidarStatusVulnerabilidade(unittest.TestCase):

    def test_opcoes_validas(self):
        self.assertEqual(validar_status_vulnerabilidade("1"), StatusDaVuln.ABERTA)
        self.assertEqual(validar_status_vulnerabilidade("2"), StatusDaVuln.EM_TRATAMENTO)
        self.assertEqual(validar_status_vulnerabilidade("3"), StatusDaVuln.CORRIGIDA)
        self.assertEqual(validar_status_vulnerabilidade("4"), StatusDaVuln.ACEITA)

    def test_opcao_invalida_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            validar_status_vulnerabilidade("9")


class TestPedirStatusVulnerabilidade(unittest.TestCase):

    def test_retorna_aberta_digita_1(self):
        with patch("builtins.input", return_value="1"):
            self.assertEqual(pedir_status_vulnerabilidade("Digite: "), StatusDaVuln.ABERTA)

    def test_aceita_erro_e_depois_valido(self):
        with patch("builtins.input", side_effect=["9", "4"]):  # primeiro errado, depois certo
            self.assertEqual(pedir_status_vulnerabilidade("Digite: "), StatusDaVuln.ACEITA)


class TestPedirFloatComVirgula(unittest.TestCase):

    def test_aceita_virgula(self):
        with patch("builtins.input", return_value="2,5"):
            self.assertEqual(pedir_float("Digite: "), 2.5)


class TestPedirCvss(unittest.TestCase):

    def test_aceita_nota_valida(self):
        with patch("builtins.input", return_value="9.8"):
            self.assertEqual(pedir_cvss("Digite: "), 9.8)

    def test_aceita_virgula(self):
        with patch("builtins.input", return_value="9,8"):
            self.assertEqual(pedir_cvss("Digite: "), 9.8)

    def test_rejeita_maior_que_10_e_pede_de_novo(self):
        with patch("builtins.input", side_effect=["15", "7"]):
            self.assertEqual(pedir_cvss("Digite: "), 7.0)

    def test_arredonda_para_uma_casa(self):
        with patch("builtins.input", return_value="3.94"):
            self.assertEqual(pedir_cvss("Digite: "), 3.9)


# Catálogo ---------------------------------------


class TestProximoId(unittest.TestCase):

    def test_dicionario_vazio_comeca_em_1(self):
        self.assertEqual(proximo_id({}), 1)

    def test_maior_id_mais_1(self):
        self.assertEqual(proximo_id({1: "a", 2: "b", 3: "c"}), 4)

    def test_nao_repete_id_depois_de_exclusao(self):
        self.assertEqual(proximo_id({1: "a", 3: "c"}), 4)  # com len() + 1 daria 3, que já existe


class TestCadastrarVulnerabilidade(TesteComArquivosTemporarios):

    def test_cria_com_proximo_id(self):
        catalogo = criar_catalogo()
        with patch("builtins.input", side_effect=["SMB desatualizado", "8,1"]):
            with redirect_stdout(io.StringIO()):
                nova = cadastrar_vulnerabilidade(catalogo)
        self.assertEqual(nova.id_vulnerabilidade, 4)
        self.assertEqual(nova.nome_vulnerabilidade, "SMB desatualizado")
        self.assertEqual(nova.cvss, 8.1)

    def test_guarda_no_catalogo(self):
        catalogo = criar_catalogo()
        with patch("builtins.input", side_effect=["SMB desatualizado", "8.1"]):
            with redirect_stdout(io.StringIO()):
                nova = cadastrar_vulnerabilidade(catalogo)
        self.assertEqual(len(catalogo), 3)
        self.assertIs(catalogo[4], nova)

    def test_salva_no_arquivo(self):
        catalogo = criar_catalogo()
        with patch("builtins.input", side_effect=["SMB desatualizado", "8.1"]):
            with redirect_stdout(io.StringIO()):
                cadastrar_vulnerabilidade(catalogo)
        self.assertEqual(len(carregar_catalogo()), 3)


class TestMostrarVulnerabilidade(unittest.TestCase):

    def test_mostra_dados_do_catalogo(self):
        saida = capturar_saida(mostrar_vulnerabilidade, Vulnerabilidade(1, "Senha fraca", 8.1))
        self.assertIn("Senha fraca", saida)
        self.assertIn("8.1", saida)
        self.assertIn("alto", saida)

    def test_sem_status_nao_mostra_status(self):
        saida = capturar_saida(mostrar_vulnerabilidade, Vulnerabilidade(1, "Senha fraca", 8.1))
        self.assertNotIn("Status", saida)

    def test_com_status_mostra_status(self):
        saida = capturar_saida(
            mostrar_vulnerabilidade, Vulnerabilidade(1, "Senha fraca", 8.1), StatusDaVuln.ABERTA
        )
        self.assertIn("aberta", saida)


# Vínculos ---------------------------------------


class TestVincularVulnerabilidade(TesteComArquivosTemporarios):

    def setUp(self):
        super().setUp()
        self.catalogo = criar_catalogo()
        self.notebook = criar_notebook()
        self.servidor = criar_servidor()
        self.ativos = {1: self.notebook, 2: self.servidor}

    def test_vincula_com_status(self):
        vincular_vulnerabilidade(self.ativos, self.catalogo, 1, 3, StatusDaVuln.ABERTA)
        self.assertEqual(self.notebook.vulnerabilidades, {3: StatusDaVuln.ABERTA})

    def test_salva_no_arquivo(self):
        vincular_vulnerabilidade(self.ativos, self.catalogo, 1, 3, StatusDaVuln.ABERTA)
        self.assertIn(3, carregar_dados()[1].vulnerabilidades)

    def test_nao_vincula_duas_vezes(self):
        vincular_vulnerabilidade(self.ativos, self.catalogo, 1, 3, StatusDaVuln.ABERTA)
        with self.assertRaises(DadoInvalidoError):
            vincular_vulnerabilidade(self.ativos, self.catalogo, 1, 3, StatusDaVuln.ABERTA)

    def test_nao_vincula_vulnerabilidade_inexistente(self):
        with self.assertRaises(DadoInvalidoError):
            vincular_vulnerabilidade(self.ativos, self.catalogo, 1, 99, StatusDaVuln.ABERTA)
        self.assertEqual(self.notebook.vulnerabilidades, {})

    def test_ativo_inexistente_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            vincular_vulnerabilidade(self.ativos, self.catalogo, 99, 3, StatusDaVuln.ABERTA)

    def test_mesma_vulnerabilidade_com_status_diferente_em_cada_ativo(self):
        vincular_vulnerabilidade(self.ativos, self.catalogo, 1, 3, StatusDaVuln.ABERTA)
        vincular_vulnerabilidade(self.ativos, self.catalogo, 2, 3, StatusDaVuln.CORRIGIDA)
        self.assertEqual(self.notebook.vulnerabilidades[3], StatusDaVuln.ABERTA)
        self.assertEqual(self.servidor.vulnerabilidades[3], StatusDaVuln.CORRIGIDA)


class TestMostrarVulnerabilidadesDoAtivo(unittest.TestCase):

    def test_mostra_cada_vulnerabilidade_com_o_status_do_ativo(self):
        catalogo = criar_catalogo()
        notebook = criar_notebook()
        notebook.vulnerabilidades[1] = StatusDaVuln.ABERTA
        notebook.vulnerabilidades[3] = StatusDaVuln.CORRIGIDA
        saida = capturar_saida(mostrar_vulnerabilidades_do_ativo, notebook, catalogo)
        self.assertIn("Senha padrão", saida)
        self.assertIn("TLS 1.0 ativo", saida)
        self.assertIn("aberta", saida)
        self.assertIn("corrigida", saida)

    def test_nao_mostra_vulnerabilidade_de_outro_ativo(self):
        catalogo = criar_catalogo()
        notebook = criar_notebook()
        notebook.vulnerabilidades[1] = StatusDaVuln.ABERTA
        saida = capturar_saida(mostrar_vulnerabilidades_do_ativo, notebook, catalogo)
        self.assertNotIn("TLS 1.0 ativo", saida)


class TestAtualizarStatusVulnerabilidade(TesteComArquivosTemporarios):

    def setUp(self):
        super().setUp()
        self.notebook = criar_notebook()
        self.notebook.vulnerabilidades[3] = StatusDaVuln.ABERTA
        self.ativos = {1: self.notebook}

    def test_atualiza_status_vinculado(self):
        atualizar_status_vulnerabilidade(self.ativos, 1, 3, StatusDaVuln.CORRIGIDA)
        self.assertEqual(self.notebook.vulnerabilidades[3], StatusDaVuln.CORRIGIDA)

    def test_nao_cria_vinculo_novo(self):
        with self.assertRaises(DadoInvalidoError):
            atualizar_status_vulnerabilidade(self.ativos, 1, 1, StatusDaVuln.CORRIGIDA)
        self.assertNotIn(1, self.notebook.vulnerabilidades)

    def test_ativo_inexistente_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            atualizar_status_vulnerabilidade(self.ativos, 99, 3, StatusDaVuln.CORRIGIDA)


class TestDesvincularVulnerabilidade(TesteComArquivosTemporarios):

    def setUp(self):
        super().setUp()
        self.catalogo = criar_catalogo()
        self.notebook = criar_notebook()
        self.notebook.vulnerabilidades[1] = StatusDaVuln.ABERTA
        self.notebook.vulnerabilidades[3] = StatusDaVuln.ABERTA
        self.ativos = {1: self.notebook}

    def test_remove_so_do_ativo(self):
        desvincular_vulnerabilidade(self.ativos, 1, 3)
        self.assertEqual(self.notebook.vulnerabilidades, {1: StatusDaVuln.ABERTA})
        self.assertIn(3, self.catalogo)

    def test_nao_vinculada_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            desvincular_vulnerabilidade(self.ativos, 1, 99)

    def test_remove_vinculo_orfao(self):
        self.notebook.vulnerabilidades[50] = StatusDaVuln.ABERTA  # aponta para algo que não está no catálogo
        desvincular_vulnerabilidade(self.ativos, 1, 50)
        self.assertNotIn(50, self.notebook.vulnerabilidades)

    def test_ativo_inexistente_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            desvincular_vulnerabilidade(self.ativos, 99, 3)


class TestExcluirVulnerabilidadeDoCatalogo(TesteComArquivosTemporarios):

    def setUp(self):
        super().setUp()
        self.catalogo = criar_catalogo()
        self.notebook = criar_notebook()
        self.servidor = criar_servidor()
        self.ativos = {1: self.notebook, 2: self.servidor}

    def test_remove_do_catalogo(self):
        excluir_vulnerabilidade_do_catalogo(self.catalogo, self.ativos, 3)
        self.assertNotIn(3, self.catalogo)
        self.assertIn(1, self.catalogo)

    def test_remove_de_todos_os_ativos_vinculados(self):
        self.notebook.vulnerabilidades[3] = StatusDaVuln.ABERTA
        self.servidor.vulnerabilidades[3] = StatusDaVuln.CORRIGIDA
        excluir_vulnerabilidade_do_catalogo(self.catalogo, self.ativos, 3)
        self.assertNotIn(3, self.notebook.vulnerabilidades)
        self.assertNotIn(3, self.servidor.vulnerabilidades)

    def test_mantem_os_outros_vinculos(self):
        self.notebook.vulnerabilidades[1] = StatusDaVuln.ABERTA
        self.notebook.vulnerabilidades[3] = StatusDaVuln.ABERTA
        excluir_vulnerabilidade_do_catalogo(self.catalogo, self.ativos, 3)
        self.assertEqual(self.notebook.vulnerabilidades, {1: StatusDaVuln.ABERTA})

    def test_exclui_mesmo_sem_nenhum_vinculo(self):
        excluir_vulnerabilidade_do_catalogo(self.catalogo, self.ativos, 3)
        self.assertNotIn(3, self.catalogo)

    def test_id_inexistente_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            excluir_vulnerabilidade_do_catalogo(self.catalogo, self.ativos, 99)
        self.assertEqual(len(self.catalogo), 2)

    def test_salva_catalogo_e_ativos(self):
        self.notebook.vulnerabilidades[3] = StatusDaVuln.ABERTA
        excluir_vulnerabilidade_do_catalogo(self.catalogo, self.ativos, 3)
        self.assertNotIn(3, carregar_catalogo())
        self.assertNotIn(3, carregar_dados()[1].vulnerabilidades)


class TestConfirmarExclusaoVuln(unittest.TestCase):

    def setUp(self):
        self.vulnerabilidade = Vulnerabilidade(3, "TLS 1.0 ativo", 5.3)

    def confirmar(self, resposta):
        with patch("builtins.input", return_value=resposta):
            with redirect_stdout(io.StringIO()):
                return confirmar_exclusao_vuln(self.vulnerabilidade)

    def test_sim_confirma(self):
        self.assertTrue(self.confirmar("sim"))

    def test_sim_com_maiuscula_e_espaco_confirma(self):
        self.assertTrue(self.confirmar("  SIM "))  # o .strip().lower() cuida disso

    def test_enter_cancela(self):
        self.assertFalse(self.confirmar(""))

    def test_qualquer_outra_resposta_cancela(self):
        self.assertFalse(self.confirmar("não"))

    def test_mostra_o_nome_e_o_id(self):
        with patch("builtins.input", return_value=""):
            saida = capturar_saida(confirmar_exclusao_vuln, self.vulnerabilidade)
        self.assertIn("TLS 1.0 ativo", saida)
        self.assertIn("ID 3", saida)


class TestEditarVulnerabilidade(unittest.TestCase):

    def setUp(self):
        self.catalogo = criar_catalogo()
        self.vulnerabilidade = self.catalogo[3]

    def editar(self, respostas):
        with patch("builtins.input", side_effect=respostas):
            with redirect_stdout(io.StringIO()):
                return editar_vulnerabilidade(self.vulnerabilidade)

    def test_edita_o_nome(self):
        mudou = self.editar(["1", "TLS 1.0 habilitado"])
        self.assertTrue(mudou)
        self.assertEqual(self.vulnerabilidade.nome_vulnerabilidade, "TLS 1.0 habilitado")
        self.assertEqual(self.vulnerabilidade.cvss, 5.3)

    def test_edita_o_cvss_com_virgula(self):
        mudou = self.editar(["2", "7,4"])
        self.assertTrue(mudou)
        self.assertEqual(self.vulnerabilidade.cvss, 7.4)

    def test_cvss_editado_muda_o_nivel(self):
        self.editar(["2", "9.1"])
        self.assertEqual(self.vulnerabilidade.nivel(), NivelDaVulnerabilidade.CRITICO)

    def test_recusa_cvss_maior_que_10(self):
        self.editar(["2", "15", "8"])  # o 15 é recusado e a nota é pedida de novo
        self.assertEqual(self.vulnerabilidade.cvss, 8.0)

    def test_arredonda_cvss_editado(self):
        self.editar(["2", "3.94"])
        self.assertEqual(self.vulnerabilidade.cvss, 3.9)

    def test_voltar_nao_muda_nada(self):
        mudou = self.editar(["3"])
        self.assertFalse(mudou)
        self.assertEqual(self.vulnerabilidade.nome_vulnerabilidade, "TLS 1.0 ativo")
        self.assertEqual(self.vulnerabilidade.cvss, 5.3)

    def test_opcao_invalida_nao_muda_nada(self):
        self.assertFalse(self.editar(["x"]))
        self.assertEqual(self.vulnerabilidade.cvss, 5.3)

    def test_edita_o_mesmo_objeto_do_catalogo(self):
        self.editar(["2", "7.5"])
        self.assertEqual(self.catalogo[3].cvss, 7.5)  # sem precisar recolocar no catálogo

    def test_ativo_vinculado_ve_a_nota_nova(self):
        notebook = criar_notebook()
        notebook.vulnerabilidades[3] = StatusDaVuln.ABERTA
        self.editar(["2", "7.5"])
        saida = capturar_saida(mostrar_vulnerabilidades_do_ativo, notebook, self.catalogo)
        self.assertIn("7.5", saida)  # o ativo só guarda o ID, então já enxerga a nota nova
        self.assertNotIn("5.3", saida)


class TestVincularAUmAtivo(TesteComArquivosTemporarios):

    def setUp(self):
        super().setUp()
        self.catalogo = criar_catalogo()
        self.notebook = criar_notebook()
        self.ativos = {1: self.notebook, 2: criar_servidor()}
        self.vulnerabilidade = self.catalogo[3]

    def vincular(self, respostas, ativos=None):
        if ativos is None:
            ativos = self.ativos
        with patch("builtins.input", side_effect=respostas) as entrada:
            with redirect_stdout(io.StringIO()):
                resultado = vincular_a_um_ativo(self.vulnerabilidade, ativos, self.catalogo)
        return resultado, entrada

    def test_vincula_e_devolve_true(self):
        resultado, _ = self.vincular(["1", "2"])  # ativo 1, status EM_TRATAMENTO
        self.assertTrue(resultado)
        self.assertEqual(self.notebook.vulnerabilidades, {3: StatusDaVuln.EM_TRATAMENTO})

    def test_ativo_inexistente_devolve_false_sem_pedir_status(self):
        resultado, entrada = self.vincular(["99"])
        self.assertFalse(resultado)
        self.assertEqual(entrada.call_count, 1)

    def test_sem_ativos_devolve_false_sem_perguntar(self):
        resultado, entrada = self.vincular([], ativos={})
        self.assertFalse(resultado)
        entrada.assert_not_called()

    def test_vinculo_duplicado_devolve_false(self):
        self.notebook.vulnerabilidades[3] = StatusDaVuln.ABERTA
        resultado, _ = self.vincular(["1", "3"])
        self.assertFalse(resultado)
        self.assertEqual(self.notebook.vulnerabilidades[3], StatusDaVuln.ABERTA)


# Escolhas feitas pelo usuário -------------------


class TestPerguntarAtivo(unittest.TestCase):

    def setUp(self):
        self.ativos = {1: criar_notebook(), 2: criar_servidor()}

    def test_sem_ativos_retorna_none_sem_perguntar(self):
        with patch("builtins.input") as entrada:
            with redirect_stdout(io.StringIO()):
                self.assertIsNone(perguntar_ativo({}))
        entrada.assert_not_called()

    def test_id_existente_retorna_o_ativo(self):
        with patch("builtins.input", return_value="2"):
            with redirect_stdout(io.StringIO()):
                self.assertIs(perguntar_ativo(self.ativos), self.ativos[2])

    def test_id_inexistente_retorna_none(self):
        with patch("builtins.input", return_value="99"):
            with redirect_stdout(io.StringIO()):
                self.assertIsNone(perguntar_ativo(self.ativos))

    def test_id_inexistente_mostra_a_mensagem_do_obter_ativo(self):
        with patch("builtins.input", return_value="99"):
            saida = capturar_saida(perguntar_ativo, self.ativos)
        self.assertIn("Ativo não encontrado.", saida)


class TestEscolherAtivoComVulnerabilidades(unittest.TestCase):

    def setUp(self):
        notebook = criar_notebook()
        notebook.vulnerabilidades[1] = StatusDaVuln.ABERTA
        self.ativos = {1: notebook, 2: criar_servidor()}

    def test_ativo_com_vinculos_retorna_o_ativo(self):
        with patch("builtins.input", return_value="1"):
            with redirect_stdout(io.StringIO()):
                self.assertIs(escolher_ativo_com_vulnerabilidades(self.ativos), self.ativos[1])

    def test_ativo_sem_vinculos_retorna_none(self):
        with patch("builtins.input", return_value="2"):
            with redirect_stdout(io.StringIO()):
                self.assertIsNone(escolher_ativo_com_vulnerabilidades(self.ativos))

    def test_id_inexistente_retorna_none(self):
        with patch("builtins.input", return_value="99"):
            with redirect_stdout(io.StringIO()):
                self.assertIsNone(escolher_ativo_com_vulnerabilidades(self.ativos))

    def test_pergunta_o_id_uma_vez_so(self):
        with patch("builtins.input", return_value="1") as entrada:
            with redirect_stdout(io.StringIO()):
                escolher_ativo_com_vulnerabilidades(self.ativos)
        self.assertEqual(entrada.call_count, 1)  # pega o bug de chamar a função duas vezes


class TestEncontrarVulnerabilidade(unittest.TestCase):

    def setUp(self):
        self.catalogo = criar_catalogo()

    def test_catalogo_vazio_retorna_none_sem_perguntar(self):
        with patch("builtins.input") as entrada:
            with redirect_stdout(io.StringIO()):
                self.assertIsNone(encontrar_vulnerabilidade({}))
        entrada.assert_not_called()

    def test_id_existente_retorna_o_objeto(self):
        with patch("builtins.input", return_value="3"):
            with redirect_stdout(io.StringIO()):
                encontrada = encontrar_vulnerabilidade(self.catalogo)
        self.assertIs(encontrada, self.catalogo[3])  # devolve o objeto, não o ID

    def test_id_inexistente_retorna_none(self):
        with patch("builtins.input", return_value="99"):
            with redirect_stdout(io.StringIO()):
                self.assertIsNone(encontrar_vulnerabilidade(self.catalogo))

    def test_mostra_o_catalogo_antes_de_perguntar(self):
        with patch("builtins.input", return_value="3"):
            saida = capturar_saida(encontrar_vulnerabilidade, self.catalogo)
        self.assertIn("Senha padrão", saida)
        self.assertIn("TLS 1.0 ativo", saida)


# Persistência do catálogo e dos vínculos --------


class TestPersistenciaCatalogo(TesteComArquivosTemporarios):

    def test_carregar_catalogo_inexistente_retorna_vazio(self):
        self.assertEqual(carregar_catalogo(), {})

    def test_salva_e_recarrega_catalogo(self):
        salvar_catalogo(criar_catalogo())
        carregado = carregar_catalogo()
        self.assertEqual(len(carregado), 2)
        self.assertEqual(carregado[3].nome_vulnerabilidade, "TLS 1.0 ativo")
        self.assertEqual(carregado[3].cvss, 5.3)

    def test_salva_e_recarrega_vinculos(self):
        notebook = criar_notebook()
        notebook.vulnerabilidades[1] = StatusDaVuln.ABERTA
        notebook.vulnerabilidades[3] = StatusDaVuln.EM_TRATAMENTO
        salvar_dados({1: notebook})
        carregado = carregar_dados()[1]
        self.assertEqual(
            carregado.vulnerabilidades,
            {1: StatusDaVuln.ABERTA, 3: StatusDaVuln.EM_TRATAMENTO},  # IDs voltam como número
        )


if __name__ == "__main__":
    unittest.main()