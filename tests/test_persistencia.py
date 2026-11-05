import json
import os
from unittest.mock import patch

from inventario.dominio.ativo import Impressora, Notebook, Roteador, Servidor
from inventario.dominio.enums import Cor, Setor, StatusDaVuln, StatusDoAtivo, Tecnologia
from inventario.dominio.excecoes import PersistenciaError
from inventario.dominio.vulnerabilidade import Vulnerabilidade
from inventario.persistencia.arquivos_json import (
    carregar_catalogo,
    carregar_dados,
    salvar_catalogo,
    salvar_dados,
)
from tests.apoio import TesteComArquivosTemporarios


def criar_um_ativo_de_cada_tipo():
    notebook = Notebook(
        1, "Notebook da Recepção", Setor.TI, "Rafael Torres", StatusDoAtivo.ATIVO, "Linux", 15.6
    )
    servidor = Servidor(
        2, "Servidor de Arquivos", Setor.FINANCEIRO, "Rafael Torres", StatusDoAtivo.ATIVO, 32, 4
    )
    roteador = Roteador(
        3, "Roteador do Escritório", Setor.TI, "Rafael Torres", StatusDoAtivo.EM_MANUTENCAO, 8, 1000
    )
    impressora = Impressora(
        4,
        "Impressora do RH",
        Setor.RH,
        "Rafael Torres",
        StatusDoAtivo.INATIVO,
        Cor.COLORIDA,
        Tecnologia.LASER,
    )
    return {1: notebook, 2: servidor, 3: roteador, 4: impressora}


class TestEscritaAtomica(TesteComArquivosTemporarios):

    def test_salvar_dados_nao_deixa_arquivo_temporario(self):
        salvar_dados(criar_um_ativo_de_cada_tipo())
        self.assertTrue(os.path.exists(self.arquivo_dados))
        self.assertFalse(os.path.exists(self.arquivo_dados + ".tmp"))

    def test_salvar_catalogo_nao_deixa_arquivo_temporario(self):
        salvar_catalogo({1: Vulnerabilidade(1, "SSH com senha fraca", 7.5)})
        self.assertTrue(os.path.exists(self.arquivo_catalogo))
        self.assertFalse(os.path.exists(self.arquivo_catalogo + ".tmp"))

    def test_salvar_inventario_vazio_grava_lista_vazia(self):
        salvar_dados(criar_um_ativo_de_cada_tipo())
        salvar_dados({})
        self.assertEqual(carregar_dados(), {})

    def test_falha_na_gravacao_preserva_o_arquivo_anterior(self):
        self.addCleanup(os.remove, self.arquivo_dados + ".tmp")
        salvar_dados(criar_um_ativo_de_cada_tipo())

        with patch("inventario.persistencia.arquivos_json.os.replace", side_effect=OSError):
            with self.assertRaises(PersistenciaError):
                salvar_dados({})

        self.assertEqual(len(carregar_dados()), 4)

    def test_sem_permissao_lanca_persistencia_error(self):
        with patch("builtins.open", side_effect=PermissionError):
            with self.assertRaises(PersistenciaError):
                salvar_dados(criar_um_ativo_de_cada_tipo())

    def test_grava_acentos_sem_escapar(self):
        salvar_dados(criar_um_ativo_de_cada_tipo())

        with open(self.arquivo_dados, encoding="utf-8") as arquivo:
            conteudo = arquivo.read()

        self.assertIn("Notebook da Recepção", conteudo)


class TestArquivoCorrompido(TesteComArquivosTemporarios):

    def escrever_texto_invalido(self, caminho):
        with open(caminho, "w", encoding="utf-8") as arquivo:
            arquivo.write('[{"id": 1, "nome": "Notebook"')

    def test_carregar_dados_corrompido_lanca_persistencia_error(self):
        self.escrever_texto_invalido(self.arquivo_dados)

        with self.assertRaises(PersistenciaError):
            carregar_dados()

    def test_carregar_catalogo_corrompido_lanca_persistencia_error(self):
        self.escrever_texto_invalido(self.arquivo_catalogo)

        with self.assertRaises(PersistenciaError):
            carregar_catalogo()

    def test_arquivo_corrompido_continua_intacto_apos_tentar_carregar(self):
        self.escrever_texto_invalido(self.arquivo_dados)

        with self.assertRaises(PersistenciaError):
            carregar_dados()

        with open(self.arquivo_dados, encoding="utf-8") as arquivo:
            self.assertEqual(arquivo.read(), '[{"id": 1, "nome": "Notebook"')


class TestGravarERecarregar(TesteComArquivosTemporarios):

    def test_arquivo_e_um_array_de_objetos_com_campo_tipo(self):
        salvar_dados(criar_um_ativo_de_cada_tipo())

        with open(self.arquivo_dados, encoding="utf-8") as arquivo:
            dados_brutos = json.load(arquivo)

        self.assertIsInstance(dados_brutos, list)

        tipos_gravados = []
        for registro in dados_brutos:
            tipos_gravados.append(registro["tipo"])

        self.assertEqual(tipos_gravados, ["Notebook", "Servidor", "Roteador", "Impressora"])

    def test_recarrega_cada_ativo_na_subclasse_certa(self):
        salvar_dados(criar_um_ativo_de_cada_tipo())
        carregados = carregar_dados()

        self.assertIsInstance(carregados[1], Notebook)
        self.assertIsInstance(carregados[2], Servidor)
        self.assertIsInstance(carregados[3], Roteador)
        self.assertIsInstance(carregados[4], Impressora)

    def test_recarrega_atributos_proprios_de_cada_tipo(self):
        salvar_dados(criar_um_ativo_de_cada_tipo())
        carregados = carregar_dados()

        self.assertEqual(carregados[1].sistema_operacional, "Linux")
        self.assertEqual(carregados[2].ram, 32)
        self.assertEqual(carregados[3].portas, 8)
        self.assertEqual(carregados[4].tecnologia, Tecnologia.LASER)

    def test_vinculos_sao_gravados_so_com_o_id(self):
        ativos = criar_um_ativo_de_cada_tipo()
        ativos[2].vulnerabilidades[1] = StatusDaVuln.ABERTA
        salvar_dados(ativos)

        with open(self.arquivo_dados, encoding="utf-8") as arquivo:
            dados_brutos = json.load(arquivo)

        vinculo = dados_brutos[1]["vulnerabilidades"][0]
        self.assertEqual(vinculo, {"id_vulnerabilidade": 1, "status_tratamento": 1})

    def test_vinculos_apontam_para_vulnerabilidades_do_catalogo(self):
        catalogo = {
            1: Vulnerabilidade(1, "SSH com senha fraca", 7.5),
            2: Vulnerabilidade(2, "Firmware desatualizado", 9.1),
        }
        ativos = criar_um_ativo_de_cada_tipo()
        ativos[2].vulnerabilidades[1] = StatusDaVuln.ABERTA
        ativos[3].vulnerabilidades[1] = StatusDaVuln.EM_TRATAMENTO
        ativos[3].vulnerabilidades[2] = StatusDaVuln.CORRIGIDA

        salvar_catalogo(catalogo)
        salvar_dados(ativos)

        catalogo_carregado = carregar_catalogo()
        ativos_carregados = carregar_dados()

        for ativo in ativos_carregados.values():
            for id_vulnerabilidade in ativo.vulnerabilidades:
                self.assertIn(id_vulnerabilidade, catalogo_carregado)

        self.assertEqual(
            ativos_carregados[3].vulnerabilidades,
            {1: StatusDaVuln.EM_TRATAMENTO, 2: StatusDaVuln.CORRIGIDA},
        )