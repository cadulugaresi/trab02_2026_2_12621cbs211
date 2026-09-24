import unittest
from funcoes_s1 import (
    Ativo, Vulnerabilidade,
    Categorias, Setor, StatusDoAtivo,
    NivelDaVulnerabilidade, StatusDaVuln,
    encontrar_ativo_por_id, encontrar_ativo_por_nome,
    validar_nome_responsavel,
    validar_status, validar_setor, validar_categoria,
    encontrar_ativos_por_categ, encontrar_ativos_por_status,
    DadoInvalidoError,
)

class TestAtivo(unittest.TestCase):
    def test_criar(self):
        a = Ativo(1, 'macbook', Categorias.NOTEBOOK, Setor.TI, 'cadu', StatusDoAtivo.ATIVO)
        self.assertEqual(a.id, 1)
        self.assertEqual(a.nome, 'macbook')
        self.assertEqual(a.vulnerabilidades, [])

    def test_para_dicionario(self):
        a = Ativo(1, 'macbook', Categorias.NOTEBOOK, Setor.TI, 'cadu', StatusDoAtivo.ATIVO)
        d = a.para_dicionario()
        self.assertEqual(d['id'], 1)
        self.assertEqual(d['categoria'], 1)
        self.assertEqual(d['setor'], 1)

class TestVulnerabilidade(unittest.TestCase):
    def test_criar(self):
        v = Vulnerabilidade('senha fraca', 'senha', NivelDaVulnerabilidade.ALTO, StatusDaVuln.ABERTA)
        self.assertEqual(v.nome_vulnerabilidade, 'senha fraca')
        self.assertEqual(v.tipo, 'senha')
        self.assertEqual(v.nivel, NivelDaVulnerabilidade.ALTO)

    def test_para_dicionario(self):
        v = Vulnerabilidade('senha fraca', 'senha', NivelDaVulnerabilidade.ALTO, StatusDaVuln.ABERTA)
        d = v.para_dicionario()
        self.assertEqual(d['tipo'], 'senha')
        self.assertEqual(d['nivel'], 3)

class TestValidacoes(unittest.TestCase):
    def test_nome_vazio(self):
        with self.assertRaises(DadoInvalidoError):
            validar_nome_responsavel('')

    def test_nome_so_numeros(self):
        with self.assertRaises(DadoInvalidoError):
            validar_nome_responsavel('123')

    def test_nome_valido(self):
        validar_nome_responsavel('cadu')

class TestValidacoesDeEnum(unittest.TestCase):
    def test_validar_status_valido(self):
        self.assertEqual(validar_status('1'), StatusDoAtivo.ATIVO)
        self.assertEqual(validar_status('2'), StatusDoAtivo.INATIVO)
        self.assertEqual(validar_status('3'), StatusDoAtivo.EM_MANUTENCAO)

    def test_validar_status_invalido(self):
        with self.assertRaises(DadoInvalidoError):
            validar_status('99')
        with self.assertRaises(DadoInvalidoError):
            validar_status('')

    def test_validar_setor_valido(self):
        self.assertEqual(validar_setor('1'), Setor.TI)
        self.assertEqual(validar_setor('5'), Setor.JURIDICO)

    def test_validar_setor_invalido(self):
        with self.assertRaises(DadoInvalidoError):
            validar_setor('0')
        with self.assertRaises(DadoInvalidoError):
            validar_setor('6')

    def test_validar_categoria_valida(self):
        self.assertEqual(validar_categoria('1'), Categorias.NOTEBOOK)
        self.assertEqual(validar_categoria('4'), Categorias.IMPRESSORA)

    def test_validar_categoria_invalida(self):
        with self.assertRaises(DadoInvalidoError):
            validar_categoria('0')
        with self.assertRaises(DadoInvalidoError):
            validar_categoria('5')

class TestBusca(unittest.TestCase):
    def setUp(self):
        self.ativos = {
            1: Ativo(1, 'macbook', Categorias.NOTEBOOK, Setor.TI, 'cadu', StatusDoAtivo.ATIVO),
            2: Ativo(2, 'mac-mini', Categorias.SERVIDOR, Setor.TI, 'cadu', StatusDoAtivo.ATIVO),
            3: Ativo(3, 'imac', Categorias.NOTEBOOK, Setor.TI, 'cadu', StatusDoAtivo.ATIVO),
        }

    def test_busca_id_existente(self):
        self.assertIsNotNone(encontrar_ativo_por_id(1, self.ativos))

    def test_busca_id_inexistente(self):
        self.assertIsNone(encontrar_ativo_por_id(999, self.ativos))

    def test_busca_nome_parcial(self):
        self.assertEqual(len(encontrar_ativo_por_nome('mac', self.ativos)), 3)

    def test_busca_nome_case_insensitive(self):
        self.assertEqual(len(encontrar_ativo_por_nome('MAC', self.ativos)), 3)

    def test_busca_nome_sem_match(self):
        self.assertEqual(encontrar_ativo_por_nome('xyz', self.ativos), [])

if __name__ == '__main__':
    unittest.main()

class TestCadastroDuplicado(unittest.TestCase):
    def test_id_duplicado_sobrescreve(self):
        """Simula comportamento de ID duplicado no dicionário."""
        ativos = {}
        a1 = Ativo(1, 'macbook', Categorias.NOTEBOOK, Setor.TI, 'cadu', StatusDoAtivo.ATIVO)
        a2 = Ativo(1, 'outro', Categorias.SERVIDOR, Setor.RH, 'joao', StatusDoAtivo.INATIVO)
        ativos[1] = a1
        ativos[1] = a2
        self.assertEqual(len(ativos), 1)
        self.assertEqual(ativos[1].nome, 'outro')

class TestFiltros(unittest.TestCase):
    """Testes para encontrar_ativos_por_categ e encontrar_ativos_por_status (S2_09)."""

    def setUp(self):
        """Cria um dicionário de ativos pra usar em cada teste."""
        self.ativos = {
            1: Ativo(1, 'macbook', Categorias.NOTEBOOK, Setor.TI, 'cadu', StatusDoAtivo.ATIVO),
            2: Ativo(2, 'srv-db', Categorias.SERVIDOR, Setor.TI, 'cadu', StatusDoAtivo.ATIVO),
            3: Ativo(3, 'impressora-1', Categorias.IMPRESSORA, Setor.RH, 'joao', StatusDoAtivo.INATIVO),
            4: Ativo(4, 'notebook-rh', Categorias.NOTEBOOK, Setor.RH, 'joao', StatusDoAtivo.EM_MANUTENCAO),
        }

    def test_encontrar_ativos_por_categ_com_resultado(self):
        resultado = encontrar_ativos_por_categ(Categorias.NOTEBOOK, self.ativos)
        self.assertEqual(len(resultado), 2)

    def test_encontrar_ativos_por_categ_sem_resultado(self):
        resultado = encontrar_ativos_por_categ(Categorias.ROTEADOR, self.ativos)
        self.assertEqual(resultado, [])

    def test_encontrar_ativos_por_categ_dicionario_vazio(self):
        resultado = encontrar_ativos_por_categ(Categorias.NOTEBOOK, {})
        self.assertEqual(resultado, [])

    def test_encontrar_ativos_por_status_com_resultado(self):
        resultado = encontrar_ativos_por_status(StatusDoAtivo.ATIVO, self.ativos)
        self.assertEqual(len(resultado), 2)

    def test_encontrar_ativos_por_status_sem_resultado(self):
        resultado = encontrar_ativos_por_status(StatusDoAtivo.INATIVO, self.ativos)
        self.assertEqual(len(resultado), 1)

    def test_encontrar_ativos_por_status_dicionario_vazio(self):
        resultado = encontrar_ativos_por_status(StatusDoAtivo.ATIVO, {})
        self.assertEqual(resultado, [])

class TestAtualizacao(unittest.TestCase):
    def test_alteracao_muda_estado(self):
        a = Ativo(1, 'macbook', Categorias.NOTEBOOK, Setor.TI, 'cadu', StatusDoAtivo.ATIVO)
        antes = a.para_dicionario()
        a.responsavel = 'joao'
        depois = a.para_dicionario()
        self.assertNotEqual(antes, depois)

    def test_id_nao_muda(self):
        a = Ativo(1, 'macbook', Categorias.NOTEBOOK, Setor.TI, 'cadu', StatusDoAtivo.ATIVO)
        a.responsavel = 'joao'
        d = a.para_dicionario()
        self.assertEqual(d['id'], 1)

    def test_sem_alteracao_estados_iguais(self):
        a = Ativo(1, 'macbook', Categorias.NOTEBOOK, Setor.TI, 'cadu', StatusDoAtivo.ATIVO)
        self.assertEqual(a.para_dicionario(), a.para_dicionario())