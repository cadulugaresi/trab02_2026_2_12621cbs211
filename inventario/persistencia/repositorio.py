from abc import ABC, abstractmethod


class Repositorio(ABC):

    @abstractmethod
    def carregar_ativos(self):
        pass

    @abstractmethod
    def carregar_catalogo(self):
        pass

    @abstractmethod
    def adicionar_ativo(self, ativo):
        pass

    @abstractmethod
    def atualizar_ativo(self, ativo):
        pass

    @abstractmethod
    def remover_ativo(self, id_ativo):
        pass

    @abstractmethod
    def adicionar_vulnerabilidade(self, vulnerabilidade):
        pass

    @abstractmethod
    def atualizar_vulnerabilidade(self, vulnerabilidade):
        pass

    @abstractmethod
    def remover_vulnerabilidade(self, id_vulnerabilidade):
        pass

    @abstractmethod
    def vincular(self, id_ativo, id_vulnerabilidade, status):
        pass

    @abstractmethod
    def atualizar_status_vinculo(self, id_ativo, id_vulnerabilidade, status):
        pass

    @abstractmethod
    def desvincular(self, id_ativo, id_vulnerabilidade):
        pass

    @abstractmethod
    def adicionar_dependencia(self, id_ativo_que_depende, id_ativo_do_qual_depende, fracao):
        pass

    @abstractmethod
    def remover_dependencia(self, id_ativo_que_depende, id_ativo_do_qual_depende):
        pass

    @abstractmethod
    def atualizar_dependencia(
        self,
        id_ativo_que_depende,
        id_ativo_do_qual_depende_antigo,
        id_ativo_do_qual_depende_novo,
        fracao_nova,
    ):
        pass
