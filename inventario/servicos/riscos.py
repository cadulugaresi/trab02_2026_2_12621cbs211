import numpy as np

from inventario.dominio.enums import StatusDaVuln


def mapear_ids_para_posicoes(dicionario_por_id):
    posicoes = {}

    for posicao, id_do_item in enumerate(sorted(dicionario_por_id)):
        posicoes[id_do_item] = posicao

    return posicoes


def montar_matriz_m(ativos, catalogo, posicoes_dos_ativos, posicoes_das_vulns):
    matriz_m = np.zeros((len(ativos), len(catalogo)))

    for id_ativo, ativo in ativos.items():
        for id_vulnerabilidade, status in ativo.vulnerabilidades.items():
            if status != StatusDaVuln.CORRIGIDA:
                matriz_m[posicoes_dos_ativos[id_ativo], posicoes_das_vulns[id_vulnerabilidade]] = 1

    return matriz_m


def montar_vetor_fator(ativos, posicoes_dos_ativos):
    vetor_fator = np.zeros(len(ativos))

    for id_ativo, ativo in ativos.items():
        vetor_fator[posicoes_dos_ativos[id_ativo]] = ativo.fator_exposicao

    return vetor_fator


def montar_vetor_cvss(catalogo, posicoes_das_vulns):
    vetor_cvss = np.zeros(len(catalogo))

    for id_vulnerabilidade, vulnerabilidade in catalogo.items():
        vetor_cvss[posicoes_das_vulns[id_vulnerabilidade]] = vulnerabilidade.cvss

    return vetor_cvss


def calcular_risco_proprio(ativos, catalogo):
    linha_do_ativo = mapear_ids_para_posicoes(ativos)
    coluna_da_vuln = mapear_ids_para_posicoes(catalogo)

    matriz_m = montar_matriz_m(ativos, catalogo, linha_do_ativo, coluna_da_vuln)
    vetor_cvss = montar_vetor_cvss(catalogo, coluna_da_vuln)
    vetor_f = montar_vetor_fator(ativos, linha_do_ativo)

    return vetor_f * (matriz_m @ vetor_cvss)
