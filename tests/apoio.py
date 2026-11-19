import os
import unittest
from unittest.mock import patch

from inventario.dominio.ativo import Notebook, Servidor
from inventario.dominio.enums import Setor, StatusDaVuln, StatusDoAtivo
from inventario.dominio.excecoes import PersistenciaError
from inventario.persistencia import arquivos_json
from inventario.persistencia.arquivos_json import RepositorioJSON
from inventario.persistencia.banco_sqlite import RepositorioSQLite
from inventario.servicos.ativos import registrar_ativo_no_inventario
from inventario.servicos.dependencias import cadastrar_dependencia
from inventario.servicos.vulnerabilidades import (
    registrar_vulnerabilidade_no_catalogo,
    vincular_vulnerabilidade,
)


class TesteComArquivosTemporarios(unittest.TestCase):

    arquivo_dados = "teste_ativos_tmp.json"
    arquivo_catalogo = "teste_catalogo_tmp.json"

    def setUp(self):
        self.originais = (arquivos_json.ARQUIVO_ATIVOS, arquivos_json.ARQUIVO_CATALOGO)
        arquivos_json.ARQUIVO_ATIVOS = self.arquivo_dados
        arquivos_json.ARQUIVO_CATALOGO = self.arquivo_catalogo
        self.repositorio = RepositorioJSON()

    def tearDown(self):
        for arquivo in (self.arquivo_dados, self.arquivo_catalogo):
            if os.path.exists(arquivo):
                os.remove(arquivo)
        arquivos_json.ARQUIVO_ATIVOS, arquivos_json.ARQUIVO_CATALOGO = self.originais


def estado_em_dicionarios(ativos, catalogo):
    ativos_em_dicionario = {}
    for id_ativo, ativo in ativos.items():
        ativos_em_dicionario[id_ativo] = ativo.para_dicionario()

    catalogo_em_dicionario = {}
    for id_vulnerabilidade, vulnerabilidade in catalogo.items():
        catalogo_em_dicionario[id_vulnerabilidade] = vulnerabilidade.para_dicionario()

    return {"ativos": ativos_em_dicionario, "catalogo": catalogo_em_dicionario}


def criar_notebook_do_rafael(id_ativo):
    return Notebook(
        id_ativo,
        "Notebook do Rafael",
        Setor.TI,
        "Rafael Torres",
        StatusDoAtivo.ATIVO,
        "Linux",
        14.0,
    )


def criar_servidor_do_rafael(id_ativo):
    return Servidor(
        id_ativo,
        "Servidor do Rafael",
        Setor.TI,
        "Rafael Torres",
        StatusDoAtivo.ATIVO,
        32,
        4.0,
    )


class TesteComInventarioGravado(unittest.TestCase):

    def setUp(self):
        self.repositorio = RepositorioSQLite(":memory:")
        self.ativos = {}
        self.catalogo = {}
        registrar_ativo_no_inventario(self.repositorio, self.ativos, criar_notebook_do_rafael(1))
        registrar_ativo_no_inventario(self.repositorio, self.ativos, criar_servidor_do_rafael(2))
        registrar_vulnerabilidade_no_catalogo(self.repositorio, self.catalogo, "Log4Shell", 10)
        vincular_vulnerabilidade(
            self.repositorio, self.ativos, self.catalogo, 1, 1, StatusDaVuln.ABERTA
        )
        cadastrar_dependencia(self.repositorio, self.ativos, 1, 2, 0.3)
        self.estado_antes = self.estado_da_memoria()
        self.assertEqual(self.estado_do_banco(), self.estado_antes)

    def tearDown(self):
        self.repositorio.conexao.close()

    def estado_da_memoria(self):
        return estado_em_dicionarios(self.ativos, self.catalogo)

    def estado_do_banco(self):
        return estado_em_dicionarios(
            self.repositorio.carregar_ativos(), self.repositorio.carregar_catalogo()
        )

    def banco_falhando_em(self, nome_da_operacao):
        falha_do_banco = PersistenciaError("Não foi possível gravar no banco de dados.")
        return patch.object(self.repositorio, nome_da_operacao, side_effect=falha_do_banco)

    def conferir_memoria_e_banco_sem_alteracao(self):
        self.assertEqual(self.estado_da_memoria(), self.estado_antes)
        self.assertEqual(self.estado_do_banco(), self.estado_antes)
