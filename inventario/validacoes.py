from inventario.enums import Cor, Setor, StatusDaVuln, StatusDoAtivo, Tecnologia
from inventario.excecoes import DadoInvalidoError
from inventario.modelos.ativo import Impressora, Notebook, Roteador, Servidor


def validar_nome_responsavel(nome):

    if not nome:
        raise DadoInvalidoError("Este campo não pode ser vazio.")
    if nome.isnumeric():
        raise DadoInvalidoError("Este campo não pode ser composto apenas por números.")


def validar_status(status_digitado):

    if status_digitado == "1":
        return StatusDoAtivo.ATIVO

    elif status_digitado == "2":
        return StatusDoAtivo.INATIVO

    elif status_digitado == "3":
        return StatusDoAtivo.EM_MANUTENCAO

    else:
        raise DadoInvalidoError("Status inválido. Tente novamente.")


def validar_status_vulnerabilidade(status_digitado):

    if status_digitado == "1":
        return StatusDaVuln.ABERTA
    elif status_digitado == "2":
        return StatusDaVuln.EM_TRATAMENTO
    elif status_digitado == "3":
        return StatusDaVuln.CORRIGIDA
    elif status_digitado == "4":
        return StatusDaVuln.ACEITA
    else:
        raise DadoInvalidoError("Status inválido. Tente novamente.")


def validar_setor(setor_digitado):

    if setor_digitado == "1":
        return Setor.TI

    elif setor_digitado == "2":
        return Setor.FINANCEIRO

    elif setor_digitado == "3":
        return Setor.MARKETING

    elif setor_digitado == "4":
        return Setor.RH

    elif setor_digitado == "5":
        return Setor.JURIDICO

    else:
        raise DadoInvalidoError("Setor inválido. Tente novamente.")


def validar_tipo(tipo_digitado):

    if tipo_digitado == "1":
        return Notebook

    elif tipo_digitado == "2":
        return Servidor

    elif tipo_digitado == "3":
        return Roteador

    elif tipo_digitado == "4":
        return Impressora

    else:
        raise DadoInvalidoError("Tipo inválido. Tente novamente.")


def validar_cor(opcao):

    if opcao == "1":
        return Cor.COLORIDA
    elif opcao == "2":
        return Cor.PRETA_E_BRANCA

    else:
        raise DadoInvalidoError("Cor inválida. Tente novamente.")


def validar_tecnologia(opcao_tec):

    if opcao_tec == "1":
        return Tecnologia.TINTA
    elif opcao_tec == "2":
        return Tecnologia.LASER
    else:
        raise DadoInvalidoError("Tecnologia inválida. Tente novamente.")
