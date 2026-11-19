import math

from inventario.dominio.excecoes import DadoInvalidoError

MAIOR_INTEIRO_ACEITO = 2**63 - 1


def validar_numero(valor):
    if type(valor) is not int and type(valor) is not float:
        raise DadoInvalidoError("Este campo precisa ser um número.")
    if type(valor) is float and not math.isfinite(valor):
        raise DadoInvalidoError("Este campo precisa ser um número finito.")
    if type(valor) is int and valor > MAIOR_INTEIRO_ACEITO:
        raise DadoInvalidoError(
            f"Este número é grande demais. O máximo aceito é {MAIOR_INTEIRO_ACEITO}."
        )
    return valor


def validar_numero_positivo(valor):
    validar_numero(valor)
    if valor <= 0:
        raise DadoInvalidoError("Este campo não pode ser nulo ou negativo.")
    return valor


def validar_inteiro_positivo(valor):
    if type(valor) is not int:
        raise DadoInvalidoError("Este campo precisa ser um número inteiro.")
    return validar_numero_positivo(valor)


def validar_cvss(cvss):
    validar_numero(cvss)
    cvss = round(cvss, 1)
    if cvss <= 0 or cvss > 10:
        raise DadoInvalidoError("O CVSS deve estar entre 0.1 e 10.")
    return cvss


def validar_texto_obrigatorio(texto):
    if type(texto) is not str:
        raise DadoInvalidoError("Este campo precisa ser um texto.")
    if not texto.strip():
        raise DadoInvalidoError("Este campo não pode ser vazio.")
    if texto.strip().isnumeric():
        raise DadoInvalidoError("Este campo não pode ser composto apenas por números.")


def validar_soma_fracao(soma_atual, fracao_nova):
    soma = round(soma_atual + fracao_nova, 6)
    if soma >= 1:
        raise DadoInvalidoError(
            "A soma das frações precisa ficar abaixo de 1. "
            f"A nova fração precisa ser menor que {round(1 - soma_atual, 6)}."
        )
    return fracao_nova


def validar_fracao(fracao):
    validar_numero(fracao)
    if fracao <= 0:
        raise DadoInvalidoError("A fração precisa ser maior que zero.")


def validar_dependencia_de_si_mesmo(id_ativo_que_depende, id_ativo_do_qual_depende):
    if id_ativo_que_depende == id_ativo_do_qual_depende:
        raise DadoInvalidoError("Um ativo não pode depender dele próprio.")


def validar_fracao_da_dependencia(soma_atual, fracao):
    validar_fracao(fracao)
    validar_soma_fracao(soma_atual, fracao)


def validar_fator_exposicao(fator):
    validar_numero(fator)
    if fator <= 0 or fator > 2:
        raise DadoInvalidoError("O fator de exposição deve ser maior que 0 e no máximo 2.")
    return fator
