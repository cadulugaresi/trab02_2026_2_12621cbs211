import copy

from inventario.dominio.excecoes import DadoInvalidoError
from inventario.interface.ativos import perguntar_ativo
from inventario.interface.entradas import (
    pedir_cvss,
    pedir_info,
    pedir_int,
    pedir_status_vulnerabilidade,
)
from inventario.servicos.vulnerabilidades import (
    registrar_vulnerabilidade_no_catalogo,
    vincular_vulnerabilidade,
    atualizar_vulnerabilidade_no_catalogo,
)


def cadastrar_vulnerabilidade(repositorio, catalogo):
    nome_vulnerabilidade = pedir_info("Digite o nome da vulnerabilidade: ")
    cvss = pedir_cvss("Digite a nota CVSS da vulnerabilidade (0.1 a 10): ")

    vulnerabilidade = registrar_vulnerabilidade_no_catalogo(
        repositorio, catalogo, nome_vulnerabilidade, cvss
    )

    mostrar_vulnerabilidade(vulnerabilidade)

    return vulnerabilidade


def mostrar_vulnerabilidade(vulnerabilidade, status_tratamento=None):

    print(
        f"\nID: {vulnerabilidade.id_vulnerabilidade}\n"
        f"Vulnerabilidade: {vulnerabilidade.nome_vulnerabilidade}\n"
        f"CVSS: {vulnerabilidade.cvss}\n"
        f"Nível: {vulnerabilidade.nivel().name.lower()}"
    )

    if status_tratamento is not None:
        print(f"Status neste ativo: {status_tratamento.name.lower()}")


def mostrar_vulnerabilidades_do_ativo(ativo, catalogo):
    for id_vulnerabilidade, status_tratamento in ativo.vulnerabilidades.items():
        vulnerabilidade = catalogo[id_vulnerabilidade]
        mostrar_vulnerabilidade(vulnerabilidade, status_tratamento)


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


def confirmar_exclusao_vuln(vulnerabilidade):

    print(
        f'Tem certeza que deseja excluir a vulnerabilidade "{vulnerabilidade.nome_vulnerabilidade}" (ID {vulnerabilidade.id_vulnerabilidade})?'
    )
    resposta = input('Digite "sim" para excluir ou tecle enter para voltar: ').strip().lower()

    if resposta == "sim":
        return True
    else:
        return False


def editar_vulnerabilidade(repositorio, vulnerabilidade, catalogo):
    vulnerabilidade_em_edicao = copy.copy(vulnerabilidade)
    print("\n1 - Editar nome\n2 - Editar CVSS\n3 - Voltar")

    opcao_edicao = input("Escolha uma opção: ").strip()

    if opcao_edicao == "1":
        novo_nome = pedir_info("Digite o novo nome da vulnerabilidade: ")
        vulnerabilidade_em_edicao.nome_vulnerabilidade = novo_nome

    elif opcao_edicao == "2":
        novo_cvss = pedir_cvss("Digite a nova nota CVSS (0.1 a 10): ")
        vulnerabilidade_em_edicao.cvss = novo_cvss

    elif opcao_edicao == "3":
        print("Voltando ao menu de vulnerabilidades...")
        return

    else:
        print("Opção inválida. Tente novamente.")
        return

    try:
        atualizar_vulnerabilidade_no_catalogo(repositorio, catalogo, vulnerabilidade_em_edicao)
    except DadoInvalidoError as erro:
        print(erro)
        print("As alterações não foram salvas.")
        return

    print("Vulnerabilidade atualizada com sucesso!")
    mostrar_vulnerabilidade(vulnerabilidade_em_edicao)


def vincular_a_um_ativo(repositorio, vulnerabilidade, ativos, catalogo):
    ativo_encontrado = perguntar_ativo(ativos, "Digite o ID do ativo: ")

    if not ativo_encontrado:
        return False

    status_tratamento = pedir_status_vulnerabilidade("Digite o status: ")

    try:
        vincular_vulnerabilidade(
            repositorio,
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
