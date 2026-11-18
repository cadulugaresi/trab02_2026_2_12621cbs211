from inventario.dominio.excecoes import DadoInvalidoError
from inventario.dominio.vulnerabilidade import Vulnerabilidade
from inventario.servicos.ativos import obter_ativo
from inventario.dominio.validacoes import validar_cvss, validar_nome_responsavel


def proximo_id(dicionario):

    maior_id = 0

    for id_existente in dicionario:
        if id_existente > maior_id:
            maior_id = id_existente

    return maior_id + 1


def registrar_vulnerabilidade_no_catalogo(repositorio, catalogo, nome_vulnerabilidade, cvss):
    cvss = validar_cvss(cvss)
    validar_nome_responsavel(nome_vulnerabilidade)
    id_vulnerabilidade = proximo_id(catalogo)

    vulnerabilidade = Vulnerabilidade(id_vulnerabilidade, nome_vulnerabilidade, cvss)
    catalogo[id_vulnerabilidade] = vulnerabilidade
    repositorio.adicionar_vulnerabilidade(vulnerabilidade)

    return vulnerabilidade


def vincular_vulnerabilidade(
    repositorio, ativos, catalogo, id_ativo, id_vulnerabilidade, status_tratamento
):
    ativo = obter_ativo(ativos, id_ativo)

    if id_vulnerabilidade not in catalogo:
        raise DadoInvalidoError("Vulnerabilidade não encontrada no catálogo.")

    if id_vulnerabilidade in ativo.vulnerabilidades:
        raise DadoInvalidoError("Esta vulnerabilidade já está vinculada a este ativo.")

    ativo.vulnerabilidades[id_vulnerabilidade] = status_tratamento
    repositorio.vincular(id_ativo, id_vulnerabilidade, status_tratamento)


def desvincular_vulnerabilidade(repositorio, ativos, id_ativo, id_vulnerabilidade):
    ativo = obter_ativo(ativos, id_ativo)

    if id_vulnerabilidade not in ativo.vulnerabilidades:
        raise DadoInvalidoError("Esta vulnerabilidade não está vinculada a este ativo.")

    del ativo.vulnerabilidades[id_vulnerabilidade]
    repositorio.desvincular(id_ativo, id_vulnerabilidade)


def atualizar_status_vulnerabilidade(
    repositorio, ativos, id_ativo, id_vulnerabilidade, novo_status
):
    ativo = obter_ativo(ativos, id_ativo)

    if id_vulnerabilidade not in ativo.vulnerabilidades:
        raise DadoInvalidoError(
            "Este ativo não possui nenhuma vulnerabilidade com este ID vinculada a ele."
        )

    ativo.vulnerabilidades[id_vulnerabilidade] = novo_status
    repositorio.atualizar_status_vinculo(id_ativo, id_vulnerabilidade, novo_status)


def excluir_vulnerabilidade_do_catalogo(repositorio, catalogo, ativos, id_vulnerabilidade):
    if id_vulnerabilidade not in catalogo:
        raise DadoInvalidoError("Vulnerabilidade não encontrada no catálogo.")

    for ativo in ativos.values():
        if id_vulnerabilidade in ativo.vulnerabilidades:
            del ativo.vulnerabilidades[id_vulnerabilidade]

    del catalogo[id_vulnerabilidade]
    repositorio.remover_vulnerabilidade(id_vulnerabilidade)


def atualizar_vulnerabilidade_no_catalogo(repositorio, catalogo, vulnerabilidade_atualizada):
    if vulnerabilidade_atualizada.id_vulnerabilidade not in catalogo:
        raise DadoInvalidoError("Vulnerabilidade não encontrada no catálogo.")
    vulnerabilidade_atualizada.cvss = validar_cvss(vulnerabilidade_atualizada.cvss)
    catalogo[vulnerabilidade_atualizada.id_vulnerabilidade] = vulnerabilidade_atualizada
    repositorio.atualizar_vulnerabilidade(vulnerabilidade_atualizada)
