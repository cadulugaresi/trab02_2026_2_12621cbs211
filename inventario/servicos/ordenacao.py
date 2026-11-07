def por_id(ativo):
    return ativo.id


def por_nome(ativo):
    return ativo.nome.lower()


def por_quantidade_de_vulnerabilidades(ativo):
    return -len(ativo.vulnerabilidades)


CRITERIOS_DE_ORDENACAO = {
    "id": por_id,
    "nome": por_nome,
    "vulnerabilidades": por_quantidade_de_vulnerabilidades,
}


def listar_ativos_ordenados(ativos, criterio):
    return sorted(ativos.values(), key=criterio)
