import io
import os
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import inventario.persistencia
from inventario.entradas import pedir_cvss, pedir_float, pedir_status_vulnerabilidade
from inventario.enums import NivelDaVulnerabilidade, Setor, StatusDaVuln, StatusDoAtivo
from inventario.excecoes import DadoInvalidoError
from inventario.modelos.ativo import Notebook, Servidor
from inventario.modelos.vulnerabilidade import Vulnerabilidade
from inventario.operacoes.ativos import encontrar_ativo, escolher_ativo_com_vulnerabilidades
from inventario.operacoes.vulnerabilidades import (
    atualizar_status_vulnerabilidade,
    cadastrar_vulnerabilidade,
    confirmar_exclusao_vuln,
    desvincular_vulnerabilidade,
    excluir_vulnerabilidade_do_catalogo,
    encontrar_vulnerabilidade,
    mostrar_vulnerabilidade,
    mostrar_vulnerabilidades_do_ativo,
    proximo_id,
    vincular_vulnerabilidade,
)
from inventario.persistencia import (
    carregar_catalogo,
    carregar_dados,
    salvar_catalogo,
    salvar_dados,
)
from inventario.validacoes import validar_status_vulnerabilidade


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
    with redirect_stdout(buffer):  # guarda o que seria impresso na tela
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
        reconstruida = Vulnerabilidade.de_dicionario(dicionario)  # ida e volta
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


class TestCadastrarVulnerabilidade(unittest.TestCase):

    def test_cria_com_proximo_id(self):
        catalogo = criar_catalogo()
        with patch("builtins.input", side_effect=["SMB desatualizado", "8,1"]):
            with redirect_stdout(io.StringIO()):  # esconde o que a função imprime
                nova = cadastrar_vulnerabilidade(catalogo)
        self.assertEqual(nova.id_vulnerabilidade, 4)
        self.assertEqual(nova.nome_vulnerabilidade, "SMB desatualizado")
        self.assertEqual(nova.cvss, 8.1)

    def test_nao_coloca_no_catalogo_sozinha(self):
        catalogo = criar_catalogo()
        with patch("builtins.input", side_effect=["SMB desatualizado", "8.1"]):
            with redirect_stdout(io.StringIO()):
                cadastrar_vulnerabilidade(catalogo)
        self.assertEqual(len(catalogo), 2)  # quem guarda no catálogo é o menu


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


class TestVincularVulnerabilidade(unittest.TestCase):

    def setUp(self):
        self.catalogo = criar_catalogo()
        self.notebook = criar_notebook()

    def test_vincula_com_status(self):
        vincular_vulnerabilidade(self.notebook, 3, StatusDaVuln.ABERTA, self.catalogo)
        self.assertEqual(self.notebook.vulnerabilidades, {3: StatusDaVuln.ABERTA})

    def test_nao_vincula_duas_vezes(self):
        vincular_vulnerabilidade(self.notebook, 3, StatusDaVuln.ABERTA, self.catalogo)
        with self.assertRaises(DadoInvalidoError):
            vincular_vulnerabilidade(self.notebook, 3, StatusDaVuln.ABERTA, self.catalogo)

    def test_nao_vincula_vulnerabilidade_inexistente(self):
        with self.assertRaises(DadoInvalidoError):
            vincular_vulnerabilidade(self.notebook, 99, StatusDaVuln.ABERTA, self.catalogo)
        self.assertEqual(self.notebook.vulnerabilidades, {})  # nada foi gravado

    def test_mesma_vulnerabilidade_com_status_diferente_em_cada_ativo(self):
        servidor = criar_servidor()
        vincular_vulnerabilidade(self.notebook, 3, StatusDaVuln.ABERTA, self.catalogo)
        vincular_vulnerabilidade(servidor, 3, StatusDaVuln.CORRIGIDA, self.catalogo)
        self.assertEqual(self.notebook.vulnerabilidades[3], StatusDaVuln.ABERTA)
        self.assertEqual(servidor.vulnerabilidades[3], StatusDaVuln.CORRIGIDA)


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
        notebook.vulnerabilidades[1] = StatusDaVuln.ABERTA  # o notebook só tem a 1
        saida = capturar_saida(mostrar_vulnerabilidades_do_ativo, notebook, catalogo)
        self.assertNotIn("TLS 1.0 ativo", saida)


class TestAtualizarStatusVulnerabilidade(unittest.TestCase):

    def setUp(self):
        self.notebook = criar_notebook()
        self.notebook.vulnerabilidades[3] = StatusDaVuln.ABERTA

    def test_atualiza_status_vinculado(self):
        atualizar_status_vulnerabilidade(self.notebook, 3, StatusDaVuln.CORRIGIDA)
        self.assertEqual(self.notebook.vulnerabilidades[3], StatusDaVuln.CORRIGIDA)

    def test_nao_cria_vinculo_novo(self):
        with self.assertRaises(DadoInvalidoError):
            atualizar_status_vulnerabilidade(self.notebook, 1, StatusDaVuln.CORRIGIDA)
        self.assertNotIn(1, self.notebook.vulnerabilidades)  # a 1 não podia ter sido criada


class TestDesvincularVulnerabilidade(unittest.TestCase):

    def setUp(self):
        self.catalogo = criar_catalogo()
        self.notebook = criar_notebook()
        self.notebook.vulnerabilidades[1] = StatusDaVuln.ABERTA
        self.notebook.vulnerabilidades[3] = StatusDaVuln.ABERTA

    def test_remove_so_do_ativo(self):
        desvincular_vulnerabilidade(self.notebook, 3)
        self.assertEqual(self.notebook.vulnerabilidades, {1: StatusDaVuln.ABERTA})
        self.assertIn(3, self.catalogo)  # continua existindo no catálogo

    def test_nao_vinculada_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            desvincular_vulnerabilidade(self.notebook, 99)

    def test_remove_vinculo_orfao(self):
        self.notebook.vulnerabilidades[50] = StatusDaVuln.ABERTA  # aponta para algo que não está no catálogo
        desvincular_vulnerabilidade(self.notebook, 50)
        self.assertNotIn(50, self.notebook.vulnerabilidades)


class TestExcluirVulnerabilidadeDoCatalogo(unittest.TestCase):

    def setUp(self):
        self.catalogo = criar_catalogo()
        self.notebook = criar_notebook()
        self.servidor = criar_servidor()
        self.ativos = {1: self.notebook, 2: self.servidor}

    def test_remove_do_catalogo(self):
        excluir_vulnerabilidade_do_catalogo(self.catalogo, self.ativos, 3)
        self.assertNotIn(3, self.catalogo)
        self.assertIn(1, self.catalogo)  # as outras continuam

    def test_remove_de_todos_os_ativos_vinculados(self):
        self.notebook.vulnerabilidades[3] = StatusDaVuln.ABERTA
        self.servidor.vulnerabilidades[3] = StatusDaVuln.CORRIGIDA  # a mesma em dois ativos
        excluir_vulnerabilidade_do_catalogo(self.catalogo, self.ativos, 3)
        self.assertNotIn(3, self.notebook.vulnerabilidades)
        self.assertNotIn(3, self.servidor.vulnerabilidades)

    def test_mantem_os_outros_vinculos(self):
        self.notebook.vulnerabilidades[1] = StatusDaVuln.ABERTA
        self.notebook.vulnerabilidades[3] = StatusDaVuln.ABERTA
        excluir_vulnerabilidade_do_catalogo(self.catalogo, self.ativos, 3)
        self.assertEqual(self.notebook.vulnerabilidades, {1: StatusDaVuln.ABERTA})

    def test_exclui_mesmo_sem_nenhum_vinculo(self):
        excluir_vulnerabilidade_do_catalogo(self.catalogo, self.ativos, 3)  # ninguém tinha a 3
        self.assertNotIn(3, self.catalogo)

    def test_id_inexistente_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            excluir_vulnerabilidade_do_catalogo(self.catalogo, self.ativos, 99)
        self.assertEqual(len(self.catalogo), 2)  # nada foi apagado


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


# Escolhas feitas pelo usuário -------------------


class TestEncontrarAtivo(unittest.TestCase):

    def setUp(self):
        self.ativos = {1: criar_notebook(), 2: criar_servidor()}

    def test_sem_ativos_retorna_none_sem_perguntar(self):
        with patch("builtins.input") as entrada:
            with redirect_stdout(io.StringIO()):
                self.assertIsNone(encontrar_ativo({}))
        entrada.assert_not_called()  # nem chegou a pedir o ID

    def test_id_existente_retorna_o_ativo(self):
        with patch("builtins.input", return_value="2"):
            with redirect_stdout(io.StringIO()):
                self.assertIs(encontrar_ativo(self.ativos), self.ativos[2])

    def test_id_inexistente_retorna_none(self):
        with patch("builtins.input", return_value="99"):
            with redirect_stdout(io.StringIO()):
                self.assertIsNone(encontrar_ativo(self.ativos))


class TestEscolherAtivoComVulnerabilidades(unittest.TestCase):

    def setUp(self):
        notebook = criar_notebook()
        notebook.vulnerabilidades[1] = StatusDaVuln.ABERTA
        self.ativos = {1: notebook, 2: criar_servidor()}  # o servidor não tem vínculos

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


class TestPersistenciaCatalogo(unittest.TestCase):

    def setUp(self):
        self.originais = (inventario.persistencia.ARQUIVO_DADOS, inventario.persistencia.ARQUIVO_CATALOGO)
        inventario.persistencia.ARQUIVO_DADOS = "teste_ativos_tmp.json"  # não mexe nos arquivos reais
        inventario.persistencia.ARQUIVO_CATALOGO = "teste_catalogo_tmp.json"

    def tearDown(self):
        for arquivo in (inventario.persistencia.ARQUIVO_DADOS, inventario.persistencia.ARQUIVO_CATALOGO):
            if os.path.exists(arquivo):
                os.remove(arquivo)
        inventario.persistencia.ARQUIVO_DADOS, inventario.persistencia.ARQUIVO_CATALOGO = self.originais

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