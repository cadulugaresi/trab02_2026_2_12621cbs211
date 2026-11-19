class DadoInvalidoError(Exception):
    pass


class RecursoNaoEncontradoError(DadoInvalidoError):
    pass


class PersistenciaError(Exception):
    pass
