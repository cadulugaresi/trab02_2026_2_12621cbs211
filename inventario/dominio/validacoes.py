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


def validar_soma_fracao(soma_atual, fracao_nova):
    soma = round(soma_atual + fracao_nova, 6)
    if soma >= 1:
        raise DadoInvalidoError(
            f"A soma das frações precisa ficar abaixo de 1. Ainda cabem {1 - soma_atual:.3f}."
        )
    return fracao_nova


def validar_fracao(fracao):
    if fracao <= 0:
        raise DadoInvalidoError("A fração precisa ser maior que zero.")
