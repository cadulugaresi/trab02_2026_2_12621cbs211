from inventario.dominio.excecoes import DadoInvalidoError


def validar_nome_responsavel(nome):

    if not nome:
        raise DadoInvalidoError("Este campo não pode ser vazio.")
    if nome.isnumeric():
        raise DadoInvalidoError("Este campo não pode ser composto apenas por números.")
