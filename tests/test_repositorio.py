from inventario.persistencia.arquivos_json import RepositorioJSON
from tests.apoio import TesteComArquivosTemporarios
from tests.contrato_repositorio import ContratoDoRepositorio


class TestRepositorioJSON(ContratoDoRepositorio, TesteComArquivosTemporarios):

    def criar_repositorio(self):
        return RepositorioJSON()
