from inventario.dominio.excecoes import DadoInvalidoError, RecursoNaoEncontradoError
from inventario.dominio.vulnerabilidade import Vulnerabilidade
from inventario.servicos.ativos import obter_ativo
from inventario.dominio.validacoes import (
    validar_cvss,
    validar_inteiro_positivo,
    validar_texto_obrigatorio,
)


def obter_vulnerabilidade(catalogo, id_vulnerabilidade):
    if id_vulnerabilidade not in catalogo:
        raise RecursoNaoEncontradoError("Vulnerabilidade não encontrada no catálogo.")
    return catalogo[id_vulnerabilidade]


def proximo_id(dicionario):

    maior_id = 0

    for id_existente in dicionario:
        if id_existente > maior_id:
            maior_id = id_existente

    return maior_id + 1


def registrar_vulnerabilidade_no_catalogo(repositorio, catalogo, nome_vulnerabilidade, cvss):
    cvss = validar_cvss(cvss)
    validar_texto_obrigatorio(nome_vulnerabilidade)
    id_vulnerabilidade = proximo_id(catalogo)

    vulnerabilidade = Vulnerabilidade(id_vulnerabilidade, nome_vulnerabilidade, cvss)
    repositorio.adicionar_vulnerabilidade(vulnerabilidade)
    catalogo[id_vulnerabilidade] = vulnerabilidade

    return vulnerabilidade


def vincular_vulnerabilidade(
    repositorio, ativos, catalogo, id_ativo, id_vulnerabilidade, status_tratamento
):
    validar_inteiro_positivo(id_vulnerabilidade)
    ativo = obter_ativo(ativos, id_ativo)
    obter_vulnerabilidade(catalogo, id_vulnerabilidade)

    if id_vulnerabilidade in ativo.vulnerabilidades:
        raise DadoInvalidoError("Esta vulnerabilidade já está vinculada a este ativo.")

    repositorio.vincular(id_ativo, id_vulnerabilidade, status_tratamento)
    ativo.vulnerabilidades[id_vulnerabilidade] = status_tratamento


def desvincular_vulnerabilidade(repositorio, ativos, id_ativo, id_vulnerabilidade):
    ativo = obter_ativo(ativos, id_ativo)

    if id_vulnerabilidade not in ativo.vulnerabilidades:
        raise RecursoNaoEncontradoError("Esta vulnerabilidade não está vinculada a este ativo.")

    repositorio.desvincular(id_ativo, id_vulnerabilidade)
    del ativo.vulnerabilidades[id_vulnerabilidade]


def atualizar_status_vulnerabilidade(
    repositorio, ativos, id_ativo, id_vulnerabilidade, novo_status
):
    ativo = obter_ativo(ativos, id_ativo)

    if id_vulnerabilidade not in ativo.vulnerabilidades:
        raise RecursoNaoEncontradoError(
            "Este ativo não possui nenhuma vulnerabilidade com este ID vinculada a ele."
        )

    repositorio.atualizar_status_vinculo(id_ativo, id_vulnerabilidade, novo_status)
    ativo.vulnerabilidades[id_vulnerabilidade] = novo_status


def excluir_vulnerabilidade_do_catalogo(repositorio, catalogo, ativos, id_vulnerabilidade):
    obter_vulnerabilidade(catalogo, id_vulnerabilidade)
    repositorio.remover_vulnerabilidade(id_vulnerabilidade)

    for ativo in ativos.values():
        if id_vulnerabilidade in ativo.vulnerabilidades:
            del ativo.vulnerabilidades[id_vulnerabilidade]

    del catalogo[id_vulnerabilidade]


def atualizar_vulnerabilidade_no_catalogo(repositorio, catalogo, vulnerabilidade_atualizada):
    obter_vulnerabilidade(catalogo, vulnerabilidade_atualizada.id_vulnerabilidade)
    validar_texto_obrigatorio(vulnerabilidade_atualizada.nome_vulnerabilidade)
    vulnerabilidade_atualizada.cvss = validar_cvss(vulnerabilidade_atualizada.cvss)
    repositorio.atualizar_vulnerabilidade(vulnerabilidade_atualizada)
    catalogo[vulnerabilidade_atualizada.id_vulnerabilidade] = vulnerabilidade_atualizada
