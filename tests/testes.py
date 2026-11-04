import os
import unittest
from inventario.dominio.enums import (
    Cor,
    Setor,
    StatusDoAtivo,
    Tecnologia,
)
from inventario.entradas import (
    pedir_cor,
    pedir_float,
    pedir_info,
    pedir_int,
    pedir_setor,
    pedir_status,
    pedir_tecnologia,
    pedir_tipo,
)
from inventario.dominio.excecoes import DadoInvalidoError
from inventario.dominio.ativo import Impressora, Notebook, Roteador, Servidor
from inventario.persistencia import carregar_dados, salvar_dados
from inventario.operacoes.ativos import (
    cadastrar_ativo,
    cadastro_impressora,
    cadastro_notebook,
    cadastro_roteador,
    cadastro_servidor,
    confirmar_exclusao,
    encontrar_ativo_por_id,
    encontrar_ativo_por_nome,
    encontrar_ativos_por_status,
    listar_ativos_por_tipo,
    obter_ativo,
    pedir_id_disponivel,
    registrar_ativo,
)
from inventario.validacoes import (
    validar_cor,
    validar_nome_responsavel,
    validar_setor,
    validar_status,
    validar_tecnologia,
    validar_tipo,
)
from tests.apoio import TesteComArquivosTemporarios
from unittest.mock import patch


# Exibir detalhes
class TestExibirDetalhes(unittest.TestCase):

    def test_notebook_mostra_tipo(self):
        n = Notebook(1, "Dell", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, "Linux", 15.6)
        detalhes = n.exibir_detalhes()
        self.assertIn("Tipo: Notebook", detalhes)

    def test_notebook_mostra_campos_especificos(self):
        n = Notebook(1, "Dell", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, "Linux", 15.6)
        detalhes = n.exibir_detalhes()
        self.assertIn("Sistema operacional: Linux", detalhes)
        self.assertIn("Tamanho da tela: 15.6 polegadas", detalhes)

    def test_servidor_mostra_tipo(self):
        s = Servidor(2, "Dell PowerEdge", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, 32, 4)
        detalhes = s.exibir_detalhes()
        self.assertIn("Tipo: Servidor", detalhes)

    def test_servidor_mostra_campos_especificos(self):
        s = Servidor(2, "Dell PowerEdge", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, 32, 4)
        detalhes = s.exibir_detalhes()
        self.assertIn("Memória RAM: 32GB", detalhes)
        self.assertIn("Qtde armazenamento: 4T", detalhes)

    def test_roteador_mostra_tipo(self):
        r = Roteador(3, "TP-Link", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, 4, 1000)
        detalhes = r.exibir_detalhes()
        self.assertIn("Tipo: Roteador", detalhes)

    def test_roteador_mostra_campos_especificos(self):
        r = Roteador(3, "TP-Link", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, 4, 1000)
        detalhes = r.exibir_detalhes()
        self.assertIn("Qtde de portas: 4", detalhes)
        self.assertIn("Velocidade: 1000MB", detalhes)

    def test_impressora_mostra_tipo(self):
        i = Impressora(4, "HP", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, Cor.COLORIDA, Tecnologia.LASER)
        detalhes = i.exibir_detalhes()
        self.assertIn("Tipo: Impressora", detalhes)

    def test_impressora_mostra_campos_especificos(self):
        i = Impressora(4, "HP", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, Cor.COLORIDA, Tecnologia.LASER)
        detalhes = i.exibir_detalhes()
        self.assertIn("Cor: COLORIDA", detalhes)
        self.assertIn("Tecnologia: LASER", detalhes)

    def test_todos_mostram_campos_comuns(self):
        n = Notebook(1, "Dell", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, "Linux", 15.6)
        detalhes = n.exibir_detalhes()
        self.assertIn("ID: 1", detalhes)
        self.assertIn("Nome: Dell", detalhes)
        self.assertIn("Setor: TI", detalhes)
        self.assertIn("Responsável: Cadu", detalhes)
        self.assertIn("Status: ATIVO", detalhes)


# Validações -------------------------------------


class TestValidarSetor(unittest.TestCase):

    def test_setor_1_retorna_ti(self):
        self.assertEqual(validar_setor("1"), Setor.TI)

    def test_setor_5_retorna_juridico(self):
        self.assertEqual(validar_setor("5"), Setor.JURIDICO)

    def test_setor_invalido_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            validar_setor("6")


class TestValidarStatus(unittest.TestCase):

    def test_status_1_retorna_ativo(self):
        self.assertEqual(validar_status("1"), StatusDoAtivo.ATIVO)

    def test_status_3_retorna_manutencao(self):
        self.assertEqual(validar_status("3"), StatusDoAtivo.EM_MANUTENCAO)

    def test_status_4_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            validar_status("4")


class TestValidarTipo(unittest.TestCase):

    def test_tipo_1_retorna_notebook(self):
        self.assertEqual(validar_tipo("1"), Notebook)

    def test_tipo_4_retorna_impressora(self):
        self.assertEqual(validar_tipo("4"), Impressora)

    def test_tipo_5_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            validar_tipo("5")


class TestValidarCor(unittest.TestCase):

    def test_cor_1_retorna_colorido(self):
        self.assertEqual(validar_cor("1"), Cor.COLORIDA)

    def test_cor_3_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            validar_cor("3")


class TestValidarTech(unittest.TestCase):

    def test_tech_1_retorna_tinta(self):
        self.assertEqual(validar_tecnologia("1"), Tecnologia.TINTA)

    def test_tech_2_retorna_laser(self):
        self.assertEqual(validar_tecnologia("2"), Tecnologia.LASER)

    def test_tech_3_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            validar_tecnologia("3")


class TestValidarNomeResponsavel(unittest.TestCase):

    def test_nome_valido_nao_levanta_erro(self):
        validar_nome_responsavel("Cadu")

    def test_nome_numerico_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            validar_nome_responsavel("123")

    def test_nome_vazio_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            validar_nome_responsavel("")


# Funções encontrar ativo ------------------------


class TestEncontrarAtivoPorId(unittest.TestCase):

    def setUp(self):
        self.ativos = {
            1: Notebook(1, "Dell", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, "Linux", 15.6),
            2: Servidor(2, "Dell PowerEdge", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, 32, 4),
            3: Roteador(3, "TP-Link", Setor.MARKETING, "Ana", StatusDoAtivo.INATIVO, 4, 1000),
            4: Impressora(4, "HP", Setor.RH, "Bia", StatusDoAtivo.ATIVO, Cor.COLORIDA, Tecnologia.LASER),
            5: Notebook(5, "Dellinho", Setor.FINANCEIRO, "Henrique", StatusDoAtivo.EM_MANUTENCAO, "Windows XP", 32),
        }

    def test_encontra_ativo_existente(self):
        ativo = encontrar_ativo_por_id(1, self.ativos)
        self.assertIsNotNone(ativo)
        self.assertEqual(ativo.nome, "Dell")

    def test_retorna_none_quando_id_nao_existe(self):
        ativo = encontrar_ativo_por_id(99, self.ativos)
        self.assertIsNone(ativo)


class TestObterAtivo(unittest.TestCase):

    def setUp(self):
        self.notebook = Notebook(1, "Dell", Setor.TI, "Rafael Torres", StatusDoAtivo.ATIVO, "Linux", 15.6)
        self.ativos = {1: self.notebook}

    def test_devolve_ativo_existente(self):
        self.assertIs(obter_ativo(self.ativos, 1), self.notebook)

    def test_id_inexistente_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):  # diferente do encontrar, que devolve None
            obter_ativo(self.ativos, 99)


class TestEncontrarAtivosPorNome(unittest.TestCase):

    def setUp(self):
        self.ativos = {
            1: Notebook(1, "Dell", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, "Linux", 15.6),
            2: Servidor(2, "Dell PowerEdge", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, 32, 4),
            3: Roteador(3, "TP-Link", Setor.MARKETING, "Ana", StatusDoAtivo.INATIVO, 4, 1000),
        }

    def test_busca_nome_exato(self):
        encontrados = encontrar_ativo_por_nome("Dell", self.ativos)
        self.assertEqual(len(encontrados), 2)

    def test_busca_parcial_case_insensitive(self):
        encontrados = encontrar_ativo_por_nome("dell", self.ativos)
        self.assertEqual(len(encontrados), 2)

    def test_busca_sem_resultado(self):
        encontrados = encontrar_ativo_por_nome("Xyz", self.ativos)
        self.assertEqual(len(encontrados), 0)


class TestEncontrarAtivosPorStatus(unittest.TestCase):

    def setUp(self):
        self.ativos = {
            1: Notebook(1, "Dell", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, "Linux", 15.6),
            2: Servidor(2, "Dell PowerEdge", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, 32, 4),
            3: Roteador(3, "TP-Link", Setor.MARKETING, "Ana", StatusDoAtivo.INATIVO, 4, 1000),
        }

    def test_status_ativo_retorna_2(self):
        encontrados = encontrar_ativos_por_status(StatusDoAtivo.ATIVO, self.ativos)
        self.assertEqual(len(encontrados), 2)

    def test_status_inativo_retorna_1(self):
        encontrados = encontrar_ativos_por_status(StatusDoAtivo.INATIVO, self.ativos)
        self.assertEqual(len(encontrados), 1)


class TestListarAtivosPorTipo(unittest.TestCase):

    def setUp(self):
        self.ativos = {
            1: Notebook(1, "Dell", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, "Linux", 15.6),
            2: Servidor(2, "Dell PowerEdge", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, 32, 4),
            3: Roteador(3, "TP-Link", Setor.MARKETING, "Ana", StatusDoAtivo.INATIVO, 4, 1000),
        }

    def test_listar_notebooks_retorna_um(self):
        encontrados = listar_ativos_por_tipo(Notebook, self.ativos)
        self.assertEqual(len(encontrados), 1)

    def test_listar_impressora_retorna_vazio(self):
        encontrados = listar_ativos_por_tipo(Impressora, self.ativos)
        self.assertEqual(len(encontrados), 0)


# Serialização -----------------------------------


class TestSerializacaoNotebook(unittest.TestCase):

    def setUp(self):
        self.notebook = Notebook(1, "Dell", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, "Linux", 15.6)

    def test_para_dicionario_contem_chaves(self):
        dicionario = self.notebook.para_dicionario()
        self.assertIn("id", dicionario)
        self.assertIn("tipo", dicionario)
        self.assertIn("sistema_operacional", dicionario)

    def test_tipo_esta_correto(self):
        dicionario = self.notebook.para_dicionario()
        self.assertEqual(dicionario["tipo"], "Notebook")

    def test_de_dicionario_reconstroi(self):
        dicionario = self.notebook.para_dicionario()
        reconstruido = Notebook.de_dicionario(dicionario)
        self.assertEqual(reconstruido.id, self.notebook.id)
        self.assertEqual(reconstruido.nome, self.notebook.nome)


class TestSerializacaoServidor(unittest.TestCase):

    def setUp(self):
        self.servidor = Servidor(2, "Dell PowerEdge", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, 32, 4)

    def test_tipo_esta_correto(self):
        dicionario = self.servidor.para_dicionario()
        self.assertEqual(dicionario["tipo"], "Servidor")

    def test_de_dicionario_reconstroi(self):
        dicionario = self.servidor.para_dicionario()
        reconstruido = Servidor.de_dicionario(dicionario)
        self.assertEqual(reconstruido.ram, self.servidor.ram)


class TestSerializacaoRoteador(unittest.TestCase):

    def setUp(self):
        self.roteador = Roteador(3, "TP-Link", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, 4, 1000)

    def test_tipo_esta_correto(self):
        dicionario = self.roteador.para_dicionario()
        self.assertEqual(dicionario["tipo"], "Roteador")

    def test_de_dicionario_reconstroi(self):
        dicionario = self.roteador.para_dicionario()
        reconstruido = Roteador.de_dicionario(dicionario)
        self.assertEqual(reconstruido.portas, self.roteador.portas)


class TestSerializacaoImpressora(unittest.TestCase):

    def setUp(self):
        self.impressora = Impressora(4, "HP", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, Cor.COLORIDA, Tecnologia.LASER)

    def test_tipo_esta_correto(self):
        dicionario = self.impressora.para_dicionario()
        self.assertEqual(dicionario["tipo"], "Impressora")

    def test_de_dicionario_reconstroi(self):
        dicionario = self.impressora.para_dicionario()
        reconstruido = Impressora.de_dicionario(dicionario)
        self.assertEqual(reconstruido.cor, self.impressora.cor)


# Persistência de dados --------------------------


class TestPersistencia(TesteComArquivosTemporarios):

    def test_salvar_cria_arquivo(self):
        ativos = {1: Notebook(1, "Dell", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, "Linux", 15.6)}
        salvar_dados(ativos)
        self.assertTrue(os.path.exists(self.arquivo_dados))

    def test_carregar_devolve_o_que_foi_salvo(self):
        ativos = {1: Notebook(1, "Dell", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, "Linux", 15.6)}
        salvar_dados(ativos)
        carregados = carregar_dados()
        self.assertEqual(len(carregados), 1)
        self.assertEqual(carregados[1].nome, "Dell")

    def test_carregar_arquivo_inexistente_retorna_vazio(self):
        self.assertEqual(carregar_dados(), {})  # o setUp já começa sem arquivo


# Testes de Input --------------------------------


class TestPedirInt(unittest.TestCase):

    def test_retorna_inteiro_valido(self):
        with patch("builtins.input", return_value="42"):
            self.assertEqual(pedir_int("Digite: "), 42)

    def test_aceita_zero_ou_negativo(self):
        with patch("builtins.input", side_effect=["0", "5"]):
            self.assertEqual(pedir_int("Digite: "), 5)

    def test_aceita_texto_depois_numero(self):
        with patch("builtins.input", side_effect=["abc", "7"]):
            self.assertEqual(pedir_int("Digite: "), 7)


class TestPedirFloat(unittest.TestCase):

    def test_retorna_float_valido(self):
        with patch("builtins.input", return_value="3.14"):
            self.assertEqual(pedir_float("Digite: "), 3.14)

    def test_rejeita_zero_e_aceita_depois(self):
        with patch("builtins.input", side_effect=["0", "2.5"]):
            self.assertEqual(pedir_float("Digite: "), 2.5)


class TestPedirInfo(unittest.TestCase):

    def test_retorna_string_valida(self):
        with patch("builtins.input", return_value="Cadu"):
            self.assertEqual(pedir_info("Digite: "), "Cadu")

    def test_rejeita_vazio_e_aceita_depois(self):
        with patch("builtins.input", side_effect=["", "Cadu"]):
            self.assertEqual(pedir_info("Digite: "), "Cadu")


class TestPedirStatus(unittest.TestCase):

    def test_retorna_ativo_quando_digita_1(self):
        with patch("builtins.input", return_value="1"):
            self.assertEqual(pedir_status("Digite: "), StatusDoAtivo.ATIVO)

    def test_aceita_erro_e_depois_valido(self):
        with patch("builtins.input", side_effect=["9", "1"]):
            self.assertEqual(pedir_status("Digite: "), StatusDoAtivo.ATIVO)


class TestPedirSetor(unittest.TestCase):

    def test_retorna_ti_digita_1(self):
        with patch("builtins.input", return_value="1"):
            self.assertEqual(pedir_setor("Digite: "), Setor.TI)

    def test_aceita_erro_e_retorna_ti(self):
        with patch("builtins.input", side_effect=["9", "1"]):
            self.assertEqual(pedir_setor("Digite: "), Setor.TI)


class TestPedirCor(unittest.TestCase):

    def test_retorna_colorido_digita_1(self):
        with patch("builtins.input", return_value="1"):
            self.assertEqual(pedir_cor(), Cor.COLORIDA)

    def test_retorna_peb_digita_2(self):
        with patch("builtins.input", return_value="2"):
            self.assertEqual(pedir_cor(), Cor.PRETA_E_BRANCA)


class TestPedirTech(unittest.TestCase):

    def test_retorna_tinta_digita_1(self):
        with patch("builtins.input", return_value="1"):
            self.assertEqual(pedir_tecnologia(), Tecnologia.TINTA)

    def test_retorna_laser_digita_2(self):
        with patch("builtins.input", return_value="2"):
            self.assertEqual(pedir_tecnologia(), Tecnologia.LASER)


class TestPedirTipo(unittest.TestCase):

    def test_retorna_notebook_digita_1(self):
        with patch("builtins.input", return_value="1"):
            self.assertEqual(pedir_tipo("Digite: "), Notebook)

    def test_retorna_impressora_digita_4(self):
        with patch("builtins.input", return_value="4"):
            self.assertEqual(pedir_tipo("Digite: "), Impressora)


class TestPedirIdDisponivel(unittest.TestCase):

    def test_retorna_id_se_disponivel(self):
        with patch("builtins.input", return_value="10"):
            self.assertEqual(pedir_id_disponivel({}), 10)

    def test_rejeita_id_existente_e_pede_de_novo(self):
        ativos = {1: Notebook(1, "Dell", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, "Linux", 15.6)}
        with patch("builtins.input", side_effect=["1", "2"]):
            self.assertEqual(pedir_id_disponivel(ativos), 2)


# Cadastros específicos --------------------------


class TestCadastroNotebook(unittest.TestCase):

    def test_retorna_so_e_tela(self):
        with patch("builtins.input", side_effect=["Linux", "15.6"]):
            so, tela = cadastro_notebook()
        self.assertEqual(so, "Linux")
        self.assertEqual(tela, 15.6)


class TestCadastroServidor(unittest.TestCase):

    def test_retorna_ram_e_armazenamento(self):
        with patch("builtins.input", side_effect=["32", "4"]):
            ram, armazenamento = cadastro_servidor()
        self.assertEqual(ram, 32)
        self.assertEqual(armazenamento, 4.0)


class TestCadastroRoteador(unittest.TestCase):

    def test_retorna_portas_e_velocidade(self):
        with patch("builtins.input", side_effect=["4", "1000"]):
            portas, velocidade = cadastro_roteador()
        self.assertEqual(portas, 4)
        self.assertEqual(velocidade, 1000)


class TestCadastroImpressora(unittest.TestCase):

    def test_retorna_cor_e_tecnologia(self):
        with patch("builtins.input", side_effect=["1", "2"]):
            cor, tecnologia = cadastro_impressora()
        self.assertEqual(cor, Cor.COLORIDA)
        self.assertEqual(tecnologia, Tecnologia.LASER)


# Cadastrar Ativo --------------------------------


class TestCadastrarAtivo(TesteComArquivosTemporarios):

    def test_guarda_no_inventario(self):
        ativos = {}
        respostas = ["1", "5", "Dell", "1", "Cadu", "1", "Linux", "15.6"]
        with patch("builtins.input", side_effect=respostas):
            ativo = cadastrar_ativo(ativos)
        self.assertIs(ativos[5], ativo)  # agora quem guarda é a própria função
        self.assertIn(5, carregar_dados())  # e já salvou no arquivo

    def test_registrar_id_repetido_levanta_erro(self):
        ativo = Notebook(1, "Dell", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, "Linux", 15.6)
        ativos = {1: ativo}
        with self.assertRaises(DadoInvalidoError):
            registrar_ativo(ativos, ativo)

    def test_cadastra_notebook(self):
        # Ordem: tipo, id, nome, setor, responsável, status, so, tela
        respostas = ["1", "5", "Dell", "1", "Cadu", "1", "Linux", "15.6"]
        with patch("builtins.input", side_effect=respostas):
            ativo = cadastrar_ativo({})
        self.assertIsInstance(ativo, Notebook)
        self.assertEqual(ativo.id, 5)
        self.assertEqual(ativo.nome, "Dell")
        self.assertEqual(ativo.sistema_operacional, "Linux")
        self.assertEqual(ativo.tela, 15.6)

    def test_cadastra_servidor(self):
        respostas = ["2", "6", "PowerEdge", "1", "Cadu", "1", "32", "4"]
        with patch("builtins.input", side_effect=respostas):
            ativo = cadastrar_ativo({})
        self.assertIsInstance(ativo, Servidor)
        self.assertEqual(ativo.ram, 32)

    def test_cadastra_roteador(self):
        respostas = ["3", "7", "TP-Link", "1", "Cadu", "1", "4", "1000"]
        with patch("builtins.input", side_effect=respostas):
            ativo = cadastrar_ativo({})
        self.assertIsInstance(ativo, Roteador)
        self.assertEqual(ativo.portas, 4)

    def test_cadastra_impressora(self):
        respostas = ["4", "8", "HP", "1", "Cadu", "1", "1", "2"]
        with patch("builtins.input", side_effect=respostas):
            ativo = cadastrar_ativo({})
        self.assertIsInstance(ativo, Impressora)
        self.assertEqual(ativo.cor, Cor.COLORIDA)


# Confirmar Exclusão -----------------------------


class TestConfirmarExclusao(unittest.TestCase):

    def setUp(self):
        self.ativo = Notebook(1, "Dell", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, "Linux", 15.6)

    def test_retorna_true_com_sim(self):
        with patch("builtins.input", return_value="sim"):
            self.assertTrue(confirmar_exclusao(self.ativo))

    def test_retorna_false_com_enter(self):
        with patch("builtins.input", return_value=""):
            self.assertFalse(confirmar_exclusao(self.ativo))

    def test_retorna_false_com_nao(self):
        with patch("builtins.input", return_value="nao"):
            self.assertFalse(confirmar_exclusao(self.ativo))


if __name__ == "__main__":
    unittest.main()