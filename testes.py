import unittest
from funcoes_t2 import *

class TestExibirDetalhes(unittest.TestCase):

    # --- Notebook ---
    def test_notebook_mostra_tipo(self):
        n = Notebook(1, "Dell", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, "Linux", 15.6)
        detalhes = n.exibir_detalhes()
        self.assertIn("Tipo: Notebook", detalhes)

    def test_notebook_mostra_campos_especificos(self):
        n = Notebook(1, "Dell", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, "Linux", 15.6)
        detalhes = n.exibir_detalhes()
        self.assertIn("Sistema operacional: Linux", detalhes)
        self.assertIn("Tamanho da tela: 15.6 polegadas", detalhes)

    # --- Servidor ---
    def test_servidor_mostra_tipo(self):
        s = Servidor(2, "Dell PowerEdge", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, 32, 4)
        detalhes = s.exibir_detalhes()
        self.assertIn("Tipo: Servidor", detalhes)

    def test_servidor_mostra_campos_especificos(self):
        s = Servidor(2, "Dell PowerEdge", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, 32, 4)
        detalhes = s.exibir_detalhes()
        self.assertIn("Memória RAM: 32GB", detalhes)
        self.assertIn("Qtde armazenamento: 4T", detalhes)

    # --- Roteador ---
    def test_roteador_mostra_tipo(self):
        r = Roteador(3, "TP-Link", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, 4, 1000)
        detalhes = r.exibir_detalhes()
        self.assertIn("Tipo: Roteador", detalhes)

    def test_roteador_mostra_campos_especificos(self):
        r = Roteador(3, "TP-Link", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, 4, 1000)
        detalhes = r.exibir_detalhes()
        self.assertIn("Qtde de portas: 4", detalhes)
        self.assertIn("Velocidade: 1000MB", detalhes)

    # --- Impressora ---
    def test_impressora_mostra_tipo(self):
        i = Impressora(4, "HP", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, Cor.COLORIDA, Tecnologia.LASER)
        detalhes = i.exibir_detalhes()
        self.assertIn("Tipo: Impressora", detalhes)

    def test_impressora_mostra_campos_especificos(self):
        i = Impressora(4, "HP", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, Cor.COLORIDA, Tecnologia.LASER)
        detalhes = i.exibir_detalhes()
        self.assertIn("Cor: COLORIDA", detalhes)
        self.assertIn("Tecnologia: LASER", detalhes)

    # --- Campos comuns em todos ---
    def test_todos_mostram_campos_comuns(self):
        n = Notebook(1, "Dell", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, "Linux", 15.6)
        detalhes = n.exibir_detalhes()
        self.assertIn("ID: 1", detalhes)
        self.assertIn("Nome: Dell", detalhes)
        self.assertIn("Setor: TI", detalhes)
        self.assertIn("Responsável: Cadu", detalhes)
        self.assertIn("Status: ATIVO", detalhes)


if __name__ == '__main__':
    unittest.main()