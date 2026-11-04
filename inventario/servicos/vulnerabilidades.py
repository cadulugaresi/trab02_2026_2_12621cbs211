from inventario.dominio.excecoes import DadoInvalidoError
from inventario.dominio.vulnerabilidade import Vulnerabilidade
from inventario.persistencia.arquivos_json import salvar_catalogo, salvar_dados
from inventario.servicos.ativos import obter_ativo


def proximo_id(dicionario):

    maior_id = 0

    for id_existente in dicionario:
        if id_existente > maior_id:
            maior_id = id_existente

    return maior_id + 1


def registrar_vulnerabilidade_no_catalogo(catalogo, nome_vulnerabilidade, cvss):
    id_vulnerabilidade = proximo_id(catalogo)

    vulnerabilidade = Vulnerabilidade(id_vulnerabilidade, nome_vulnerabilidade, cvss)
    catalogo[id_vulnerabilidade] = vulnerabilidade
    salvar_catalogo(catalogo)

    return vulnerabilidade


def vincular_vulnerabilidade(ativos, catalogo, id_ativo, id_vulnerabilidade, status_tratamento):
    ativo = obter_ativo(ativos, id_ativo)

    if id_vulnerabilidade not in catalogo:
        raise DadoInvalidoError("Vulnerabilidade não encontrada no catálogo.")

    if id_vulnerabilidade in ativo.vulnerabilidades:
        raise DadoInvalidoError("Esta vulnerabilidade já está vinculada a este ativo.")

    ativo.vulnerabilidades[id_vulnerabilidade] = status_tratamento
    salvar_dados(ativos)


def desvincular_vulnerabilidade(ativos, id_ativo, id_vulnerabilidade):
    ativo = obter_ativo(ativos, id_ativo)

    if id_vulnerabilidade not in ativo.vulnerabilidades:
        raise DadoInvalidoError("Esta vulnerabilidade não está vinculada a este ativo.")

    del ativo.vulnerabilidades[id_vulnerabilidade]
    salvar_dados(ativos)


def atualizar_status_vulnerabilidade(ativos, id_ativo, id_vulnerabilidade, novo_status):
    ativo = obter_ativo(ativos, id_ativo)

    if id_vulnerabilidade not in ativo.vulnerabilidades:
        raise DadoInvalidoError(
            "Este ativo não possui nenhuma vulnerabilidade com este ID vinculada a ele."
        )

    ativo.vulnerabilidades[id_vulnerabilidade] = novo_status
    salvar_dados(ativos)


def excluir_vulnerabilidade_do_catalogo(catalogo, ativos, id_vulnerabilidade):
    if id_vulnerabilidade not in catalogo:
        raise DadoInvalidoError("Vulnerabilidade não encontrada no catálogo.")

    for ativo in ativos.values():
        if id_vulnerabilidade in ativo.vulnerabilidades:
            del ativo.vulnerabilidades[id_vulnerabilidade]

    del catalogo[id_vulnerabilidade]
    salvar_catalogo(catalogo)
    salvar_dados(ativos)


def atualizar_vulnerabilidade_no_catalogo(catalogo, vulnerabilidade_atualizada):
    if vulnerabilidade_atualizada.id_vulnerabilidade not in catalogo:
        raise DadoInvalidoError("Vulnerabilidade não encontrada no catálogo.")
    catalogo[vulnerabilidade_atualizada.id_vulnerabilidade] = vulnerabilidade_atualizada
    salvar_catalogo(catalogo)
