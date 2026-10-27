from inventario.excecoes import DadoInvalidoError
from inventario.modelos.ativo import OPCOES_MENU
from inventario.validacoes import (
    validar_cor,
    validar_nome_responsavel,
    validar_setor,
    validar_status,
    validar_status_vulnerabilidade,
    validar_tecnologia,
    validar_tipo,
)


def pedir_info(mensagem):

    info = None
    while info is None:

        info = input(mensagem).strip()

        try:
            validar_nome_responsavel(info)
            return info
        except DadoInvalidoError as erro:
            print(erro)
            info = None


def pedir_status(mensagem):

    status = None

    while status is None:

        try:
            print("""
            Status:

            ATIVO - 1
            INATIVO - 2
            EM_MANUTENCAO - 3
            """)

            status_digitado = input(mensagem).strip()
            status = validar_status(status_digitado)

        except DadoInvalidoError as erro:
            print(erro)

    return status


def pedir_status_vulnerabilidade(mensagem):

    status_tratamento = None

    while status_tratamento is None:

        try:
            print("""
            Status da vulnerabilidade:

            ABERTA - 1
            EM TRATAMENTO - 2
            CORRIGIDA - 3
            ACEITA - 4
            """)

            status_digitado = input(mensagem).strip()
            status_tratamento = validar_status_vulnerabilidade(status_digitado)

        except DadoInvalidoError as erro:
            print(erro)

    return status_tratamento


def pedir_setor(mensagem):

    setor = None

    while setor is None:

        try:
            print("""
            Setor:

            TI - 1
            FINANCEIRO - 2
            MARKETING - 3
            RH - 4
            JURIDICO - 5
            """)

            setor_digitado = input(mensagem).strip()
            setor = validar_setor(setor_digitado)

        except DadoInvalidoError as erro:
            print(erro)

    return setor


def pedir_float(mensagem):
    while True:
        try:
            numero = input(mensagem).strip().replace(",", ".")

            if not numero:
                raise DadoInvalidoError("Este campo não pode ser vazio. Tente novamente.")

            if float(numero) <= 0:
                raise DadoInvalidoError(
                    "Este campo não pode ser nulo ou negativo. Tente novamente."
                )

            return float(numero)

        except ValueError:
            print("Digite um número válido")

        except DadoInvalidoError as erro:
            print(erro)


def pedir_int(mensagem):

    while True:
        try:
            numero_int = input(mensagem).strip()

            if not numero_int:
                raise DadoInvalidoError("Este campo não pode ser vazio. Tente novamente.")

            if int(numero_int) <= 0:
                raise DadoInvalidoError(
                    "Este campo não pode ser nulo ou negativo. Tente novamente."
                )

            return int(numero_int)

        except ValueError:
            print("Digite um número válido")

        except DadoInvalidoError as erro:
            print(erro)


def pedir_cvss(mensagem):

    while True:
        cvss = pedir_float(mensagem)

        if cvss > 10:
            print("O CVSS não pode ser maior que 10.")
        else:
            return round(cvss, 1)


def pedir_tipo(mensagem):

    tipo = None

    while tipo is None:

        try:
            print("Tipos de ativo:")
            for numero, nome in OPCOES_MENU.items():
                print(f"{numero} - {nome}")

            tipo_digitado = input(mensagem).strip()
            tipo = validar_tipo(tipo_digitado)

        except DadoInvalidoError as erro:
            print(erro)

    return tipo


def pedir_cor():

    cor = None
    while cor is None:

        try:
            print("""
            Qual é a cor do cartucho da impressora?

            1 - Colorido
            2 - Preto e branco
            """)
            opcao_cor = input("Escolha: ").strip()
            cor = validar_cor(opcao_cor)

        except DadoInvalidoError as erro:
            print(erro)

    return cor


def pedir_tecnologia():

    tecnologia = None
    while tecnologia is None:

        try:
            print("""
            Tecnologias de impressão:

            1 - Tinta
            2 - Laser
            """)
            opcao_tec = input("Qual é a tecnologia da impressão? ")
            tecnologia = validar_tecnologia(opcao_tec)

        except DadoInvalidoError as erro:
            print(erro)

    return tecnologia
