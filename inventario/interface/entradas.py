from inventario.dominio.excecoes import DadoInvalidoError
from inventario.dominio.validacoes import (
    validar_cvss,
    validar_texto_obrigatorio,
    validar_fator_exposicao,
)
from inventario.interface.conversao_das_opcoes_do_menu import (
    TIPOS_DE_ATIVOS,
    validar_cor,
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
            validar_texto_obrigatorio(info)
            return info
        except DadoInvalidoError as erro:
            print(erro)
            info = None


def pedir_status(mensagem):

    status = None

    while status is None:

        try:
            print("\nStatus:\n")
            print("ATIVO - 1\nINATIVO - 2\nEM_MANUTENCAO - 3")

            status_digitado = input(mensagem).strip()
            status = validar_status(status_digitado)

        except DadoInvalidoError as erro:
            print(erro)

    return status


def pedir_status_vulnerabilidade(mensagem):

    status_tratamento = None

    while status_tratamento is None:

        try:
            print("\nStatus da vulnerabilidade:\n")
            print("ABERTA - 1\nEM TRATAMENTO - 2\nCORRIGIDA - 3\nACEITA - 4")

            status_digitado = input(mensagem).strip()
            status_tratamento = validar_status_vulnerabilidade(status_digitado)

        except DadoInvalidoError as erro:
            print(erro)

    return status_tratamento


def pedir_setor(mensagem):

    setor = None

    while setor is None:

        try:
            print("\nSetor:\n")
            print("TI - 1\nFINANCEIRO - 2\nMARKETING - 3\nRH - 4\nJURIDICO - 5")

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
        try:
            return validar_cvss(cvss)
        except DadoInvalidoError as erro:
            print(erro)


def pedir_tipo(mensagem):

    tipo = None

    while tipo is None:

        try:
            print("\nTipos de ativo:\n")
            for numero, classe in TIPOS_DE_ATIVOS.items():
                print(f"{numero} - {classe.__name__}")

            tipo_digitado = input(mensagem).strip()
            tipo = validar_tipo(tipo_digitado)

        except DadoInvalidoError as erro:
            print(erro)

    return tipo


def pedir_cor():

    cor = None
    while cor is None:

        try:
            print("\nQual é a cor do cartucho da impressora?\n")
            print("1 - Colorido\n2 - Preto e branco")
            opcao_cor = input("Escolha: ").strip()
            cor = validar_cor(opcao_cor)

        except DadoInvalidoError as erro:
            print(erro)

    return cor


def pedir_tecnologia():

    tecnologia = None
    while tecnologia is None:

        try:
            print("\nTecnologias de impressão:\n")
            print("1 - Tinta\n2 - Laser")
            opcao_tec = input("Qual é a tecnologia da impressão? ")
            tecnologia = validar_tecnologia(opcao_tec)

        except DadoInvalidoError as erro:
            print(erro)

    return tecnologia


def pedir_fator_exposicao(mensagem, fator_sugerido=None):
    while True:
        novo_fator_exposicao = input(mensagem).strip().replace(",", ".")

        if novo_fator_exposicao == "" and fator_sugerido is not None:
            return fator_sugerido
        else:
            try:
                return validar_fator_exposicao(float(novo_fator_exposicao))
            except ValueError:
                print("Digite um número válido")
            except DadoInvalidoError as erro:
                print(erro)
