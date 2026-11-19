import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from inventario.dominio.enums import StatusDaVuln
from inventario.dominio.excecoes import PersistenciaError
from inventario.dominio.vulnerabilidade import Vulnerabilidade
from inventario.interface.ativos import editar_ativo
from inventario.interface.vulnerabilidades import editar_vulnerabilidade
from inventario.servicos.ativos import (
    atualizar_ativo_no_inventario,
    registrar_ativo_no_inventario,
    remover_ativo_do_inventario,
)
from inventario.servicos.dependencias import (
    atualizar_dependencia,
    cadastrar_dependencia,
    remover_dependencia,
)
from inventario.servicos.vulnerabilidades import (
    atualizar_status_vulnerabilidade,
    atualizar_vulnerabilidade_no_catalogo,
    desvincular_vulnerabilidade,
    excluir_vulnerabilidade_do_catalogo,
    registrar_vulnerabilidade_no_catalogo,
    vincular_vulnerabilidade,
)
from tests.apoio import TesteComInventarioGravado, criar_notebook_do_rafael


class TesteDosServicosDeAtivoComFalhaNoBanco(TesteComInventarioGravado):

    def test_registrar_ativo(self):
        with self.banco_falhando_em("adicionar_ativo"):
            with self.assertRaises(PersistenciaError):
                registrar_ativo_no_inventario(
                    self.repositorio, self.ativos, criar_notebook_do_rafael(3)
                )

        self.conferir_memoria_e_banco_sem_alteracao()

    def test_atualizar_ativo(self):
        notebook_com_tela_nova = criar_notebook_do_rafael(1)
        notebook_com_tela_nova.tela = 15.6

        with self.banco_falhando_em("atualizar_ativo"):
            with self.assertRaises(PersistenciaError):
                atualizar_ativo_no_inventario(self.repositorio, self.ativos, notebook_com_tela_nova)

        self.conferir_memoria_e_banco_sem_alteracao()

    def test_remover_ativo(self):
        with self.banco_falhando_em("remover_ativo"):
            with self.assertRaises(PersistenciaError):
                remover_ativo_do_inventario(self.repositorio, self.ativos, 2)

        self.conferir_memoria_e_banco_sem_alteracao()


class TesteDosServicosDeVulnerabilidadeComFalhaNoBanco(TesteComInventarioGravado):

    def test_registrar_vulnerabilidade(self):
        with self.banco_falhando_em("adicionar_vulnerabilidade"):
            with self.assertRaises(PersistenciaError):
                registrar_vulnerabilidade_no_catalogo(
                    self.repositorio, self.catalogo, "Heartbleed", 7.5
                )

        self.conferir_memoria_e_banco_sem_alteracao()

    def test_vincular_vulnerabilidade(self):
        with self.banco_falhando_em("vincular"):
            with self.assertRaises(PersistenciaError):
                vincular_vulnerabilidade(
                    self.repositorio, self.ativos, self.catalogo, 2, 1, StatusDaVuln.ABERTA
                )

        self.conferir_memoria_e_banco_sem_alteracao()

    def test_desvincular_vulnerabilidade(self):
        with self.banco_falhando_em("desvincular"):
            with self.assertRaises(PersistenciaError):
                desvincular_vulnerabilidade(self.repositorio, self.ativos, 1, 1)

        self.conferir_memoria_e_banco_sem_alteracao()

    def test_atualizar_status_da_vulnerabilidade(self):
        with self.banco_falhando_em("atualizar_status_vinculo"):
            with self.assertRaises(PersistenciaError):
                atualizar_status_vulnerabilidade(
                    self.repositorio, self.ativos, 1, 1, StatusDaVuln.CORRIGIDA
                )

        self.conferir_memoria_e_banco_sem_alteracao()

    def test_excluir_vulnerabilidade_do_catalogo(self):
        with self.banco_falhando_em("remover_vulnerabilidade"):
            with self.assertRaises(PersistenciaError):
                excluir_vulnerabilidade_do_catalogo(self.repositorio, self.catalogo, self.ativos, 1)

        self.conferir_memoria_e_banco_sem_alteracao()

    def test_atualizar_vulnerabilidade_no_catalogo(self):
        log4shell_com_nota_nova = Vulnerabilidade(1, "Log4Shell", 9.0)

        with self.banco_falhando_em("atualizar_vulnerabilidade"):
            with self.assertRaises(PersistenciaError):
                atualizar_vulnerabilidade_no_catalogo(
                    self.repositorio, self.catalogo, log4shell_com_nota_nova
                )

        self.conferir_memoria_e_banco_sem_alteracao()


class TesteDosServicosDeDependenciaComFalhaNoBanco(TesteComInventarioGravado):

    def test_cadastrar_dependencia(self):
        with self.banco_falhando_em("adicionar_dependencia"):
            with self.assertRaises(PersistenciaError):
                cadastrar_dependencia(self.repositorio, self.ativos, 2, 1, 0.2)

        self.conferir_memoria_e_banco_sem_alteracao()

    def test_remover_dependencia(self):
        with self.banco_falhando_em("remover_dependencia"):
            with self.assertRaises(PersistenciaError):
                remover_dependencia(self.repositorio, self.ativos, 1, 2)

        self.conferir_memoria_e_banco_sem_alteracao()

    def test_atualizar_dependencia(self):
        with self.banco_falhando_em("atualizar_dependencia"):
            with self.assertRaises(PersistenciaError):
                atualizar_dependencia(self.repositorio, self.ativos, 1, 2, 2, 0.5)

        self.conferir_memoria_e_banco_sem_alteracao()


class TesteDasTelasDeEdicaoComFalhaNoBanco(TesteComInventarioGravado):

    def test_editar_ativo_no_menu(self):
        respostas = ["1", "2", "3", "7"]

        with self.banco_falhando_em("atualizar_ativo"):
            with patch("builtins.input", side_effect=respostas):
                with redirect_stdout(io.StringIO()):
                    with self.assertRaises(PersistenciaError):
                        editar_ativo(self.repositorio, self.ativos)

        self.conferir_memoria_e_banco_sem_alteracao()

    def test_editar_vulnerabilidade_no_menu(self):
        respostas = ["2", "9"]

        with self.banco_falhando_em("atualizar_vulnerabilidade"):
            with patch("builtins.input", side_effect=respostas):
                with redirect_stdout(io.StringIO()):
                    with self.assertRaises(PersistenciaError):
                        editar_vulnerabilidade(self.repositorio, self.catalogo[1], self.catalogo)

        self.conferir_memoria_e_banco_sem_alteracao()


if __name__ == "__main__":
    unittest.main()
