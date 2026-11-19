import unittest

from inventario.dominio.enums import StatusDaVuln
from inventario.dominio.excecoes import DadoInvalidoError, RecursoNaoEncontradoError
from inventario.dominio.vulnerabilidade import Vulnerabilidade
from inventario.servicos.ativos import (
    atualizar_ativo_no_inventario,
    obter_ativo,
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
    obter_vulnerabilidade,
    vincular_vulnerabilidade,
)
from tests.apoio import TesteComInventarioGravado, criar_notebook_do_rafael

MENSAGEM_DE_ATIVO_NAO_ENCONTRADO = "Ativo não encontrado."
MENSAGEM_DE_VULNERABILIDADE_NAO_ENCONTRADA = "Vulnerabilidade não encontrada no catálogo."


class TesteDaExcecaoDeRecursoNaoEncontrado(unittest.TestCase):

    def test_e_um_dado_invalido_para_o_menu_continuar_capturando(self):
        self.assertTrue(issubclass(RecursoNaoEncontradoError, DadoInvalidoError))


class TesteDosServicosComRecursoNaoEncontrado(TesteComInventarioGravado):

    def conferir_recurso_nao_encontrado(self, operacao, mensagem_esperada):
        with self.assertRaises(RecursoNaoEncontradoError) as contexto:
            operacao()

        self.assertEqual(str(contexto.exception), mensagem_esperada)
        self.conferir_memoria_e_banco_sem_alteracao()

    def test_obter_ativo_inexistente(self):
        self.conferir_recurso_nao_encontrado(
            lambda: obter_ativo(self.ativos, 99), MENSAGEM_DE_ATIVO_NAO_ENCONTRADO
        )

    def test_atualizar_ativo_inexistente(self):
        self.conferir_recurso_nao_encontrado(
            lambda: atualizar_ativo_no_inventario(
                self.repositorio, self.ativos, criar_notebook_do_rafael(99)
            ),
            MENSAGEM_DE_ATIVO_NAO_ENCONTRADO,
        )

    def test_remover_ativo_inexistente(self):
        self.conferir_recurso_nao_encontrado(
            lambda: remover_ativo_do_inventario(self.repositorio, self.ativos, 99),
            MENSAGEM_DE_ATIVO_NAO_ENCONTRADO,
        )

    def test_obter_vulnerabilidade_inexistente(self):
        self.conferir_recurso_nao_encontrado(
            lambda: obter_vulnerabilidade(self.catalogo, 99),
            MENSAGEM_DE_VULNERABILIDADE_NAO_ENCONTRADA,
        )

    def test_obter_vulnerabilidade_existente_devolve_a_do_catalogo(self):
        self.assertIs(obter_vulnerabilidade(self.catalogo, 1), self.catalogo[1])

    def test_vincular_a_ativo_inexistente(self):
        self.conferir_recurso_nao_encontrado(
            lambda: vincular_vulnerabilidade(
                self.repositorio, self.ativos, self.catalogo, 99, 1, StatusDaVuln.ABERTA
            ),
            MENSAGEM_DE_ATIVO_NAO_ENCONTRADO,
        )

    def test_vincular_vulnerabilidade_inexistente(self):
        self.conferir_recurso_nao_encontrado(
            lambda: vincular_vulnerabilidade(
                self.repositorio, self.ativos, self.catalogo, 2, 99, StatusDaVuln.ABERTA
            ),
            MENSAGEM_DE_VULNERABILIDADE_NAO_ENCONTRADA,
        )

    def test_desvincular_vinculo_inexistente(self):
        self.conferir_recurso_nao_encontrado(
            lambda: desvincular_vulnerabilidade(self.repositorio, self.ativos, 2, 1),
            "Esta vulnerabilidade não está vinculada a este ativo.",
        )

    def test_atualizar_status_de_vinculo_inexistente(self):
        self.conferir_recurso_nao_encontrado(
            lambda: atualizar_status_vulnerabilidade(
                self.repositorio, self.ativos, 2, 1, StatusDaVuln.CORRIGIDA
            ),
            "Este ativo não possui nenhuma vulnerabilidade com este ID vinculada a ele.",
        )

    def test_excluir_vulnerabilidade_inexistente(self):
        self.conferir_recurso_nao_encontrado(
            lambda: excluir_vulnerabilidade_do_catalogo(
                self.repositorio, self.catalogo, self.ativos, 99
            ),
            MENSAGEM_DE_VULNERABILIDADE_NAO_ENCONTRADA,
        )

    def test_atualizar_vulnerabilidade_inexistente(self):
        self.conferir_recurso_nao_encontrado(
            lambda: atualizar_vulnerabilidade_no_catalogo(
                self.repositorio, self.catalogo, Vulnerabilidade(99, "Heartbleed", 7.5)
            ),
            MENSAGEM_DE_VULNERABILIDADE_NAO_ENCONTRADA,
        )

    def test_cadastrar_dependencia_para_ativo_inexistente(self):
        self.conferir_recurso_nao_encontrado(
            lambda: cadastrar_dependencia(self.repositorio, self.ativos, 1, 99, 0.2),
            MENSAGEM_DE_ATIVO_NAO_ENCONTRADO,
        )

    def test_remover_dependencia_inexistente(self):
        self.conferir_recurso_nao_encontrado(
            lambda: remover_dependencia(self.repositorio, self.ativos, 2, 1),
            "Este ativo não possui essa dependência.",
        )

    def test_atualizar_dependencia_inexistente(self):
        self.conferir_recurso_nao_encontrado(
            lambda: atualizar_dependencia(self.repositorio, self.ativos, 2, 1, 1, 0.5),
            "Este ativo não possui essa dependência.",
        )


if __name__ == "__main__":
    unittest.main()
