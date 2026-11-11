import unittest

import numpy as np

from inventario.dominio.ativo import Notebook, Roteador, Servidor
from inventario.dominio.enums import Setor, StatusDaVuln, StatusDoAtivo
from inventario.dominio.vulnerabilidade import Vulnerabilidade
from inventario.servicos.riscos import (
    calcular_risco_proprio,
    mapear_ids_para_posicoes,
    montar_matriz_m,
    montar_vetor_cvss,
    montar_vetor_fator,
)


def criar_notebook(id_do_ativo=1, fator_exposicao=None):
    return Notebook(
        id_do_ativo,
        "Dell",
        Setor.TI,
        "Rafael Torres",
        StatusDoAtivo.ATIVO,
        "Linux",
        15.6,
        fator_exposicao,
    )


def criar_servidor(id_do_ativo=2):
    return Servidor(id_do_ativo, "PowerEdge", Setor.TI, "Rafael Torres", StatusDoAtivo.ATIVO, 32, 4)


def criar_roteador(id_do_ativo=3):
    return Roteador(id_do_ativo, "Cisco", Setor.TI, "Rafael Torres", StatusDoAtivo.ATIVO, 24, 1000)


def criar_catalogo():
    return {
        1: Vulnerabilidade(1, "Senha padrão do fabricante", 9.8),
        2: Vulnerabilidade(2, "Sistema operacional desatualizado", 7.5),
        3: Vulnerabilidade(3, "Compartilhamento de arquivos sem criptografia", 5.3),
    }


def vincular_vulnerabilidades_do_cenario(notebook, servidor, roteador):
    notebook.vulnerabilidades[2] = StatusDaVuln.EM_TRATAMENTO
    servidor.vulnerabilidades[3] = StatusDaVuln.ABERTA
    servidor.vulnerabilidades[2] = StatusDaVuln.CORRIGIDA
    roteador.vulnerabilidades[1] = StatusDaVuln.ABERTA


class TesteComCenarioDeRisco(unittest.TestCase):

    def setUp(self):
        self.catalogo = criar_catalogo()
        self.notebook = criar_notebook()
        self.servidor = criar_servidor()
        self.roteador = criar_roteador()
        vincular_vulnerabilidades_do_cenario(self.notebook, self.servidor, self.roteador)
        self.ativos = {1: self.notebook, 2: self.servidor, 3: self.roteador}
        self.posicoes_dos_ativos = mapear_ids_para_posicoes(self.ativos)
        self.posicoes_das_vulns = mapear_ids_para_posicoes(self.catalogo)

    def montar_matriz_do_cenario(self):
        return montar_matriz_m(
            self.ativos, self.catalogo, self.posicoes_dos_ativos, self.posicoes_das_vulns
        )


class TestMapearIdsParaPosicoes(unittest.TestCase):

    def test_ordena_os_ids_e_aceita_buracos(self):
        dicionario_com_buracos = {300: "Rafael Torres", 5: "Rafael Torres", 12: "Rafael Torres"}

        posicoes = mapear_ids_para_posicoes(dicionario_com_buracos)

        self.assertEqual(posicoes, {5: 0, 12: 1, 300: 2})


class TestMontarMatrizM(TesteComCenarioDeRisco):

    def test_cenario_principal_gera_a_matriz_esperada(self):
        matriz_esperada = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]])

        np.testing.assert_array_equal(self.montar_matriz_do_cenario(), matriz_esperada)

    def test_vulnerabilidade_corrigida_nao_entra_na_matriz(self):
        matriz_m = self.montar_matriz_do_cenario()

        linha_do_servidor = self.posicoes_dos_ativos[2]
        coluna_da_vuln_corrigida = self.posicoes_das_vulns[2]
        self.assertEqual(matriz_m[linha_do_servidor, coluna_da_vuln_corrigida], 0)

    def test_vulnerabilidade_aceita_entra_como_1_na_matriz(self):
        self.notebook.vulnerabilidades[1] = StatusDaVuln.ACEITA

        matriz_m = self.montar_matriz_do_cenario()

        linha_do_notebook = self.posicoes_dos_ativos[1]
        coluna_da_vuln_aceita = self.posicoes_das_vulns[1]
        self.assertEqual(matriz_m[linha_do_notebook, coluna_da_vuln_aceita], 1)


class TestMontarVetorCvss(TesteComCenarioDeRisco):

    def test_vetor_tem_o_cvss_de_cada_vulnerabilidade_em_ordem_de_id(self):
        vetor_cvss = montar_vetor_cvss(self.catalogo, self.posicoes_das_vulns)

        np.testing.assert_allclose(vetor_cvss, [9.8, 7.5, 5.3])


class TestMontarVetorFator(TesteComCenarioDeRisco):

    def test_usa_o_fator_padrao_de_cada_tipo_de_ativo(self):
        vetor_fator = montar_vetor_fator(self.ativos, self.posicoes_dos_ativos)

        fatores_esperados = [
            Notebook.FATOR_EXPOSICAO_PADRAO,
            Servidor.FATOR_EXPOSICAO_PADRAO,
            Roteador.FATOR_EXPOSICAO_PADRAO,
        ]
        np.testing.assert_allclose(vetor_fator, fatores_esperados)

    def test_usa_o_fator_do_proprio_ativo_quando_difere_do_padrao(self):
        notebook_mais_exposto = criar_notebook(1, fator_exposicao=2.0)
        self.ativos[1] = notebook_mais_exposto

        vetor_fator = montar_vetor_fator(self.ativos, self.posicoes_dos_ativos)

        fatores_esperados = [
            2.0,
            Servidor.FATOR_EXPOSICAO_PADRAO,
            Roteador.FATOR_EXPOSICAO_PADRAO,
        ]
        np.testing.assert_allclose(vetor_fator, fatores_esperados)


class TestCalcularRiscoProprio(TesteComCenarioDeRisco):

    def test_cenario_principal_gera_o_risco_esperado(self):
        risco_proprio = calcular_risco_proprio(self.ativos, self.catalogo)

        np.testing.assert_allclose(risco_proprio, [9.0, 6.89, 14.7])

    def test_continua_certo_com_buracos_nos_ids_dos_ativos(self):
        notebook = criar_notebook(5)
        servidor = criar_servidor(12)
        roteador = criar_roteador(300)
        vincular_vulnerabilidades_do_cenario(notebook, servidor, roteador)
        ativos_com_buracos = {300: roteador, 5: notebook, 12: servidor}

        risco_proprio = calcular_risco_proprio(ativos_com_buracos, self.catalogo)

        np.testing.assert_allclose(risco_proprio, [9.0, 6.89, 14.7])


if __name__ == "__main__":
    unittest.main()
