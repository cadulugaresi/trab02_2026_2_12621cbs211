import io
import os
import unittest
from contextlib import redirect_stdout
from inventario.dominio.enums import (
    Cor,
    Setor,
    StatusDaVuln,
    StatusDoAtivo,
    Tecnologia,
)
from inventario.interface.entradas import (
    pedir_cor,
    pedir_fator_exposicao,
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
from inventario.persistencia.arquivos_json import carregar_ativos, salvar_ativos
from inventario.interface.ativos import (
    cadastrar_ativo,
    cadastro_impressora,
    cadastro_notebook,
    cadastro_roteador,
    cadastro_servidor,
    confirmar_exclusao,
    editar_ativo,
    excluir_ativo,
    pedir_id_disponivel,
)
from inventario.servicos.ativos import (
    atualizar_ativo_no_inventario,
    encontrar_ativo_por_id,
    encontrar_ativos_por_nome,
    encontrar_ativos_por_status,
    encontrar_ativos_por_tipo,
    obter_ativo,
    registrar_ativo_no_inventario,
    remover_ativo_do_inventario,
)
from inventario.dominio.validacoes import (
    validar_cvss,
    validar_fator_exposicao,
    validar_fracao_da_dependencia,
    validar_inteiro_positivo,
    validar_numero,
    validar_numero_positivo,
    validar_texto_obrigatorio,
)
from inventario.interface.conversao_das_opcoes_do_menu import (
    validar_cor,
    validar_setor,
    validar_status,
    validar_tecnologia,
    validar_tipo,
)
from tests.apoio import TesteComArquivosTemporarios
from unittest.mock import patch

MENSAGEM_DE_NUMERO_GRANDE_DEMAIS = (
    "Este número é grande demais. O máximo aceito é 9223372036854775807."
)


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
        i = Impressora(
            4, "HP", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, Cor.COLORIDA, Tecnologia.LASER
        )
        detalhes = i.exibir_detalhes()
        self.assertIn("Tipo: Impressora", detalhes)

    def test_impressora_mostra_campos_especificos(self):
        i = Impressora(
            4, "HP", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, Cor.COLORIDA, Tecnologia.LASER
        )
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


class TestValidarTextoObrigatorio(unittest.TestCase):

    def test_texto_valido_nao_levanta_erro(self):
        validar_texto_obrigatorio("Cadu")

    def test_texto_numerico_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            validar_texto_obrigatorio("123")

    def test_texto_vazio_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            validar_texto_obrigatorio("")

    def test_texto_com_120_caracteres_e_aceito(self):
        validar_texto_obrigatorio("R" * 120)

    def test_texto_com_mais_de_120_caracteres_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError) as contexto:
            validar_texto_obrigatorio("R" * 121)

        self.assertEqual(str(contexto.exception), "Este campo pode ter no máximo 120 caracteres.")


class TestValidarFatorExposicao(unittest.TestCase):

    def test_fator_dentro_da_faixa_e_devolvido(self):
        self.assertEqual(validar_fator_exposicao(1.4), 1.4)

    def test_fator_igual_a_dois_e_aceito(self):
        self.assertEqual(validar_fator_exposicao(2), 2)

    def test_fator_zero_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            validar_fator_exposicao(0)

    def test_fator_negativo_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            validar_fator_exposicao(-1)

    def test_fator_acima_de_dois_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            validar_fator_exposicao(2.1)


class TestValidacoesNumericas(unittest.TestCase):

    def setUp(self):
        self.valores_nao_finitos = [float("nan"), float("inf"), float("-inf")]

    def conferir_recusa(self, validacao, valor, mensagem_esperada):
        with self.assertRaises(DadoInvalidoError) as contexto:
            validacao(valor)
        self.assertEqual(str(contexto.exception), mensagem_esperada)

    def test_numero_inteiro_e_fracionario_sao_devolvidos(self):
        self.assertEqual(validar_numero(3), 3)
        self.assertEqual(validar_numero(2.5), 2.5)

    def test_booleano_e_texto_nao_sao_numeros(self):
        for valor in [True, "3"]:
            with self.subTest(valor=valor):
                self.conferir_recusa(validar_numero, valor, "Este campo precisa ser um número.")

    def test_valores_nao_finitos_sao_recusados_pelo_validar_numero(self):
        for valor in self.valores_nao_finitos:
            with self.subTest(valor=valor):
                self.conferir_recusa(
                    validar_numero, valor, "Este campo precisa ser um número finito."
                )

    def test_valores_nao_finitos_sao_recusados_pelo_validar_numero_positivo(self):
        for valor in self.valores_nao_finitos:
            with self.subTest(valor=valor):
                self.conferir_recusa(
                    validar_numero_positivo, valor, "Este campo precisa ser um número finito."
                )

    def test_valores_nao_finitos_sao_recusados_pelo_validar_cvss(self):
        for valor in self.valores_nao_finitos:
            with self.subTest(valor=valor):
                self.conferir_recusa(
                    validar_cvss, valor, "Este campo precisa ser um número finito."
                )

    def test_valores_nao_finitos_sao_recusados_pelo_validar_fator_exposicao(self):
        for valor in self.valores_nao_finitos:
            with self.subTest(valor=valor):
                self.conferir_recusa(
                    validar_fator_exposicao, valor, "Este campo precisa ser um número finito."
                )

    def test_valores_nao_finitos_sao_recusados_na_fracao_da_dependencia(self):
        for valor in self.valores_nao_finitos:
            with self.subTest(valor=valor):
                with self.assertRaises(DadoInvalidoError) as contexto:
                    validar_fracao_da_dependencia(0, valor)
                self.assertEqual(
                    str(contexto.exception), "Este campo precisa ser um número finito."
                )

    def test_maior_inteiro_aceito_e_devolvido(self):
        maior_inteiro_aceito = 2**63 - 1

        for validacao in [validar_numero, validar_numero_positivo, validar_inteiro_positivo]:
            with self.subTest(validacao=validacao.__name__):
                self.assertEqual(validacao(maior_inteiro_aceito), maior_inteiro_aceito)

    def test_inteiro_acima_do_limite_e_recusado_sem_estourar(self):
        for validacao in [validar_numero, validar_numero_positivo, validar_inteiro_positivo]:
            for valor in [2**63, 10**400]:
                with self.subTest(validacao=validacao.__name__, digitos=len(str(valor))):
                    self.conferir_recusa(validacao, valor, MENSAGEM_DE_NUMERO_GRANDE_DEMAIS)


# Funções encontrar ativo ------------------------


class TestEncontrarAtivoPorId(unittest.TestCase):

    def setUp(self):
        self.ativos = {
            1: Notebook(1, "Dell", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, "Linux", 15.6),
            2: Servidor(2, "Dell PowerEdge", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, 32, 4),
            3: Roteador(3, "TP-Link", Setor.MARKETING, "Ana", StatusDoAtivo.INATIVO, 4, 1000),
            4: Impressora(
                4, "HP", Setor.RH, "Bia", StatusDoAtivo.ATIVO, Cor.COLORIDA, Tecnologia.LASER
            ),
            5: Notebook(
                5,
                "Dellinho",
                Setor.FINANCEIRO,
                "Henrique",
                StatusDoAtivo.EM_MANUTENCAO,
                "Windows XP",
                32,
            ),
        }

    def test_encontra_ativo_existente(self):
        ativo = encontrar_ativo_por_id(self.ativos, 1)
        self.assertIsNotNone(ativo)
        self.assertEqual(ativo.nome, "Dell")

    def test_retorna_none_quando_id_nao_existe(self):
        ativo = encontrar_ativo_por_id(self.ativos, 99)
        self.assertIsNone(ativo)


class TestObterAtivo(unittest.TestCase):

    def setUp(self):
        self.notebook = Notebook(
            1, "Dell", Setor.TI, "Rafael Torres", StatusDoAtivo.ATIVO, "Linux", 15.6
        )
        self.ativos = {1: self.notebook}

    def test_devolve_ativo_existente(self):
        self.assertIs(obter_ativo(self.ativos, 1), self.notebook)

    def test_id_inexistente_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            obter_ativo(self.ativos, 99)


class TestRemoverAtivoDoInventario(TesteComArquivosTemporarios):

    def setUp(self):
        super().setUp()
        self.notebook = Notebook(
            1, "Dell", Setor.TI, "Rafael Torres", StatusDoAtivo.ATIVO, "Linux", 15.6
        )
        self.ativos = {1: self.notebook}

    def test_remove_e_salva(self):
        remover_ativo_do_inventario(self.repositorio, self.ativos, 1)
        self.assertNotIn(1, self.ativos)
        self.assertNotIn(1, carregar_ativos())

    def test_id_inexistente_levanta_erro(self):
        with self.assertRaises(DadoInvalidoError):
            remover_ativo_do_inventario(self.repositorio, self.ativos, 99)
        self.assertIn(1, self.ativos)


class TestAtualizarAtivoNoInventario(TesteComArquivosTemporarios):

    def setUp(self):
        super().setUp()
        self.notebook = Notebook(
            1, "Dell", Setor.TI, "Rafael Torres", StatusDoAtivo.ATIVO, "Linux", 15.6
        )
        self.notebook.vulnerabilidades[3] = StatusDaVuln.ABERTA
        self.ativos = {1: self.notebook}
        salvar_ativos(self.ativos)

    def test_salva_edicao_simples(self):
        self.notebook.responsavel = "Ana Souza"
        atualizar_ativo_no_inventario(self.repositorio, self.ativos, self.notebook)
        self.assertEqual(carregar_ativos()[1].responsavel, "Ana Souza")

    def test_troca_de_tipo_mantem_as_vulnerabilidades(self):
        servidor = Servidor(1, "Dell", Setor.TI, "Rafael Torres", StatusDoAtivo.ATIVO, 32, 4)
        atualizar_ativo_no_inventario(self.repositorio, self.ativos, servidor)
        self.assertIs(self.ativos[1], servidor)
        self.assertEqual(servidor.vulnerabilidades, {3: StatusDaVuln.ABERTA})
        self.assertIsInstance(carregar_ativos()[1], Servidor)

    def test_id_inexistente_levanta_erro(self):
        roteador = Roteador(99, "TP-Link", Setor.TI, "Rafael Torres", StatusDoAtivo.ATIVO, 4, 1000)
        with self.assertRaises(DadoInvalidoError):
            atualizar_ativo_no_inventario(self.repositorio, self.ativos, roteador)
        self.assertNotIn(99, self.ativos)

    def test_recusa_ativo_com_dados_invalidos_sem_alterar_memoria_nem_arquivo(self):
        dicionario_antes = self.notebook.para_dicionario()
        casos = [
            (
                "nome vazio",
                Notebook(1, "", Setor.TI, "Rafael Torres", StatusDoAtivo.ATIVO, "Linux", 15.6),
                "Este campo não pode ser vazio.",
            ),
            (
                "responsável numérico",
                Notebook(1, "Dell", Setor.TI, "123", StatusDoAtivo.ATIVO, "Linux", 15.6),
                "Este campo não pode ser composto apenas por números.",
            ),
            (
                "tela negativa",
                Notebook(1, "Dell", Setor.TI, "Rafael Torres", StatusDoAtivo.ATIVO, "Linux", -3),
                "Este campo não pode ser nulo ou negativo.",
            ),
            (
                "troca para servidor com RAM fracionária",
                Servidor(1, "Dell", Setor.TI, "Rafael Torres", StatusDoAtivo.ATIVO, 8.5, 4),
                "Este campo precisa ser um número inteiro.",
            ),
        ]

        for descricao, ativo_invalido, mensagem_esperada in casos:
            with self.subTest(caso=descricao):
                with self.assertRaises(DadoInvalidoError) as contexto:
                    atualizar_ativo_no_inventario(self.repositorio, self.ativos, ativo_invalido)

                self.assertEqual(str(contexto.exception), mensagem_esperada)
                self.assertIs(self.ativos[1], self.notebook)
                self.assertEqual(carregar_ativos()[1].para_dicionario(), dicionario_antes)


class TestEncontrarAtivosPorNome(unittest.TestCase):

    def setUp(self):
        self.ativos = {
            1: Notebook(1, "Dell", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, "Linux", 15.6),
            2: Servidor(2, "Dell PowerEdge", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, 32, 4),
            3: Roteador(3, "TP-Link", Setor.MARKETING, "Ana", StatusDoAtivo.INATIVO, 4, 1000),
        }

    def test_busca_nome_exato(self):
        encontrados = encontrar_ativos_por_nome(self.ativos, "Dell")
        self.assertEqual(len(encontrados), 2)

    def test_busca_parcial_case_insensitive(self):
        encontrados = encontrar_ativos_por_nome(self.ativos, "dell")
        self.assertEqual(len(encontrados), 2)

    def test_busca_sem_resultado(self):
        encontrados = encontrar_ativos_por_nome(self.ativos, "Xyz")
        self.assertEqual(len(encontrados), 0)


class TestEncontrarAtivosPorStatus(unittest.TestCase):

    def setUp(self):
        self.ativos = {
            1: Notebook(1, "Dell", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, "Linux", 15.6),
            2: Servidor(2, "Dell PowerEdge", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, 32, 4),
            3: Roteador(3, "TP-Link", Setor.MARKETING, "Ana", StatusDoAtivo.INATIVO, 4, 1000),
        }

    def test_status_ativo_retorna_2(self):
        encontrados = encontrar_ativos_por_status(self.ativos, StatusDoAtivo.ATIVO)
        self.assertEqual(len(encontrados), 2)

    def test_status_inativo_retorna_1(self):
        encontrados = encontrar_ativos_por_status(self.ativos, StatusDoAtivo.INATIVO)
        self.assertEqual(len(encontrados), 1)


class TestListarAtivosPorTipo(unittest.TestCase):

    def setUp(self):
        self.ativos = {
            1: Notebook(1, "Dell", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, "Linux", 15.6),
            2: Servidor(2, "Dell PowerEdge", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, 32, 4),
            3: Roteador(3, "TP-Link", Setor.MARKETING, "Ana", StatusDoAtivo.INATIVO, 4, 1000),
        }

    def test_listar_notebooks_retorna_um(self):
        encontrados = encontrar_ativos_por_tipo(self.ativos, Notebook)
        self.assertEqual(len(encontrados), 1)

    def test_listar_impressora_retorna_vazio(self):
        encontrados = encontrar_ativos_por_tipo(self.ativos, Impressora)
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
        self.impressora = Impressora(
            4, "HP", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, Cor.COLORIDA, Tecnologia.LASER
        )

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
        salvar_ativos(ativos)
        self.assertTrue(os.path.exists(self.arquivo_dados))

    def test_carregar_devolve_o_que_foi_salvo(self):
        ativos = {1: Notebook(1, "Dell", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, "Linux", 15.6)}
        salvar_ativos(ativos)
        carregados = carregar_ativos()
        self.assertEqual(len(carregados), 1)
        self.assertEqual(carregados[1].nome, "Dell")

    def test_carregar_arquivo_inexistente_retorna_vazio(self):
        self.assertEqual(carregar_ativos(), {})


# Testes de Input --------------------------------


def responder_e_capturar_saida(funcao_que_pergunta, respostas):
    saida = io.StringIO()
    with patch("builtins.input", side_effect=respostas):
        with redirect_stdout(saida):
            valor_devolvido = funcao_que_pergunta("Digite: ")
    return valor_devolvido, saida.getvalue()


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

    def test_zero_e_negativo_mostram_a_mensagem_do_dominio(self):
        for resposta_invalida in ["0", "-3"]:
            with self.subTest(resposta=resposta_invalida):
                valor, saida = responder_e_capturar_saida(pedir_int, [resposta_invalida, "5"])

                self.assertEqual(valor, 5)
                self.assertEqual(saida, "Este campo não pode ser nulo ou negativo.\n")

    def test_campo_vazio_mostra_a_mensagem_e_pergunta_de_novo(self):
        valor, saida = responder_e_capturar_saida(pedir_int, ["", "5"])

        self.assertEqual(valor, 5)
        self.assertEqual(saida, "Este campo não pode ser vazio.\n")

    def test_numero_fracionario_nao_e_aceito_como_inteiro(self):
        valor, saida = responder_e_capturar_saida(pedir_int, ["3.5", "5"])

        self.assertEqual(valor, 5)
        self.assertEqual(saida, "Digite um número válido\n")

    def test_numero_acima_do_limite_mostra_o_maximo_e_pergunta_de_novo(self):
        valor, saida = responder_e_capturar_saida(pedir_int, ["9223372036854775808", "5"])

        self.assertEqual(valor, 5)
        self.assertEqual(saida, MENSAGEM_DE_NUMERO_GRANDE_DEMAIS + "\n")


class TestPedirFloat(unittest.TestCase):

    def test_retorna_float_valido(self):
        with patch("builtins.input", return_value="3.14"):
            self.assertEqual(pedir_float("Digite: "), 3.14)

    def test_rejeita_zero_e_aceita_depois(self):
        with patch("builtins.input", side_effect=["0", "2.5"]):
            self.assertEqual(pedir_float("Digite: "), 2.5)

    def test_valores_nao_finitos_digitados_sao_recusados(self):
        for resposta_invalida in ["nan", "NaN", "inf", "-inf", "Infinity"]:
            with self.subTest(resposta=resposta_invalida):
                valor, saida = responder_e_capturar_saida(pedir_float, [resposta_invalida, "2.5"])

                self.assertEqual(valor, 2.5)
                self.assertEqual(saida, "Este campo precisa ser um número finito.\n")

    def test_zero_e_negativo_mostram_a_mensagem_do_dominio(self):
        for resposta_invalida in ["0", "-1,5"]:
            with self.subTest(resposta=resposta_invalida):
                valor, saida = responder_e_capturar_saida(pedir_float, [resposta_invalida, "2.5"])

                self.assertEqual(valor, 2.5)
                self.assertEqual(saida, "Este campo não pode ser nulo ou negativo.\n")

    def test_campo_vazio_mostra_a_mensagem_e_pergunta_de_novo(self):
        valor, saida = responder_e_capturar_saida(pedir_float, ["", "2.5"])

        self.assertEqual(valor, 2.5)
        self.assertEqual(saida, "Este campo não pode ser vazio.\n")

    def test_texto_mostra_que_o_numero_e_invalido(self):
        valor, saida = responder_e_capturar_saida(pedir_float, ["abc", "2.5"])

        self.assertEqual(valor, 2.5)
        self.assertEqual(saida, "Digite um número válido\n")


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
        respostas = ["1", "5", "Dell", "1", "Cadu", "1", "Linux", "15.6", ""]
        with patch("builtins.input", side_effect=respostas):
            ativo = cadastrar_ativo(self.repositorio, ativos)
        self.assertIs(ativos[5], ativo)
        self.assertIn(5, carregar_ativos())

    def test_registrar_id_repetido_levanta_erro(self):
        ativo = Notebook(1, "Dell", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, "Linux", 15.6)
        ativos = {1: ativo}
        with self.assertRaises(DadoInvalidoError):
            registrar_ativo_no_inventario(self.repositorio, ativos, ativo)

    def test_cadastra_notebook(self):
        # Ordem: tipo, id, nome, setor, responsável, status, so, tela, fator de exposição
        respostas = ["1", "5", "Dell", "1", "Cadu", "1", "Linux", "15.6", ""]
        with patch("builtins.input", side_effect=respostas):
            ativo = cadastrar_ativo(self.repositorio, {})
        self.assertIsInstance(ativo, Notebook)
        self.assertEqual(ativo.id, 5)
        self.assertEqual(ativo.nome, "Dell")
        self.assertEqual(ativo.sistema_operacional, "Linux")
        self.assertEqual(ativo.tela, 15.6)

    def test_cadastra_servidor(self):
        respostas = ["2", "6", "PowerEdge", "1", "Cadu", "1", "32", "4", ""]
        with patch("builtins.input", side_effect=respostas):
            ativo = cadastrar_ativo(self.repositorio, {})
        self.assertIsInstance(ativo, Servidor)
        self.assertEqual(ativo.ram, 32)

    def test_cadastra_roteador(self):
        respostas = ["3", "7", "TP-Link", "1", "Cadu", "1", "4", "1000", ""]
        with patch("builtins.input", side_effect=respostas):
            ativo = cadastrar_ativo(self.repositorio, {})
        self.assertIsInstance(ativo, Roteador)
        self.assertEqual(ativo.portas, 4)

    def test_cadastra_impressora(self):
        respostas = ["4", "8", "HP", "1", "Cadu", "1", "1", "2", ""]
        with patch("builtins.input", side_effect=respostas):
            ativo = cadastrar_ativo(self.repositorio, {})
        self.assertIsInstance(ativo, Impressora)
        self.assertEqual(ativo.cor, Cor.COLORIDA)


class TestCadastrarAtivoComFatorDeExposicao(TesteComArquivosTemporarios):

    def cadastrar_notebook_com_fator(self, respostas_do_fator):
        respostas = ["1", "5", "Dell", "1", "Rafael Torres", "1", "Linux", "15.6"]
        respostas.extend(respostas_do_fator)
        with patch("builtins.input", side_effect=respostas):
            with patch("builtins.print"):
                return cadastrar_ativo(self.repositorio, {})

    def test_enter_mantem_o_fator_padrao_do_tipo(self):
        ativo = self.cadastrar_notebook_com_fator([""])
        self.assertEqual(ativo.fator_exposicao, Notebook.FATOR_EXPOSICAO_PADRAO)

    def test_guarda_o_fator_digitado(self):
        ativo = self.cadastrar_notebook_com_fator(["1.4"])
        self.assertEqual(ativo.fator_exposicao, 1.4)

    def test_aceita_virgula_como_separador_decimal(self):
        ativo = self.cadastrar_notebook_com_fator(["1,4"])
        self.assertEqual(ativo.fator_exposicao, 1.4)

    def test_texto_invalido_pergunta_de_novo(self):
        ativo = self.cadastrar_notebook_com_fator(["abc", "1.4"])
        self.assertEqual(ativo.fator_exposicao, 1.4)

    def test_fator_fora_da_faixa_pergunta_de_novo(self):
        ativo = self.cadastrar_notebook_com_fator(["5", "0", "1.4"])
        self.assertEqual(ativo.fator_exposicao, 1.4)

    def test_fator_digitado_e_salvo_no_repositorio(self):
        self.cadastrar_notebook_com_fator(["1.4"])
        self.assertEqual(carregar_ativos()[5].fator_exposicao, 1.4)


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


# Excluir Ativo ----------------------------------


class TestExcluirAtivo(TesteComArquivosTemporarios):

    def setUp(self):
        super().setUp()
        self.ativos = {
            1: Notebook(1, "Dell", Setor.TI, "Rafael Torres", StatusDoAtivo.ATIVO, "Linux", 15.6)
        }

    def test_confirmando_remove_e_salva(self):
        with patch("builtins.input", side_effect=["1", "sim"]):
            excluir_ativo(self.repositorio, self.ativos)
        self.assertNotIn(1, self.ativos)
        self.assertNotIn(1, carregar_ativos())

    def test_cancelando_mantem_o_ativo(self):
        with patch("builtins.input", side_effect=["1", ""]):
            excluir_ativo(self.repositorio, self.ativos)
        self.assertIn(1, self.ativos)

    def test_id_inexistente_nao_pede_confirmacao(self):
        with patch("builtins.input", side_effect=["99"]) as entrada:
            excluir_ativo(self.repositorio, self.ativos)
        self.assertEqual(entrada.call_count, 1)
        self.assertIn(1, self.ativos)


# Editar Ativo -----------------------------------


class TestEditarAtivo(TesteComArquivosTemporarios):

    def setUp(self):
        super().setUp()
        self.notebook = Notebook(
            1, "Dell", Setor.TI, "Rafael Torres", StatusDoAtivo.ATIVO, "Linux", 15.6
        )
        self.notebook.vulnerabilidades[3] = StatusDaVuln.ABERTA
        self.ativos = {1: self.notebook}
        salvar_ativos(self.ativos)

    def test_editar_responsavel_salva_ao_voltar(self):
        with patch("builtins.input", side_effect=["1", "1", "Ana Souza", "7"]):
            editar_ativo(self.repositorio, self.ativos)
        self.assertEqual(carregar_ativos()[1].responsavel, "Ana Souza")

    def test_trocar_tipo_mantem_as_vulnerabilidades(self):
        with patch("builtins.input", side_effect=["1", "5", "2", "32", "4", "7"]):
            editar_ativo(self.repositorio, self.ativos)
        self.assertIsInstance(self.ativos[1], Servidor)
        self.assertEqual(self.ativos[1].vulnerabilidades, {3: StatusDaVuln.ABERTA})
        self.assertIsInstance(carregar_ativos()[1], Servidor)

    def test_trocar_tipo_volta_o_fator_para_o_padrao_do_tipo_novo(self):
        self.notebook.fator_exposicao = 1.7
        salvar_ativos(self.ativos)
        with patch("builtins.input", side_effect=["1", "5", "2", "32", "4", "7"]):
            with patch("builtins.print"):
                editar_ativo(self.repositorio, self.ativos)
        self.assertEqual(self.ativos[1].fator_exposicao, Servidor.FATOR_EXPOSICAO_PADRAO)
        self.assertEqual(carregar_ativos()[1].fator_exposicao, Servidor.FATOR_EXPOSICAO_PADRAO)

    def test_id_inexistente_nao_abre_o_menu(self):
        with patch("builtins.input", side_effect=["99"]) as entrada:
            editar_ativo(self.repositorio, self.ativos)
        self.assertEqual(entrada.call_count, 1)

    def editar_fator_do_notebook(self, respostas_do_fator):
        respostas = ["1", "6"]
        respostas.extend(respostas_do_fator)
        respostas.append("7")
        with patch("builtins.input", side_effect=respostas):
            with patch("builtins.print"):
                editar_ativo(self.repositorio, self.ativos)

    def test_editar_fator_salva_ao_voltar(self):
        self.editar_fator_do_notebook(["1.4"])
        self.assertEqual(self.ativos[1].fator_exposicao, 1.4)
        self.assertEqual(carregar_ativos()[1].fator_exposicao, 1.4)

    def test_enter_na_edicao_pergunta_de_novo(self):
        self.editar_fator_do_notebook(["", "1.4"])
        self.assertEqual(self.ativos[1].fator_exposicao, 1.4)
        self.assertEqual(carregar_ativos()[1].fator_exposicao, 1.4)

    def test_fator_invalido_na_edicao_pergunta_de_novo(self):
        self.editar_fator_do_notebook(["abc", "3", "1.4"])
        self.assertEqual(self.ativos[1].fator_exposicao, 1.4)

    def test_ativo_antigo_invalido_mostra_o_erro_sem_travar_nem_salvar(self):
        self.notebook.nome = "123"
        salvar_ativos(self.ativos)
        saida = io.StringIO()

        with patch("builtins.input", side_effect=["1", "2", "3", "7"]):
            with redirect_stdout(saida):
                editar_ativo(self.repositorio, self.ativos)

        self.assertIn("Este campo não pode ser composto apenas por números.", saida.getvalue())
        self.assertIn("As alterações não foram salvas.", saida.getvalue())
        self.assertIs(self.ativos[1], self.notebook)
        self.assertEqual(self.notebook.status, StatusDoAtivo.ATIVO)
        self.assertEqual(carregar_ativos()[1].status, StatusDoAtivo.ATIVO)


class TestPedirFatorExposicao(unittest.TestCase):

    def pedir_com_respostas(self, respostas, fator_sugerido=None):
        with patch("builtins.input", side_effect=respostas):
            with patch("builtins.print"):
                return pedir_fator_exposicao("Fator de exposição: ", fator_sugerido)

    def test_enter_com_sugerido_devolve_o_sugerido(self):
        self.assertEqual(self.pedir_com_respostas([""], 1.3), 1.3)

    def test_enter_sem_sugerido_pergunta_de_novo(self):
        self.assertEqual(self.pedir_com_respostas(["", "1.4"]), 1.4)

    def test_espaco_com_sugerido_conta_como_enter(self):
        self.assertEqual(self.pedir_com_respostas(["   "], 1.3), 1.3)

    def test_devolve_o_numero_digitado(self):
        self.assertEqual(self.pedir_com_respostas(["1.4"], 1.3), 1.4)

    def test_aceita_virgula(self):
        self.assertEqual(self.pedir_com_respostas(["0,8"]), 0.8)

    def test_pergunta_de_novo_ate_receber_valor_valido(self):
        self.assertEqual(self.pedir_com_respostas(["abc", "0", "2.5", "2"]), 2)


if __name__ == "__main__":
    unittest.main()
