import unittest

import numpy as np

from inventario.dominio.ativo import Notebook, Roteador, Servidor
from inventario.dominio.enums import Setor, StatusDaVuln, StatusDoAtivo
from inventario.dominio.excecoes import DadoInvalidoError
from inventario.dominio.vulnerabilidade import Vulnerabilidade
from inventario.servicos.riscos import (
    AnaliseDeRisco,
    calcular_risco_efetivo,
    calcular_risco_proprio,
    mapear_ids_para_posicoes,
    montar_matriz_a,
    montar_matriz_m,
    montar_vetor_cvss,
    montar_vetor_fator,
    resolver_sistema,
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


def vincular_dependencias_do_cenario(notebook, servidor):
    notebook.dependencias[2] = 0.5
    servidor.dependencias[3] = 0.2


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


class TestMontarMatrizA(TesteComCenarioDeRisco):

    def test_cenario_com_dependencias_gera_a_matriz_esperada(self):
        vincular_dependencias_do_cenario(self.notebook, self.servidor)

        matriz_a = montar_matriz_a(self.ativos, self.posicoes_dos_ativos)

        matriz_esperada = np.array([[0, 0.5, 0], [0, 0, 0.2], [0, 0, 0]])
        np.testing.assert_allclose(matriz_a, matriz_esperada)

    def test_ativos_sem_dependencias_geram_matriz_so_de_zeros(self):
        matriz_a = montar_matriz_a(self.ativos, self.posicoes_dos_ativos)

        np.testing.assert_array_equal(matriz_a, np.zeros((3, 3)))

    def test_respeita_a_traducao_de_ids_com_buracos(self):
        notebook = criar_notebook(5)
        servidor = criar_servidor(12)
        roteador = criar_roteador(300)
        roteador.dependencias[5] = 0.4
        ativos_com_buracos = {300: roteador, 5: notebook, 12: servidor}
        posicoes_com_buracos = mapear_ids_para_posicoes(ativos_com_buracos)

        matriz_a = montar_matriz_a(ativos_com_buracos, posicoes_com_buracos)

        matriz_esperada = np.array([[0, 0, 0], [0, 0, 0], [0.4, 0, 0]])
        np.testing.assert_allclose(matriz_a, matriz_esperada)


class TestCalcularRiscoEfetivo(TesteComCenarioDeRisco):

    def test_cenario_com_dependencias_gera_o_risco_esperado(self):
        vincular_dependencias_do_cenario(self.notebook, self.servidor)

        risco_efetivo = calcular_risco_efetivo(self.ativos, self.catalogo)

        np.testing.assert_allclose(risco_efetivo, [13.915, 9.83, 14.7])

    def test_sem_dependencias_o_risco_efetivo_e_igual_ao_risco_proprio(self):
        risco_efetivo = calcular_risco_efetivo(self.ativos, self.catalogo)
        risco_proprio = calcular_risco_proprio(self.ativos, self.catalogo)

        np.testing.assert_allclose(risco_efetivo, risco_proprio)

    def test_roteador_sem_dependencias_tem_risco_efetivo_igual_ao_proprio(self):
        vincular_dependencias_do_cenario(self.notebook, self.servidor)
        linha_do_roteador = self.posicoes_dos_ativos[3]

        risco_efetivo = calcular_risco_efetivo(self.ativos, self.catalogo)
        risco_proprio = calcular_risco_proprio(self.ativos, self.catalogo)

        np.testing.assert_allclose(
            risco_efetivo[linha_do_roteador], risco_proprio[linha_do_roteador]
        )

    def test_dependencia_circular_com_fracao_total_levanta_erro(self):
        self.notebook.dependencias[2] = 1.0
        self.servidor.dependencias[1] = 1.0
        ativos_em_ciclo = {1: self.notebook, 2: self.servidor}

        with self.assertRaises(DadoInvalidoError):
            calcular_risco_efetivo(ativos_em_ciclo, self.catalogo)


class TestResolverSistema(unittest.TestCase):

    def test_matriz_com_dependencias_gera_o_risco_efetivo_esperado(self):
        matriz_a = np.array([[0, 0.5, 0], [0, 0, 0.2], [0, 0, 0]])
        risco_proprio = np.array([23.0, 15.8, 17.0])

        risco_efetivo = resolver_sistema(matriz_a, risco_proprio)

        np.testing.assert_allclose(risco_efetivo, [32.6, 19.2, 17.0])

    def test_matriz_so_de_zeros_devolve_o_proprio_risco_proprio(self):
        matriz_a = np.zeros((3, 3))
        risco_proprio = np.array([23.0, 15.8, 17.0])

        risco_efetivo = resolver_sistema(matriz_a, risco_proprio)

        np.testing.assert_allclose(risco_efetivo, risco_proprio)

    def test_dependencia_circular_com_fracao_total_levanta_erro(self):
        matriz_a = np.array([[0, 1.0], [1.0, 0]])
        risco_proprio = np.array([23.0, 15.8])

        with self.assertRaises(DadoInvalidoError):
            resolver_sistema(matriz_a, risco_proprio)


class TestAnaliseDeRisco(TesteComCenarioDeRisco):

    def criar_analise_com_dependencias_do_cenario(self):
        vincular_dependencias_do_cenario(self.notebook, self.servidor)
        return AnaliseDeRisco(self.ativos, self.catalogo)

    def test_risco_proprio_do_ativo_devolve_o_valor_de_cada_id(self):
        analise = self.criar_analise_com_dependencias_do_cenario()
        risco_proprio_esperado_por_id = {1: 9.0, 2: 6.89, 3: 14.7}

        for id_ativo, risco_esperado in risco_proprio_esperado_por_id.items():
            self.assertAlmostEqual(analise.risco_proprio_do_ativo(id_ativo), risco_esperado)

    def test_risco_efetivo_do_ativo_devolve_o_valor_de_cada_id(self):
        analise = self.criar_analise_com_dependencias_do_cenario()
        risco_efetivo_esperado_por_id = {1: 13.915, 2: 9.83, 3: 14.7}

        for id_ativo, risco_esperado in risco_efetivo_esperado_por_id.items():
            self.assertAlmostEqual(analise.risco_efetivo_do_ativo(id_ativo), risco_esperado)

    def test_risco_herdado_do_ativo_devolve_o_valor_de_cada_id(self):
        analise = self.criar_analise_com_dependencias_do_cenario()
        risco_herdado_esperado_por_id = {1: 4.915, 2: 2.94, 3: 0}

        for id_ativo, risco_esperado in risco_herdado_esperado_por_id.items():
            self.assertAlmostEqual(analise.risco_herdado_do_ativo(id_ativo), risco_esperado)

    def test_ranking_ordena_do_maior_para_o_menor_risco_efetivo(self):
        analise = self.criar_analise_com_dependencias_do_cenario()

        self.assertEqual(analise.ranking(), [3, 1, 2])

    def test_ranking_usa_o_risco_efetivo_e_nao_o_risco_proprio(self):
        self.servidor.dependencias[3] = 0.9

        analise = AnaliseDeRisco(self.ativos, self.catalogo)

        np.testing.assert_allclose(analise.risco_efetivo, [9.0, 20.12, 14.7])
        self.assertEqual(analise.ranking(), [2, 3, 1])

    def test_funciona_com_buracos_nos_ids_dos_ativos(self):
        notebook = criar_notebook(5)
        servidor = criar_servidor(12)
        roteador = criar_roteador(300)
        vincular_vulnerabilidades_do_cenario(notebook, servidor, roteador)
        notebook.dependencias[12] = 0.5
        servidor.dependencias[300] = 0.2
        ativos_com_buracos = {300: roteador, 5: notebook, 12: servidor}

        analise = AnaliseDeRisco(ativos_com_buracos, self.catalogo)

        risco_proprio_esperado_por_id = {5: 9.0, 12: 6.89, 300: 14.7}
        risco_efetivo_esperado_por_id = {5: 13.915, 12: 9.83, 300: 14.7}
        for id_ativo, risco_esperado in risco_proprio_esperado_por_id.items():
            self.assertAlmostEqual(analise.risco_proprio_do_ativo(id_ativo), risco_esperado)
        for id_ativo, risco_esperado in risco_efetivo_esperado_por_id.items():
            self.assertAlmostEqual(analise.risco_efetivo_do_ativo(id_ativo), risco_esperado)
        self.assertEqual(analise.ranking(), [300, 5, 12])

    def test_dependencia_circular_com_fracao_total_levanta_erro_ao_criar(self):
        self.notebook.dependencias[2] = 1.0
        self.servidor.dependencias[1] = 1.0
        ativos_em_ciclo = {1: self.notebook, 2: self.servidor}

        with self.assertRaises(DadoInvalidoError):
            AnaliseDeRisco(ativos_em_ciclo, self.catalogo)


if __name__ == "__main__":
    unittest.main()
