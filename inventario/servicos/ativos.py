from inventario.dominio.excecoes import DadoInvalidoError, RecursoNaoEncontradoError


def registrar_ativo_no_inventario(repositorio, ativos, ativo):
    ativo.validar_dados()
    if ativo.id in ativos:
        raise DadoInvalidoError("Já existe um ativo cadastrado com este ID.")

    repositorio.adicionar_ativo(ativo)
    ativos[ativo.id] = ativo


def encontrar_ativo_por_id(ativos, id_ativo):
    return ativos.get(id_ativo)


def obter_ativo(ativos, id_ativo):
    ativo = encontrar_ativo_por_id(ativos, id_ativo)

    if ativo is None:
        raise RecursoNaoEncontradoError("Ativo não encontrado.")

    return ativo


def encontrar_ativos_por_nome(ativos, nome):

    encontrados = []

    for ativo in ativos.values():
        if nome.lower() in ativo.nome.lower():
            encontrados.append(ativo)

    return encontrados


def encontrar_ativos_por_status(ativos, status):
    encontrados = []
    for ativo in ativos.values():
        if ativo.status == status:
            encontrados.append(ativo)
    return encontrados


def encontrar_ativos_por_tipo(ativos, classe):

    encontrados = []

    for ativo in ativos.values():
        if isinstance(ativo, classe):
            encontrados.append(ativo)

    return encontrados


def atualizar_ativo_no_inventario(repositorio, ativos, ativo_atualizado):
    ativo_atualizado.validar_dados()
    ativo_antigo = obter_ativo(ativos, ativo_atualizado.id)
    ativo_atualizado.vulnerabilidades = ativo_antigo.vulnerabilidades
    ativo_atualizado.dependencias = ativo_antigo.dependencias
    repositorio.atualizar_ativo(ativo_atualizado)
    ativos[ativo_atualizado.id] = ativo_atualizado


def remover_ativo_do_inventario(repositorio, ativos, id_ativo):
    obter_ativo(ativos, id_ativo)
    repositorio.remover_ativo(id_ativo)
    del ativos[id_ativo]

    for ativo in ativos.values():
        ativo.dependencias.pop(id_ativo, None)
