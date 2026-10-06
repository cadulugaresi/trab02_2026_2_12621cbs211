import os
import io
import unittest
import funcoes_t2
from funcoes_t2 import *
from unittest.mock import patch
from contextlib import redirect_stdout


# Exibir detalhes
class TestExibirDetalhes(unittest.TestCase):

    # Notebook
    def test_notebook_mostra_tipo(self):
        n = Notebook(1, "Dell", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, "Linux", 15.6)
        detalhes = n.exibir_detalhes()
        self.assertIn("Tipo: Notebook", detalhes)

    def test_notebook_mostra_campos_especificos(self):
        n = Notebook(1, "Dell", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, "Linux", 15.6)
        detalhes = n.exibir_detalhes()
        self.assertIn("Sistema operacional: Linux", detalhes)
        self.assertIn("Tamanho da tela: 15.6 polegadas", detalhes)

    # Servidor
    def test_servidor_mostra_tipo(self):
        s = Servidor(2, "Dell PowerEdge", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, 32, 4)
        detalhes = s.exibir_detalhes()
        self.assertIn("Tipo: Servidor", detalhes)

    def test_servidor_mostra_campos_especificos(self):
        s = Servidor(2, "Dell PowerEdge", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, 32, 4)
        detalhes = s.exibir_detalhes()
        self.assertIn("Memória RAM: 32GB", detalhes)
        self.assertIn("Qtde armazenamento: 4T", detalhes)

    # Roteador
    def test_roteador_mostra_tipo(self):
        r = Roteador(3, "TP-Link", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, 4, 1000)
        detalhes = r.exibir_detalhes()
        self.assertIn("Tipo: Roteador", detalhes)

    def test_roteador_mostra_campos_especificos(self):
        r = Roteador(3, "TP-Link", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, 4, 1000)
        detalhes = r.exibir_detalhes()
        self.assertIn("Qtde de portas: 4", detalhes)
        self.assertIn("Velocidade: 1000MB", detalhes)

    # Impressora
    def test_impressora_mostra_tipo(self):
        i = Impressora(
            4,
            "HP",
            Setor.TI,
            "Cadu",
            StatusDoAtivo.ATIVO,
            Cor.COLORIDA,
            Tecnologia.LASER,
        )
        detalhes = i.exibir_detalhes()
        self.assertIn("Tipo: Impressora", detalhes)

    def test_impressora_mostra_campos_especificos(self):
        i = Impressora(
            4,
            "HP",
            Setor.TI,
            "Cadu",
            StatusDoAtivo.ATIVO,
            Cor.COLORIDA,
            Tecnologia.LASER,
        )
        detalhes = i.exibir_detalhes()
        self.assertIn("Cor: COLORIDA", detalhes)
        self.assertIn("Tecnologia: LASER", detalhes)

    # Campos comuns
    def test_todos_mostram_campos_comuns(self):
        n = Notebook(1, "Dell", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, "Linux", 15.6)
        detalhes = n.exibir_detalhes()
        self.assertIn("ID: 1", detalhes)
        self.assertIn("Nome: Dell", detalhes)
        self.assertIn("Setor: TI", detalhes)
        self.assertIn("Responsável: Cadu", detalhes)
        self.assertIn("Status: ATIVO", detalhes)


# Validações -------------------------------------


# Validar Setor
class TestValidarSetor(unittest.TestCase):

    def test_setor_1_retorna_ti(self):
        self.assertEqual(validar_setor("1"), Setor.TI)

    def test_setor_2_retorna_financeiro(self):
        self.assertEqual(validar_setor("2"), Setor.FINANCEIRO)

    def test_setor_3_retorna_marketing(self):
        self.assertEqual(validar_setor("3"), Setor.MARKETING)

    def test_setor_4_retorna_rh(self):
        self.assertEqual(validar_setor("4"), Setor.RH)

    def test_setor_5_retorna_juridico(self):
        self.assertEqual(validar_setor("5"), Setor.JURIDICO)

    def test_setor_invalido_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            validar_setor("6")


# Validar Status
class TestValidarStatus(unittest.TestCase):

    # --- CASOS VÁLIDOS ---
    def test_status_1_retorna_ativo(self):
        self.assertEqual(validar_status("1"), StatusDoAtivo.ATIVO)

    def test_status_2_retorna_inativo(self):
        self.assertEqual(validar_status("2"), StatusDoAtivo.INATIVO)

    def test_status_3_retorna_manutencao(self):
        self.assertEqual(validar_status("3"), StatusDoAtivo.EM_MANUTENCAO)

    # --- CASOS INVÁLIDOS ---
    def test_status_4_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            validar_status("4")

    def test_status_vazio_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            validar_status("")

    def test_status_texto_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            validar_status("abc")


# Validar Tipo
class TestValidarTipo(unittest.TestCase):

    def test_tipo_1_retorna_notebook(self):
        self.assertEqual(validar_tipo("1"), Notebook)

    def test_tipo_2_retorna_servidor(self):
        self.assertEqual(validar_tipo("2"), Servidor)

    def test_tipo_3_retorna_roteador(self):
        self.assertEqual(validar_tipo("3"), Roteador)

    def test_tipo_4_retorna_impressora(self):
        self.assertEqual(validar_tipo("4"), Impressora)

    # Tipos inválidos

    def test_tipo_5_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            validar_tipo("5")

    def test_tipo_vazio_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            validar_tipo("")

    def test_tipo_texto_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            validar_tipo("abc")


# Validar cor
class TestValidarCor(unittest.TestCase):

    def test_cor_1_retorna_colorido(self):
        self.assertEqual(validar_cor("1"), Cor.COLORIDA)

    def test_cor_2_retorna_preto_branco(self):
        self.assertEqual(validar_cor("2"), Cor.PRETA_E_BRANCA)

    # Cores inválidas

    def test_cor_texto_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            validar_cor("abc")

    def test_cor_3_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            validar_cor("3")

    def test_cor_vazia_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            validar_cor("")


# Validar tecnologia
class TestValidarTech(unittest.TestCase):

    def test_tech_1_retorna_tinta(self):
        self.assertEqual(validar_tecnologia("1"), Tecnologia.TINTA)

    def test_tech_2_retorna_laser(self):
        self.assertEqual(validar_tecnologia("2"), Tecnologia.LASER)

    # Cores inválidas

    def test_tech_texto_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            validar_tecnologia("abc")

    def test_tech_3_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            validar_tecnologia("3")

    def test_tech_vazia_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            validar_tecnologia("")


# Validar Info | Nome/Responsável
class TestValidarNomeResponsavel(unittest.TestCase):

    def test_nome_valido_nao_levanta_erro(self):
        validar_nome_responsavel("Cadu")

    def test_nome_com_espacos_nao_levanta_erro(self):
        validar_nome_responsavel("Ana Maria")

    # Infos inválidas

    def test_nome_numerico_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            validar_nome_responsavel("123")

    def test_nome_vazio_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            validar_nome_responsavel("")


# Funções encontrar ativo ------------------------

# Por ID
class TestEncontrarAtivoPorId(unittest.TestCase):

    def setUp(self):
        self.ativos = {
            1: Notebook(
                1,
                "Dell",
                Setor.TI,
                "Cadu",
                StatusDoAtivo.ATIVO,
                "Linux",
                15.6
            ),
            2: Servidor(
                2,
                "Dell PowerEdge",
                Setor.TI,
                "Cadu",
                StatusDoAtivo.ATIVO,
                32,
                4
            ),
            3: Roteador(
                3,
                "TP-Link",
                Setor.MARKETING,
                "Ana",
                StatusDoAtivo.INATIVO,
                4,
                1000
            ),
            4: Impressora(
                4,
                "HP",
                Setor.RH,
                "Bia",
                StatusDoAtivo.ATIVO,
                Cor.COLORIDA,
                Tecnologia.LASER,
            ),
            5: Notebook(
                5,
                "Dellinho",
                Setor.FINANCEIRO,
                "Henrique",
                StatusDoAtivo.EM_MANUTENCAO,
                "Windows XP",
                32
            ),
        }

    def test_encontra_ativo_existente(self):
        ativo = encontrar_ativo_por_id(1, self.ativos)
        self.assertIsNotNone(ativo)
        self.assertEqual(ativo.nome, "Dell")

    def test_retorna_none_quando_id_nao_existe(self):
        ativo = encontrar_ativo_por_id(99, self.ativos)
        self.assertIsNone(ativo)

    def test_dict_vazio_retorna_none(self):
        ativo = encontrar_ativo_por_id(1, {})
        self.assertIsNone(ativo)

# Por nome
class TestEncontrarAtivosPorNome(unittest.TestCase):

    def setUp(self):
        self.ativos = {
            1: Notebook(
                1,
                "Dell",
                Setor.TI,
                "Cadu",
                StatusDoAtivo.ATIVO,
                "Linux",
                15.6
            ),
            2: Servidor(
                2,
                "Dell PowerEdge",
                Setor.TI,
                "Cadu",
                StatusDoAtivo.ATIVO,
                32,
                4
            ),
            3: Roteador(
                3,
                "TP-Link",
                Setor.MARKETING,
                "Ana",
                StatusDoAtivo.INATIVO,
                4,
                1000
            ),
            4: Impressora(
                4,
                "HP",
                Setor.RH,
                "Bia",
                StatusDoAtivo.ATIVO,
                Cor.COLORIDA,
                Tecnologia.LASER,
            ),
            5: Notebook(
                5,
                "Dellinho",
                Setor.FINANCEIRO,
                "Henrique",
                StatusDoAtivo.EM_MANUTENCAO,
                "Windows XP",
                32
            ),
        }

    def test_busca_nome_exato(self):
        encontrados = encontrar_ativo_por_nome("Dell", self.ativos)
        self.assertEqual(len(encontrados), 3)

    def test_busca_parcial_case_insensitive(self):
        encontrados = encontrar_ativo_por_nome("dell", self.ativos)
        self.assertEqual(len(encontrados), 3)

    def test_busca_nome_unico(self):
        encontrados = encontrar_ativo_por_nome("HP", self.ativos)
        self.assertEqual(len(encontrados), 1)

    def test_busca_sem_resultado(self):
        encontrados = encontrar_ativo_por_nome("Xyz", self.ativos)
        self.assertEqual(len(encontrados), 0)

# Por Status
class TestEncontrarAtivosPorStatus(unittest.TestCase):

    def setUp(self):
        self.ativos = {
            1: Notebook(
                1,
                "Dell",
                Setor.TI,
                "Cadu",
                StatusDoAtivo.ATIVO,
                "Linux",
                15.6
            ),
            2: Servidor(
                2,
                "Dell PowerEdge",
                Setor.TI,
                "Cadu",
                StatusDoAtivo.ATIVO,
                32,
                4
            ),
            3: Roteador(
                3,
                "TP-Link",
                Setor.MARKETING,
                "Ana",
                StatusDoAtivo.INATIVO,
                4,
                1000
            ),
            4: Impressora(
                4,
                "HP",
                Setor.RH,
                "Bia",
                StatusDoAtivo.ATIVO,
                Cor.COLORIDA,
                Tecnologia.LASER,
            ),
            5: Notebook(
                5,
                "Dellinho",
                Setor.FINANCEIRO,
                "Henrique",
                StatusDoAtivo.EM_MANUTENCAO,
                "Windows XP",
                32
            ),
        }

    def test_status_ativo_retorna_3(self):
        encontrados = encontrar_ativos_por_status(StatusDoAtivo.ATIVO, self.ativos)
        self.assertEqual(len(encontrados), 3)

    def test_status_inativo_retorna_1(self):
        encontrados = encontrar_ativos_por_status(StatusDoAtivo.INATIVO, self.ativos)
        self.assertEqual(len(encontrados), 1)

    def test_status_em_manutencao_retorna_0(self):
        encontrados = encontrar_ativos_por_status(
            StatusDoAtivo.EM_MANUTENCAO, self.ativos
        )
        self.assertEqual(len(encontrados), 1)

# Por Tipo
class TestListarAtivosPorTipo(unittest.TestCase):

    def setUp(self):
        self.ativos = {
            1: Notebook(
                1,
                "Dell",
                Setor.TI,
                "Cadu",
                StatusDoAtivo.ATIVO,
                "Linux",
                15.6
            ),
            2: Servidor(
                2,
                "Dell PowerEdge",
                Setor.TI,
                "Cadu",
                StatusDoAtivo.ATIVO,
                32,
                4
            ),
            3: Roteador(
                3,
                "TP-Link",
                Setor.MARKETING,
                "Ana",
                StatusDoAtivo.INATIVO,
                4,
                1000
            ),
            4: Impressora(
                4,
                "HP",
                Setor.RH,
                "Bia",
                StatusDoAtivo.ATIVO,
                Cor.COLORIDA,
                Tecnologia.LASER,
            ),
            5: Notebook(
                5,
                "Dellinho",
                Setor.FINANCEIRO,
                "Henrique",
                StatusDoAtivo.EM_MANUTENCAO,
                "Windows XP",
                32
            ),
        }

    def test_listar_notebooks_retorna_dois(self):
        encontrados = listar_ativos_por_tipo(Notebook, self.ativos)
        self.assertEqual(len(encontrados), 2)

    def test_listar_servidor_retorna_um(self):
        encontrados = listar_ativos_por_tipo(Servidor, self.ativos)
        self.assertEqual(len(encontrados), 1)

    def test_listar_impressora_sem_resultado(self):
        ativos_sem_impressora = self.ativos.copy()
        del ativos_sem_impressora[4]
        encontrados = listar_ativos_por_tipo(Impressora, ativos_sem_impressora)
        self.assertEqual(len(encontrados), 0)


# Serialização -----------------------------------

#Notebook
class TestSerializacaoNotebook(unittest.TestCase):

    def setUp(self):
        self.notebook = Notebook(
            1, "Dell", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, "Linux", 15.6
        )

    def test_para_dicionario_contem_chaves(self):
        dicionario = self.notebook.para_dicionario()
        self.assertIn("id", dicionario)
        self.assertIn("nome", dicionario)
        self.assertIn("tipo", dicionario)
        self.assertIn("sistema_operacional", dicionario)
        self.assertIn("tela", dicionario)

    def test_tipo_esta_correto(self):
        dicionario = self.notebook.para_dicionario()
        self.assertEqual(dicionario["tipo"], "Notebook")

    def test_de_dicionario_reconstroi(self):
        dicionario = self.notebook.para_dicionario()
        reconstruido = Notebook.de_dicionario(dicionario)
        self.assertEqual(reconstruido.id, self.notebook.id)
        self.assertEqual(reconstruido.nome, self.notebook.nome)
        self.assertEqual(reconstruido.sistema_operacional, self.notebook.sistema_operacional)
        self.assertEqual(reconstruido.tela, self.notebook.tela)

# Servidor
class TestSerializacaoServidor(unittest.TestCase):

    def setUp(self):
        self.servidor = Servidor(
            2, "Dell PowerEdge", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, 32, 4
        )

    def test_para_dicionario_contem_chaves(self):
        dicionario = self.servidor.para_dicionario()
        self.assertIn("id", dicionario)
        self.assertIn("nome", dicionario)
        self.assertIn("tipo", dicionario)
        self.assertIn("ram", dicionario)
        self.assertIn("armazenamento", dicionario)

    def test_tipo_esta_correto(self):
        dicionario = self.servidor.para_dicionario()
        self.assertEqual(dicionario["tipo"], "Servidor")

    def test_de_dicionario_reconstroi(self):
        dicionario = self.servidor.para_dicionario()
        reconstruido = Servidor.de_dicionario(dicionario)
        self.assertEqual(reconstruido.id, self.servidor.id)
        self.assertEqual(reconstruido.nome, self.servidor.nome)
        self.assertEqual(reconstruido.ram, self.servidor.ram)
        self.assertEqual(reconstruido.armazenamento, self.servidor.armazenamento)

# Roteador
class TestSerializacaoRoteador(unittest.TestCase):

    def setUp(self):
        self.roteador = Roteador(
            3, "TP-Link", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, 4, 1000
        )

    def test_para_dicionario_contem_chaves(self):
        dicionario = self.roteador.para_dicionario()
        self.assertIn("id", dicionario)
        self.assertIn("nome", dicionario)
        self.assertIn("tipo", dicionario)
        self.assertIn("portas", dicionario)
        self.assertIn("velocidade", dicionario)

    def test_tipo_esta_correto(self):
        dicionario = self.roteador.para_dicionario()
        self.assertEqual(dicionario["tipo"], "Roteador")

    def test_de_dicionario_reconstroi(self):
        dicionario = self.roteador.para_dicionario()
        reconstruido = Roteador.de_dicionario(dicionario)
        self.assertEqual(reconstruido.id, self.roteador.id)
        self.assertEqual(reconstruido.nome, self.roteador.nome)
        self.assertEqual(reconstruido.portas, self.roteador.portas)
        self.assertEqual(reconstruido.velocidade, self.roteador.velocidade)

# Impressora
class TestSerializacaoImpressora(unittest.TestCase):

    def setUp(self):
        self.impressora = Impressora(
            4,
            "HP",
            Setor.TI,
            "Cadu",
            StatusDoAtivo.ATIVO,
            Cor.COLORIDA,
            Tecnologia.LASER,
        )

    def test_para_dicionario_contem_chaves(self):
        dicionario = self.impressora.para_dicionario()
        self.assertIn("id", dicionario)
        self.assertIn("nome", dicionario)
        self.assertIn("tipo", dicionario)
        self.assertIn("cor", dicionario)
        self.assertIn("tecnologia", dicionario)

    def test_tipo_esta_correto(self):
        dicionario = self.impressora.para_dicionario()
        self.assertEqual(dicionario["tipo"], "Impressora")

    def test_de_dicionario_reconstroi(self):
        dicionario = self.impressora.para_dicionario()
        reconstruido = Impressora.de_dicionario(dicionario)
        self.assertEqual(reconstruido.id, self.impressora.id)
        self.assertEqual(reconstruido.nome, self.impressora.nome)
        self.assertEqual(reconstruido.cor, self.impressora.cor)
        self.assertEqual(reconstruido.tecnologia, self.impressora.tecnologia)

# Persistência de dados --------------------------

class TestPersistencia(unittest.TestCase):  

    def setUp(self):
        self.arquivo_teste = "teste_ativos_tmp.json"
        self.arquivo_original = funcoes_t2.ARQUIVO_DADOS
        funcoes_t2.ARQUIVO_DADOS = self.arquivo_teste

    def tearDown(self):
        funcoes_t2.ARQUIVO_DADOS = self.arquivo_original
        if os.path.exists(self.arquivo_teste):
            os.remove(self.arquivo_teste)

    def test_salvar_cria_arquivo(self):
        ativos = {
            1: Notebook(1, "Dell", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, "Linux", 15.6),
        }
        salvar_dados(ativos)
        self.assertTrue(os.path.exists(self.arquivo_teste))

    def test_carregar_devolve_o_que_foi_salvo(self):
        ativos = {
            1: Notebook(1, "Dell", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, "Linux", 15.6),
        }
        salvar_dados(ativos)
        carregados = carregar_dados()
        
        self.assertEqual(len(carregados), 1)
        ativo = carregados[1]
        self.assertEqual(ativo.nome, "Dell")
        self.assertEqual(ativo.sistema_operacional, "Linux")

    def test_carregar_arquivo_inexistente_retorna_vazio(self):
        if os.path.exists(self.arquivo_teste):
            os.remove(self.arquivo_teste)
        self.assertEqual(carregar_dados(), {})

# Testes de Input --------------------------------

# Pedir int:
class TestPedirInt(unittest.TestCase):

    def test_retorna_inteiro_valido(self):
        with patch("builtins.input", return_value="42"):
            resultado = pedir_int("Digite: ")
        self.assertEqual(resultado, 42)

    def test_aceita_zero_ou_negativo(self):
        with patch("builtins.input", side_effect=["0", "5"]):
            resultado = pedir_int("Digite: ")
        self.assertEqual(resultado, 5)

    def test_aceita_texto_depois_numero(self):
        with patch("builtins.input", side_effect=["abc", "7"]):
            resultado = pedir_int("Digite: ")
        self.assertEqual(resultado, 7)

# Pedir float:
class TestPedirFloat(unittest.TestCase):

    def test_retorna_float_valido(self):
        with patch("builtins.input", return_value="3.14"):
            resultado = pedir_float("Digite: ")
        self.assertEqual(resultado, 3.14)

    def test_retorna_float_inteiro(self):
        # aceita "5" também (é float disfarçado)
        with patch("builtins.input", return_value="5"):
            resultado = pedir_float("Digite: ")
        self.assertEqual(resultado, 5.0)

    def test_rejeita_zero_e_aceita_depois(self):
        with patch("builtins.input", side_effect=["0", "2.5"]):
            resultado = pedir_float("Digite: ")
        self.assertEqual(resultado, 2.5)

    def test_rejeita_texto_e_aceita_depois(self):
        with patch("builtins.input", side_effect=["abc", "1.5"]):
            resultado = pedir_float("Digite: ")
        self.assertEqual(resultado, 1.5)

# Pedir Info | Nome/Responsável:
class TestPedirInfo(unittest.TestCase):

    def test_retorna_string_valida(self):
        with patch("builtins.input", return_value="Cadu"):
            resultado = pedir_info("Digite: ")
        self.assertEqual(resultado, "Cadu")

    def test_retorna_string_com_espacos(self):
        with patch("builtins.input", return_value="Ana Maria"):
            resultado = pedir_info("Digite: ")
        self.assertEqual(resultado, "Ana Maria")

    def test_rejeita_vazio_e_aceita_depois(self):
        with patch("builtins.input", side_effect=["", "Cadu"]):
            resultado = pedir_info("Digite: ")
        self.assertEqual(resultado, "Cadu")

    def test_rejeita_numerico_e_aceita_depois(self):
        with patch("builtins.input", side_effect=["123", "Dell"]):
            resultado = pedir_info("Digite: ")
        self.assertEqual(resultado, "Dell")

    def test_remove_espacos_das_bordas(self):
        # input com espaço antes e depois → strip() remove
        with patch("builtins.input", return_value="  Cadu  "):
            resultado = pedir_info("Digite: ")
        self.assertEqual(resultado, "Cadu")

# Input | Enum -----------------------------------

# Pedir Status
class TestPedirStatus(unittest.TestCase):

    def test_retorna_ativo_quando_digita_1(self):
        with patch("builtins.input", return_value="1"):
            resultado = pedir_status("Digite: ")
        self.assertEqual(resultado, StatusDoAtivo.ATIVO)

    def test_retorna_inativo_quando_digita_2(self):
        with patch("builtins.input", return_value="2"):
            resultado = pedir_status("Digite: ")
        self.assertEqual(resultado, StatusDoAtivo.INATIVO)

    def test_retorna_manutencao_quando_digita_3(self):
        with patch("builtins.input", return_value="3"):
            resultado = pedir_status("Digite: ")
        self.assertEqual(resultado, StatusDoAtivo.EM_MANUTENCAO)

    def test_aceita_erro_e_depois_valido(self):
        with patch("builtins.input", side_effect=["9", "1"]):
            resultado = pedir_status("Digite: ")
        self.assertEqual(resultado, StatusDoAtivo.ATIVO)

# Pedir Setor
class TestPedirSetor(unittest.TestCase):

    def test_retorna_ti_digita_1(self):
        with patch('builtins.input', return_value='1'):
            resultado=pedir_setor('Digite: ')
        self.assertEqual(resultado, Setor.TI)

    def test_retorna_finan_digita_2(self):
        with patch('builtins.input', return_value='2'):
            resultado=pedir_setor('Digite: ')
        self.assertEqual(resultado, Setor.FINANCEIRO)

    def test_retorna_mkt_digita_3(self):
        with patch('builtins.input', return_value='3'):
            resultado=pedir_setor('Digite: ')
        self.assertEqual(resultado, Setor.MARKETING)

    def test_retorna_rh_digita_4(self):
        with patch('builtins.input', return_value='4'):
            resultado=pedir_setor('Digite: ')
        self.assertEqual(resultado, Setor.RH)

    def test_retorna_juri_digita_5(self):
        with patch('builtins.input', return_value='5'):
            resultado=pedir_setor('Digite: ')
        self.assertEqual(resultado, Setor.JURIDICO)

    def test_aceita_erro_e_retorna_ti(self):
        with patch("builtins.input", side_effect=["9", "1"]):
            resultado = pedir_setor("Digite: ")
        self.assertEqual(resultado, Setor.TI)

# Pedir Cor
class TestPedirCor(unittest.TestCase):

    def test_retorna_colorido_digita_1(self):
        with patch("builtins.input", return_value="1"):
            resultado = pedir_cor()      # 👈 sem argumento
        self.assertEqual(resultado, Cor.COLORIDA)

    def test_retorna_peb_digita_2(self):
        with patch("builtins.input", return_value="2"):
            resultado = pedir_cor()
        self.assertEqual(resultado, Cor.PRETA_E_BRANCA)

# Pedir Tecnologia
class TestPedirTech(unittest.TestCase):

    def test_retorna_tinta_digita_1(self):
        with patch("builtins.input", return_value="1"):
            resultado = pedir_tecnologia()      # 👈 sem argumento
        self.assertEqual(resultado, Tecnologia.TINTA)

    def test_retorna_laser_digita_2(self):
        with patch("builtins.input", return_value="2"):
            resultado = pedir_tecnologia()
        self.assertEqual(resultado, Tecnologia.LASER)

    def test_aceita_erro_e_retorna_tinta(self):
        with patch("builtins.input", side_effect=["9", "1"]):
            resultado = pedir_tecnologia()
        self.assertEqual(resultado, Tecnologia.TINTA)


# Vulnerabilidades -------------------------------

# Mostrar Vulnerabilidades:
class TestMostrarVulnerabilidade(unittest.TestCase):

    def test_mostra_dados_da_vulnerabilidade(self):
        v = Vulnerabilidade(
            "Senha fraca", "Autenticação",
            NivelDaVulnerabilidade.ALTO,
            StatusDaVuln.ABERTA
        )
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            mostrar_vulnerabilidade(v)
        saida = buffer.getvalue()

        self.assertIn("Senha fraca", saida)
        self.assertIn("Autenticação", saida)
        self.assertIn("alto", saida)   # .name.lower()
        self.assertIn("aberta", saida)

# Nível de Vulnerabilidade
class TestNivelVulnerabilidade(unittest.TestCase):

    def test_retorna_baixo_digita_1(self):
        with patch("builtins.input", return_value="1"):
            resultado = nivel_vulnerabilidade()
        self.assertEqual(resultado, NivelDaVulnerabilidade.BAIXO)

    def test_retorna_medio_digita_2(self):
        with patch("builtins.input", return_value="2"):
            resultado = nivel_vulnerabilidade()
        self.assertEqual(resultado, NivelDaVulnerabilidade.MEDIO)

    def test_retorna_alto_digita_3(self):
        with patch("builtins.input", return_value="3"):
            resultado = nivel_vulnerabilidade()
        self.assertEqual(resultado, NivelDaVulnerabilidade.ALTO)

    def test_aceita_erro_e_depois_valido(self):
        with patch("builtins.input", side_effect=["9", "2"]):
            resultado = nivel_vulnerabilidade()
        self.assertEqual(resultado, NivelDaVulnerabilidade.MEDIO)

# Status de Vulnerabilidade
class TestStatusVulnerabilidade(unittest.TestCase):

    def test_retorna_aberta_digita_1(self):
        with patch("builtins.input", return_value="1"):
            resultado = status_vulnerabilidade()
        self.assertEqual(resultado, StatusDaVuln.ABERTA)

    def test_retorna_em_tratamento_digita_2(self):
        with patch("builtins.input", return_value="2"):
            resultado = status_vulnerabilidade()
        self.assertEqual(resultado, StatusDaVuln.EM_TRATAMENTO)

    def test_retorna_corrigida_digita_3(self):
        with patch("builtins.input", return_value="3"):
            resultado = status_vulnerabilidade()
        self.assertEqual(resultado, StatusDaVuln.CORRIGIDA)

    def test_retorna_aceita_digita_4(self):
        with patch("builtins.input", return_value="4"):
            resultado = status_vulnerabilidade()
        self.assertEqual(resultado, StatusDaVuln.ACEITA)

    def test_aceita_erro_e_depois_valido(self):
        with patch("builtins.input", side_effect=["9", "3"]):
            resultado = status_vulnerabilidade()
        self.assertEqual(resultado, StatusDaVuln.CORRIGIDA)

if __name__ == "__main__":
    unittest.main()
