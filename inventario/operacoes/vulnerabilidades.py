from inventario.entradas import pedir_cvss, pedir_info, pedir_int, pedir_status_vulnerabilidade
from inventario.operacoes.ativos import encontrar_ativo, obter_ativo
from inventario.dominio.excecoes import DadoInvalidoError
from inventario.dominio.vulnerabilidade import Vulnerabilidade
from inventario.persistencia import salvar_catalogo, salvar_dados


def proximo_id(dicionario):

    maior_id = 0

    for id_existente in dicionario:
        if id_existente > maior_id:
            maior_id = id_existente

    return maior_id + 1


def cadastrar_vulnerabilidade(catalogo):
    nome_vulnerabilidade = pedir_info("Digite o nome da vulnerabilidade: ")
    cvss = pedir_cvss("Digite a nota CVSS da vulnerabilidade (0.1 a 10): ")

    vulnerabilidade = registrar_vulnerabilidade(catalogo, nome_vulnerabilidade, cvss)

    mostrar_vulnerabilidade(vulnerabilidade)

    return vulnerabilidade


def registrar_vulnerabilidade(catalogo, nome_vulnerabilidade, cvss):
    id_vulnerabilidade = proximo_id(catalogo)  # regra: nunca repete ID

    vulnerabilidade = Vulnerabilidade(id_vulnerabilidade, nome_vulnerabilidade, cvss)
    catalogo[id_vulnerabilidade] = vulnerabilidade  # guarda no catálogo
    salvar_catalogo(catalogo)  # cozinha guarda na despensa

    return vulnerabilidade


def mostrar_vulnerabilidade(vulnerabilidade, status_tratamento=None):

    print(f"""
    ID: {vulnerabilidade.id_vulnerabilidade}
    Vulnerabilidade: {vulnerabilidade.nome_vulnerabilidade}
    CVSS: {vulnerabilidade.cvss}
    Nível: {vulnerabilidade.nivel().name.lower()}""")

    if status_tratamento is not None:
        print(f"    Status neste ativo: {status_tratamento.name.lower()}")


def vincular_vulnerabilidade(ativos, catalogo, id_ativo, id_vulnerabilidade, status_tratamento):
    ativo = obter_ativo(ativos, id_ativo)  # lança erro se o ativo não existir

    if id_vulnerabilidade not in catalogo:
        raise DadoInvalidoError("Vulnerabilidade não encontrada no catálogo.")

    if id_vulnerabilidade in ativo.vulnerabilidades:
        raise DadoInvalidoError("Esta vulnerabilidade já está vinculada a este ativo.")

    ativo.vulnerabilidades[id_vulnerabilidade] = status_tratamento
    salvar_dados(ativos)  # cozinha guarda na despensa


def desvincular_vulnerabilidade(ativos, id_ativo, id_vulnerabilidade):
    ativo = obter_ativo(ativos, id_ativo)

    if id_vulnerabilidade not in ativo.vulnerabilidades:
        raise DadoInvalidoError("Esta vulnerabilidade não está vinculada a este ativo.")

    del ativo.vulnerabilidades[id_vulnerabilidade]
    salvar_dados(ativos)


def mostrar_vulnerabilidades_do_ativo(ativo, catalogo):
    for id_vulnerabilidade, status_tratamento in ativo.vulnerabilidades.items():
        vulnerabilidade = catalogo[id_vulnerabilidade]
        mostrar_vulnerabilidade(vulnerabilidade, status_tratamento)


def atualizar_status_vulnerabilidade(ativos, id_ativo, id_vulnerabilidade, novo_status):
    ativo = obter_ativo(ativos, id_ativo)

    if id_vulnerabilidade not in ativo.vulnerabilidades:
        raise DadoInvalidoError(
            "Este ativo não possui nenhuma vulnerabilidade com este ID vinculada a ele."
        )

    ativo.vulnerabilidades[id_vulnerabilidade] = novo_status
    salvar_dados(ativos)


def encontrar_vulnerabilidade(catalogo):

    if not catalogo:
        print("Nenhuma vulnerabilidade cadastrada.")
        return None

    for vulnerabilidade in catalogo.values():
        mostrar_vulnerabilidade(vulnerabilidade)

    id_vulnerabilidade = pedir_int("Digite o ID da vulnerabilidade: ")
    vulnerabilidade_encontrada = catalogo.get(id_vulnerabilidade)

    if not vulnerabilidade_encontrada:
        print("Vulnerabilidade não encontrada.")
        return None

    return vulnerabilidade_encontrada


def excluir_vulnerabilidade_do_catalogo(catalogo, ativos, id_vulnerabilidade):
    if id_vulnerabilidade not in catalogo:
        raise DadoInvalidoError("Vulnerabilidade não encontrada no catálogo.")

    for ativo in ativos.values():
        if id_vulnerabilidade in ativo.vulnerabilidades:
            del ativo.vulnerabilidades[id_vulnerabilidade]  # tira de todo ativo que a tinha

    del catalogo[id_vulnerabilidade]
    salvar_catalogo(catalogo)  # salva uma vez só, no final
    salvar_dados(ativos)


def confirmar_exclusao_vuln(vulnerabilidade):

    print(
        f'Tem certeza que deseja excluir a vulnerabilidade "{vulnerabilidade.nome_vulnerabilidade}" (ID {vulnerabilidade.id_vulnerabilidade})?'
    )
    resposta = input('Digite "sim" para excluir ou tecle enter para voltar: ').strip().lower()

    if resposta == "sim":
        return True
    else:
        return False


def editar_vulnerabilidade(vulnerabilidade):
    print("""
    1 - Editar nome
    2 - Editar CVSS
    3 - Voltar""")

    opcao_edicao = input("Escolha uma opção: ").strip()

    if opcao_edicao == "1":
        novo_nome = pedir_info("Digite o novo nome da vulnerabilidade: ")
        vulnerabilidade.nome_vulnerabilidade = novo_nome
        print("Nome atualizado com sucesso!")
        mostrar_vulnerabilidade(vulnerabilidade)
        return True

    elif opcao_edicao == "2":
        novo_cvss = pedir_cvss("Digite a nova nota CVSS (0.1 a 10): ")
        vulnerabilidade.cvss = novo_cvss
        print("CVSS atualizado com sucesso!")
        mostrar_vulnerabilidade(vulnerabilidade)
        return True

    elif opcao_edicao == "3":
        print("Voltando ao menu de vulnerabilidades...")
        return False

    else:
        print("Opção inválida. Tente novamente.")
        return False


def vincular_a_um_ativo(vulnerabilidade, ativos, catalogo):
    ativo_encontrado = encontrar_ativo(ativos)

    if not ativo_encontrado:
        return False

    status_tratamento = pedir_status_vulnerabilidade("Digite o status: ")

    try:
        vincular_vulnerabilidade(
            ativos,
            catalogo,
            ativo_encontrado.id,
            vulnerabilidade.id_vulnerabilidade,
            status_tratamento,
        )
    except DadoInvalidoError as erro:
        print(erro)
        return False

    print(f"Vulnerabilidade vinculada com sucesso!\n{ativo_encontrado.exibir_detalhes()}")
    mostrar_vulnerabilidade(vulnerabilidade, status_tratamento)
    return True
