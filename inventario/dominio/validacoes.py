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


def validar_dependencia_de_si_mesmo(id_ativo_que_depende, id_ativo_do_qual_depende):
    if id_ativo_que_depende == id_ativo_do_qual_depende:
        raise DadoInvalidoError("Um ativo não pode depender dele próprio.")


def validar_fracao_da_dependencia(soma_atual, fracao):
    validar_fracao(fracao)
    validar_soma_fracao(soma_atual, fracao)


def validar_fator_exposicao(fator):
    if fator <= 0 or fator > 2:
        raise DadoInvalidoError("O fator de exposição deve ser maior que 0 e no máximo 2.")
    return fator
