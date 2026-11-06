from inventario.dominio.excecoes import DadoInvalidoError


def registrar_ativo_no_inventario(repositorio, ativos, ativo):
    if ativo.id in ativos:
        raise DadoInvalidoError("Já existe um ativo cadastrado com este ID.")

    ativos[ativo.id] = ativo
    repositorio.salvar_ativos(ativos)


def encontrar_ativo_por_id(ID, ativos):
    return ativos.get(ID)


def obter_ativo(ativos, id_ativo):
    ativo = encontrar_ativo_por_id(id_ativo, ativos)

    if ativo is None:
        raise DadoInvalidoError("Ativo não encontrado.")

    return ativo


def encontrar_ativo_por_nome(nome, ativos):

    encontrados = []

    for ativo in ativos.values():
        if nome.lower() in ativo.nome.lower():
            encontrados.append(ativo)

    return encontrados


def encontrar_ativos_por_status(status, ativos):
    encontrados = []
    for ativo in ativos.values():
        if ativo.status == status:
            encontrados.append(ativo)
    return encontrados


def listar_ativos_por_tipo(classe, ativos):

    encontrados = []

    for ativo in ativos.values():
        if isinstance(ativo, classe):
            encontrados.append(ativo)

    return encontrados


def atualizar_ativo_no_inventario(repositorio, ativos, ativo_atualizado):
    ativo_antigo = obter_ativo(ativos, ativo_atualizado.id)
    ativo_atualizado.vulnerabilidades = ativo_antigo.vulnerabilidades
    ativos[ativo_atualizado.id] = ativo_atualizado
    repositorio.salvar_ativos(ativos)


def remover_ativo_do_inventario(repositorio, ativos, id_ativo):
    obter_ativo(ativos, id_ativo)
    del ativos[id_ativo]
    repositorio.salvar_ativos(ativos)
