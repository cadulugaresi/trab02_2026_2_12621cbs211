from abc import ABC, abstractmethod


class Repositorio(ABC):

    @abstractmethod
    def carregar_ativos(self):
        pass

    @abstractmethod
    def salvar_ativos(self, ativos):
        pass

    @abstractmethod
    def carregar_catalogo(self):
        pass

    @abstractmethod
    def salvar_catalogo(self, catalogo):
        pass
