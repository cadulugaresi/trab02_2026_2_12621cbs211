from inventario.dominio.excecoes import DadoInvalidoError


def validar_cvss(cvss):
    cvss = round(cvss, 1)
    if cvss <= 0 or cvss > 10:
        raise DadoInvalidoError("O CVSS deve estar entre 0.1 e 10.")
    return cvss


def validar_nome_responsavel(nome):

    if not nome:
        raise DadoInvalidoError("Este campo não pode ser vazio.")
    if nome.isnumeric():
        raise DadoInvalidoError("Este campo não pode ser composto apenas por números.")
