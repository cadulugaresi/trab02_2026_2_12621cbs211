from inventario.dominio.ativo import Notebook, Servidor
from inventario.dominio.enums import Setor, StatusDaVuln, StatusDoAtivo
from inventario.dominio.vulnerabilidade import Vulnerabilidade


def criar_notebook():
    return Notebook(
        1, "Notebook da Recepção", Setor.TI, "Rafael Torres", StatusDoAtivo.ATIVO, "Linux", 15.6
    )


def criar_servidor():
    return Servidor(
        2, "Servidor de Arquivos", Setor.FINANCEIRO, "Rafael Torres", StatusDoAtivo.ATIVO, 32, 4
    )


def criar_senha_fraca():
    return Vulnerabilidade(1, "SSH com senha fraca", 7.5)


def criar_firmware_desatualizado():
    return Vulnerabilidade(2, "Firmware desatualizado", 9.1)


class ContratoDoRepositorio:

    def criar_repositorio(self):
        raise NotImplementedError

    def setUp(self):
        super().setUp()
        self.repositorio = self.criar_repositorio()

    def recarregar_ativos(self):
        return self.criar_repositorio().carregar_ativos()

    def recarregar_catalogo(self):
        return self.criar_repositorio().carregar_catalogo()

    def preparar_dois_ativos_com_vinculos(self):
        self.repositorio.adicionar_ativo(criar_notebook())
        self.repositorio.adicionar_ativo(criar_servidor())
        self.repositorio.adicionar_vulnerabilidade(criar_senha_fraca())
        self.repositorio.adicionar_vulnerabilidade(criar_firmware_desatualizado())
        self.repositorio.vincular(1, 1, StatusDaVuln.ABERTA)
        self.repositorio.vincular(1, 2, StatusDaVuln.EM_TRATAMENTO)
        self.repositorio.vincular(2, 1, StatusDaVuln.ACEITA)

    def test_carregar_ativos_sem_dados_devolve_vazio(self):
        self.assertEqual(self.repositorio.carregar_ativos(), {})

    def test_carregar_catalogo_sem_dados_devolve_vazio(self):
        self.assertEqual(self.repositorio.carregar_catalogo(), {})

    def test_adicionar_ativo_grava_com_o_tipo_e_os_dados(self):
        self.repositorio.adicionar_ativo(criar_notebook())

        ativos = self.recarregar_ativos()

        self.assertIsInstance(ativos[1], Notebook)
        self.assertEqual(ativos[1].nome, "Notebook da Recepção")
        self.assertEqual(ativos[1].sistema_operacional, "Linux")
        self.assertEqual(ativos[1].vulnerabilidades, {})

    def test_adicionar_ativo_mantem_os_que_ja_estavam_gravados(self):
        self.repositorio.adicionar_ativo(criar_notebook())

        outro_repositorio = self.criar_repositorio()
        outro_repositorio.adicionar_ativo(criar_servidor())

        self.assertEqual(len(self.recarregar_ativos()), 2)

    def test_atualizar_ativo_grava_os_dados_novos(self):
        self.repositorio.adicionar_ativo(criar_notebook())

        notebook_editado = criar_notebook()
        notebook_editado.responsavel = "Ana Souza"
        self.repositorio.atualizar_ativo(notebook_editado)

        self.assertEqual(self.recarregar_ativos()[1].responsavel, "Ana Souza")

    def test_atualizar_ativo_nao_mexe_nos_vinculos(self):
        self.preparar_dois_ativos_com_vinculos()

        self.repositorio.atualizar_ativo(criar_notebook())

        self.assertEqual(
            self.recarregar_ativos()[1].vulnerabilidades,
            {1: StatusDaVuln.ABERTA, 2: StatusDaVuln.EM_TRATAMENTO},
        )

    def test_atualizar_ativo_pode_trocar_o_tipo(self):
        self.repositorio.adicionar_ativo(criar_notebook())

        servidor_no_lugar = Servidor(
            1, "Notebook da Recepção", Setor.TI, "Rafael Torres", StatusDoAtivo.ATIVO, 16, 1
        )
        self.repositorio.atualizar_ativo(servidor_no_lugar)

        ativo_recarregado = self.recarregar_ativos()[1]
        self.assertIsInstance(ativo_recarregado, Servidor)
        self.assertEqual(ativo_recarregado.ram, 16)

    def test_remover_ativo_tira_so_ele(self):
        self.repositorio.adicionar_ativo(criar_notebook())
        self.repositorio.adicionar_ativo(criar_servidor())

        self.repositorio.remover_ativo(1)

        ativos = self.recarregar_ativos()
        self.assertNotIn(1, ativos)
        self.assertIn(2, ativos)

    def test_remover_ativo_nao_tira_a_vulnerabilidade_do_catalogo(self):
        self.preparar_dois_ativos_com_vinculos()

        self.repositorio.remover_ativo(1)

        self.assertIn(1, self.recarregar_catalogo())
        self.assertIn(2, self.recarregar_catalogo())

    def test_adicionar_vulnerabilidade_grava_no_catalogo(self):
        self.repositorio.adicionar_vulnerabilidade(criar_senha_fraca())

        catalogo = self.recarregar_catalogo()

        self.assertEqual(catalogo[1].nome_vulnerabilidade, "SSH com senha fraca")
        self.assertEqual(catalogo[1].cvss, 7.5)

    def test_adicionar_vulnerabilidade_mantem_as_que_ja_estavam_gravadas(self):
        self.repositorio.adicionar_vulnerabilidade(criar_senha_fraca())

        outro_repositorio = self.criar_repositorio()
        outro_repositorio.adicionar_vulnerabilidade(criar_firmware_desatualizado())

        self.assertEqual(len(self.recarregar_catalogo()), 2)

    def test_atualizar_vulnerabilidade_grava_os_dados_novos(self):
        self.repositorio.adicionar_vulnerabilidade(criar_senha_fraca())

        self.repositorio.atualizar_vulnerabilidade(Vulnerabilidade(1, "SSH com senha padrão", 9.8))

        catalogo = self.recarregar_catalogo()
        self.assertEqual(catalogo[1].nome_vulnerabilidade, "SSH com senha padrão")
        self.assertEqual(catalogo[1].cvss, 9.8)

    def test_remover_vulnerabilidade_tira_do_catalogo(self):
        self.repositorio.adicionar_vulnerabilidade(criar_senha_fraca())
        self.repositorio.adicionar_vulnerabilidade(criar_firmware_desatualizado())

        self.repositorio.remover_vulnerabilidade(1)

        catalogo = self.recarregar_catalogo()
        self.assertNotIn(1, catalogo)
        self.assertIn(2, catalogo)

    def test_remover_vulnerabilidade_tira_os_vinculos_de_todos_os_ativos(self):
        self.preparar_dois_ativos_com_vinculos()

        self.repositorio.remover_vulnerabilidade(1)

        ativos = self.recarregar_ativos()
        self.assertEqual(ativos[1].vulnerabilidades, {2: StatusDaVuln.EM_TRATAMENTO})
        self.assertEqual(ativos[2].vulnerabilidades, {})

    def test_vincular_grava_o_vinculo_com_o_status(self):
        self.repositorio.adicionar_ativo(criar_notebook())
        self.repositorio.adicionar_vulnerabilidade(criar_senha_fraca())

        self.repositorio.vincular(1, 1, StatusDaVuln.ABERTA)

        self.assertEqual(self.recarregar_ativos()[1].vulnerabilidades, {1: StatusDaVuln.ABERTA})

    def test_atualizar_status_vinculo_troca_so_aquele_status(self):
        self.preparar_dois_ativos_com_vinculos()

        self.repositorio.atualizar_status_vinculo(1, 1, StatusDaVuln.CORRIGIDA)

        ativos = self.recarregar_ativos()
        self.assertEqual(
            ativos[1].vulnerabilidades,
            {1: StatusDaVuln.CORRIGIDA, 2: StatusDaVuln.EM_TRATAMENTO},
        )
        self.assertEqual(ativos[2].vulnerabilidades, {1: StatusDaVuln.ACEITA})

    def test_desvincular_tira_so_aquele_vinculo(self):
        self.preparar_dois_ativos_com_vinculos()

        self.repositorio.desvincular(1, 1)

        ativos = self.recarregar_ativos()
        self.assertEqual(ativos[1].vulnerabilidades, {2: StatusDaVuln.EM_TRATAMENTO})
        self.assertEqual(ativos[2].vulnerabilidades, {1: StatusDaVuln.ACEITA})
        self.assertIn(1, self.recarregar_catalogo())

    def test_adicionar_dependencia_grava_o_id_e_a_fracao(self):
        self.repositorio.adicionar_ativo(criar_notebook())
        self.repositorio.adicionar_ativo(criar_servidor())

        self.repositorio.adicionar_dependencia(1, 2, 0.5)

        ativos = self.recarregar_ativos()
        self.assertEqual(ativos[1].dependencias, {2: 0.5})
        self.assertEqual(ativos[2].dependencias, {})

    def test_remover_dependencia_tira_a_dependencia(self):
        self.repositorio.adicionar_ativo(criar_notebook())
        self.repositorio.adicionar_ativo(criar_servidor())
        self.repositorio.adicionar_dependencia(1, 2, 0.5)

        self.repositorio.remover_dependencia(1, 2)

        self.assertEqual(self.recarregar_ativos()[1].dependencias, {})

    def test_atualizar_ativo_nao_mexe_nas_dependencias(self):
        self.repositorio.adicionar_ativo(criar_notebook())
        self.repositorio.adicionar_ativo(criar_servidor())
        self.repositorio.adicionar_dependencia(1, 2, 0.5)

        self.repositorio.atualizar_ativo(criar_notebook())

        self.assertEqual(self.recarregar_ativos()[1].dependencias, {2: 0.5})

    def test_remover_ativo_tira_as_dependencias_que_apontavam_para_ele(self):
        self.repositorio.adicionar_ativo(criar_notebook())
        self.repositorio.adicionar_ativo(criar_servidor())
        self.repositorio.adicionar_dependencia(1, 2, 0.5)

        self.repositorio.remover_ativo(2)

        self.assertEqual(self.recarregar_ativos()[1].dependencias, {})
