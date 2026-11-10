import io
from contextlib import redirect_stdout
from unittest.mock import patch

from inventario.dominio.ativo import Notebook, Roteador, Servidor
from inventario.dominio.enums import Setor, StatusDoAtivo
from inventario.dominio.excecoes import DadoInvalidoError
from inventario.interface.menu import menu_dependencias
from inventario.persistencia.arquivos_json import carregar_ativos, salvar_ativos
from inventario.servicos.ativos import (
    atualizar_ativo_no_inventario,
    remover_ativo_do_inventario,
)
from inventario.servicos.dependencias import (
    atualizar_dependencia,
    cadastrar_dependencia,
    remover_dependencia,
)
from tests.apoio import TesteComArquivosTemporarios


def criar_notebook():
    return Notebook(1, "Dell", Setor.TI, "Rafael Torres", StatusDoAtivo.ATIVO, "Linux", 15.6)


def criar_servidor():
    return Servidor(2, "PowerEdge", Setor.TI, "Rafael Torres", StatusDoAtivo.ATIVO, 32, 4)


def criar_roteador():
    return Roteador(3, "Cisco", Setor.TI, "Rafael Torres", StatusDoAtivo.ATIVO, 24, 1000)


class TesteComTresAtivos(TesteComArquivosTemporarios):

    def setUp(self):
        super().setUp()
        self.notebook = criar_notebook()
        self.servidor = criar_servidor()
        self.roteador = criar_roteador()
        self.ativos = {1: self.notebook, 2: self.servidor, 3: self.roteador}
        salvar_ativos(self.ativos)


class TestCadastrarDependencia(TesteComTresAtivos):

    def test_cadastro_valido_grava_na_memoria(self):
        cadastrar_dependencia(self.repositorio, self.ativos, 1, 2, 0.5)
        self.assertEqual(self.notebook.dependencias, {2: 0.5})

    def test_cadastro_valido_salva_no_arquivo(self):
        cadastrar_dependencia(self.repositorio, self.ativos, 1, 2, 0.5)
        self.assertEqual(carregar_ativos()[1].dependencias, {2: 0.5})

    def test_ativo_que_depende_inexistente_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            cadastrar_dependencia(self.repositorio, self.ativos, 99, 2, 0.5)

    def test_ativo_do_qual_depende_inexistente_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            cadastrar_dependencia(self.repositorio, self.ativos, 1, 99, 0.5)
        self.assertEqual(self.notebook.dependencias, {})

    def test_ativo_nao_pode_depender_dele_proprio(self):
        with self.assertRaises(DadoInvalidoError):
            cadastrar_dependencia(self.repositorio, self.ativos, 1, 1, 0.5)
        self.assertEqual(self.notebook.dependencias, {})

    def test_nao_cadastra_a_mesma_dependencia_duas_vezes(self):
        cadastrar_dependencia(self.repositorio, self.ativos, 1, 2, 0.5)
        with self.assertRaises(DadoInvalidoError):
            cadastrar_dependencia(self.repositorio, self.ativos, 1, 2, 0.2)
        self.assertEqual(self.notebook.dependencias, {2: 0.5})

    def test_soma_que_passaria_de_1_levanta_erro(self):
        cadastrar_dependencia(self.repositorio, self.ativos, 1, 2, 0.6)
        with self.assertRaises(DadoInvalidoError):
            cadastrar_dependencia(self.repositorio, self.ativos, 1, 3, 0.5)
        self.assertEqual(self.notebook.dependencias, {2: 0.6})

    def test_soma_0_1_mais_0_2_mais_0_7_e_recusada(self):
        roteador_extra = Roteador(
            4, "TP-Link", Setor.TI, "Rafael Torres", StatusDoAtivo.ATIVO, 8, 100
        )
        self.ativos[4] = roteador_extra
        salvar_ativos(self.ativos)

        cadastrar_dependencia(self.repositorio, self.ativos, 1, 2, 0.1)
        cadastrar_dependencia(self.repositorio, self.ativos, 1, 3, 0.2)
        with self.assertRaises(DadoInvalidoError):
            cadastrar_dependencia(self.repositorio, self.ativos, 1, 4, 0.7)
        self.assertEqual(self.notebook.dependencias, {2: 0.1, 3: 0.2})

    def test_fracao_zero_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            cadastrar_dependencia(self.repositorio, self.ativos, 1, 2, 0)
        self.assertEqual(self.notebook.dependencias, {})

    def test_fracao_negativa_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            cadastrar_dependencia(self.repositorio, self.ativos, 1, 2, -0.3)
        self.assertEqual(self.notebook.dependencias, {})


class TestRemoverDependencia(TesteComTresAtivos):

    def test_remove_da_memoria_e_do_arquivo(self):
        cadastrar_dependencia(self.repositorio, self.ativos, 1, 2, 0.5)

        remover_dependencia(self.repositorio, self.ativos, 1, 2)

        self.assertEqual(self.notebook.dependencias, {})
        self.assertEqual(carregar_ativos()[1].dependencias, {})

    def test_remover_dependencia_inexistente_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            remover_dependencia(self.repositorio, self.ativos, 1, 2)


class TestAtualizarDependencia(TesteComTresAtivos):

    def setUp(self):
        super().setUp()
        cadastrar_dependencia(self.repositorio, self.ativos, 1, 2, 0.5)

    def test_troca_so_a_fracao(self):
        atualizar_dependencia(self.repositorio, self.ativos, 1, 2, 2, 0.3)
        self.assertEqual(self.notebook.dependencias, {2: 0.3})

    def test_troca_so_o_ativo_mantendo_a_fracao(self):
        atualizar_dependencia(self.repositorio, self.ativos, 1, 2, 3, 0.5)
        self.assertEqual(self.notebook.dependencias, {3: 0.5})

    def test_troca_o_ativo_e_a_fracao(self):
        atualizar_dependencia(self.repositorio, self.ativos, 1, 2, 3, 0.25)
        self.assertEqual(self.notebook.dependencias, {3: 0.25})

    def test_mudanca_fica_salva_no_arquivo(self):
        atualizar_dependencia(self.repositorio, self.ativos, 1, 2, 3, 0.25)
        self.assertEqual(carregar_ativos()[1].dependencias, {3: 0.25})

    def test_ativo_nao_pode_passar_a_depender_dele_proprio(self):
        with self.assertRaises(DadoInvalidoError):
            atualizar_dependencia(self.repositorio, self.ativos, 1, 2, 1, 0.5)
        self.assertEqual(self.notebook.dependencias, {2: 0.5})

    def test_dependencia_antiga_inexistente_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            atualizar_dependencia(self.repositorio, self.ativos, 1, 3, 2, 0.5)
        self.assertEqual(self.notebook.dependencias, {2: 0.5})

    def test_novo_ativo_que_ja_e_dependencia_levanta_erro(self):
        cadastrar_dependencia(self.repositorio, self.ativos, 1, 3, 0.2)
        with self.assertRaises(DadoInvalidoError):
            atualizar_dependencia(self.repositorio, self.ativos, 1, 2, 3, 0.1)
        self.assertEqual(self.notebook.dependencias, {2: 0.5, 3: 0.2})

    def test_soma_que_passaria_de_1_levanta_erro(self):
        cadastrar_dependencia(self.repositorio, self.ativos, 1, 3, 0.4)
        with self.assertRaises(DadoInvalidoError):
            atualizar_dependencia(self.repositorio, self.ativos, 1, 2, 2, 0.6)
        self.assertEqual(self.notebook.dependencias, {2: 0.5, 3: 0.4})

    def test_soma_desconta_a_fracao_antiga(self):
        cadastrar_dependencia(self.repositorio, self.ativos, 1, 3, 0.4)
        atualizar_dependencia(self.repositorio, self.ativos, 1, 2, 2, 0.55)
        self.assertEqual(self.notebook.dependencias, {2: 0.55, 3: 0.4})

    def test_fracao_zero_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            atualizar_dependencia(self.repositorio, self.ativos, 1, 2, 2, 0)
        self.assertEqual(self.notebook.dependencias, {2: 0.5})

    def test_fracao_negativa_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            atualizar_dependencia(self.repositorio, self.ativos, 1, 2, 2, -0.3)
        self.assertEqual(self.notebook.dependencias, {2: 0.5})


class TestRemoverAtivoComDependencias(TesteComTresAtivos):

    def test_tira_da_memoria_as_dependencias_que_apontavam_para_o_ativo(self):
        cadastrar_dependencia(self.repositorio, self.ativos, 1, 2, 0.5)
        cadastrar_dependencia(self.repositorio, self.ativos, 3, 2, 0.4)
        cadastrar_dependencia(self.repositorio, self.ativos, 3, 1, 0.3)

        remover_ativo_do_inventario(self.repositorio, self.ativos, 2)

        self.assertEqual(self.notebook.dependencias, {})
        self.assertEqual(self.roteador.dependencias, {1: 0.3})


class TestTrocarTipoDoAtivoComDependencias(TesteComTresAtivos):

    def test_trocar_o_tipo_preserva_as_dependencias(self):
        cadastrar_dependencia(self.repositorio, self.ativos, 1, 2, 0.5)
        notebook_que_virou_servidor = Servidor(
            1, "Dell", Setor.TI, "Rafael Torres", StatusDoAtivo.ATIVO, 16, 2
        )

        atualizar_ativo_no_inventario(self.repositorio, self.ativos, notebook_que_virou_servidor)

        self.assertIsInstance(self.ativos[1], Servidor)
        self.assertEqual(self.ativos[1].dependencias, {2: 0.5})


class TesteDoMenuDeDependencias(TesteComTresAtivos):

    def usar_menu(self, respostas_digitadas):
        saida = io.StringIO()
        with patch("builtins.input", side_effect=respostas_digitadas):
            with redirect_stdout(saida):
                menu_dependencias(self.repositorio, self.ativos)
        return saida.getvalue()


class TestMenuAtualizarDependencia(TesteDoMenuDeDependencias):

    def setUp(self):
        super().setUp()
        cadastrar_dependencia(self.repositorio, self.ativos, 1, 2, 0.5)

    def test_enter_nos_dois_campos_mantem_a_dependencia(self):
        saida = self.usar_menu(["2", "1", "2", "", "", "5"])

        self.assertIn("Dependência atualizada com sucesso.", saida)
        self.assertEqual(self.notebook.dependencias, {2: 0.5})

    def test_troca_o_ativo_e_aceita_fracao_com_virgula(self):
        saida = self.usar_menu(["2", "1", "2", "3", "0,3", "5"])

        self.assertIn("Dependência atualizada com sucesso.", saida)
        self.assertEqual(self.notebook.dependencias, {3: 0.3})
        self.assertEqual(carregar_ativos()[1].dependencias, {3: 0.3})

    def test_id_novo_que_nao_e_numero_mostra_erro(self):
        saida = self.usar_menu(["2", "1", "2", "abc", "5"])

        self.assertIn("Digite um número válido.", saida)
        self.assertEqual(self.notebook.dependencias, {2: 0.5})

    def test_fracao_que_nao_e_numero_mostra_erro(self):
        saida = self.usar_menu(["2", "1", "2", "", "abc", "5"])

        self.assertIn("Digite um número válido.", saida)
        self.assertEqual(self.notebook.dependencias, {2: 0.5})

    def test_fracao_zero_mostra_erro(self):
        saida = self.usar_menu(["2", "1", "2", "", "0", "5"])

        self.assertIn("A fração precisa ser maior que zero.", saida)
        self.assertEqual(self.notebook.dependencias, {2: 0.5})

    def test_ativo_sem_dependencias_avisa(self):
        saida = self.usar_menu(["2", "3", "5"])

        self.assertIn("Este ativo não possui dependências cadastradas.", saida)


class TestMenuRemoverDependencia(TesteDoMenuDeDependencias):

    def test_remove_a_dependencia_escolhida(self):
        cadastrar_dependencia(self.repositorio, self.ativos, 1, 2, 0.5)

        saida = self.usar_menu(["3", "1", "2", "5"])

        self.assertIn("Dependência removida com sucesso.", saida)
        self.assertEqual(self.notebook.dependencias, {})

    def test_remocao_fica_salva_no_arquivo(self):
        cadastrar_dependencia(self.repositorio, self.ativos, 1, 2, 0.5)

        self.usar_menu(["3", "1", "2", "5"])

        self.assertEqual(carregar_ativos()[1].dependencias, {})

    def test_remove_so_a_dependencia_escolhida(self):
        cadastrar_dependencia(self.repositorio, self.ativos, 1, 2, 0.5)
        cadastrar_dependencia(self.repositorio, self.ativos, 1, 3, 0.2)

        self.usar_menu(["3", "1", "2", "5"])

        self.assertEqual(self.notebook.dependencias, {3: 0.2})

    def test_ativo_sem_dependencias_avisa_e_volta_ao_menu(self):
        saida = self.usar_menu(["3", "1", "5"])

        self.assertIn("Este ativo não possui dependências cadastradas.", saida)

    def test_dependencia_que_nao_existe_mostra_erro(self):
        cadastrar_dependencia(self.repositorio, self.ativos, 1, 2, 0.5)

        saida = self.usar_menu(["3", "1", "3", "5"])

        self.assertIn("Este ativo não possui essa dependência.", saida)
        self.assertEqual(self.notebook.dependencias, {2: 0.5})

    def test_ativo_que_nao_existe_mostra_erro(self):
        saida = self.usar_menu(["3", "99", "5"])

        self.assertIn("Ativo não encontrado.", saida)


class TestMenuListarDependencias(TesteDoMenuDeDependencias):

    def test_todos_lista_os_ativos_em_ordem_de_nome(self):
        saida = self.usar_menu(["4", "todos", "5"])

        posicao_cisco = saida.index("3 - Cisco (Roteador)")
        posicao_dell = saida.index("1 - Dell (Notebook)")
        posicao_poweredge = saida.index("2 - PowerEdge (Servidor)")

        self.assertLess(posicao_cisco, posicao_dell)
        self.assertLess(posicao_dell, posicao_poweredge)

    def test_todos_mostra_as_dependencias_de_cada_ativo(self):
        cadastrar_dependencia(self.repositorio, self.ativos, 1, 2, 0.5)
        cadastrar_dependencia(self.repositorio, self.ativos, 3, 1, 0.3)

        saida = self.usar_menu(["4", "todos", "5"])

        self.assertIn("Fração herdada: 0.5", saida)
        self.assertIn("Fração herdada: 0.3", saida)

    def test_um_mostra_as_dependencias_do_ativo_escolhido(self):
        cadastrar_dependencia(self.repositorio, self.ativos, 1, 2, 0.5)

        saida = self.usar_menu(["4", "um", "1", "5"])

        self.assertIn("Ativo: PowerEdge", saida)
        self.assertIn("Fração herdada: 0.5", saida)

    def test_um_nao_mostra_dependencias_de_outro_ativo(self):
        cadastrar_dependencia(self.repositorio, self.ativos, 1, 2, 0.5)

        saida = self.usar_menu(["4", "um", "3", "5"])

        self.assertIn("Este ativo não depende de nenhum outro ativo.", saida)
        self.assertNotIn("Fração herdada: 0.5", saida)

    def test_um_com_ativo_que_nao_existe_mostra_erro(self):
        saida = self.usar_menu(["4", "um", "99", "5"])

        self.assertIn("Ativo não encontrado.", saida)

    def test_resposta_invalida_pergunta_de_novo(self):
        saida = self.usar_menu(["4", "talvez", "todos", "5"])

        self.assertIn('Opção inválida. Digite "todos" ou "um".', saida)
        self.assertIn("Listando as dependências de todos os ativos...", saida)
