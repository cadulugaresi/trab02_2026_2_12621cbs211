from inventario.dominio.ativo import Impressora, Notebook, Roteador, Servidor
from inventario.dominio.excecoes import DadoInvalidoError
from inventario.interface.entradas import (
    pedir_cor,
    pedir_float,
    pedir_info,
    pedir_int,
    pedir_setor,
    pedir_status,
    pedir_tecnologia,
    pedir_tipo,
)
from inventario.servicos.ativos import (
    atualizar_ativo_no_inventario,
    encontrar_ativo_por_id,
    obter_ativo,
    registrar_ativo_no_inventario,
    remover_ativo_do_inventario,
)
from inventario.servicos.ordenacao import (
    listar_ativos_ordenados,
    por_nome,
)


def pedir_id_disponivel(ativos):

    while True:

        id_do_ativo = pedir_int("Digite o ID do ativo: ")
        if encontrar_ativo_por_id(ativos, id_do_ativo) is None:
            return id_do_ativo

        print("Já existe um ativo cadastrado com este ID. Tente outro.")


def cadastro_notebook():

    so = pedir_info("Digite o sistema operacional do ativo: ")
    tela = pedir_float("Digite o tamanho da tela em polegadas: ")

    return so, tela


def cadastro_roteador():

    portas = pedir_int("Digite a quantidade de portas do roteador: ")
    velocidade = pedir_int("Digite a velocidade do roteador em MB: ")

    return portas, velocidade


def cadastro_servidor():

    ram = pedir_int("Digite a quantidade de RAM do Servidor em GB: ")
    armazenamento = pedir_float("Digite a quantidade de armazenamento do Servidor em T: ")

    return ram, armazenamento


def cadastro_impressora():
    cor = pedir_cor()
    tecnologia = pedir_tecnologia()
    return cor, tecnologia


def cadastrar_ativo(repositorio, ativos):

    tipo = pedir_tipo("Digite o tipo do ativo: ")
    id_do_ativo = pedir_id_disponivel(ativos)
    nome_ativo = pedir_info("Digite o nome do ativo: ")
    setor = pedir_setor("Digite o setor do ativo: ")
    responsavel = pedir_info("Digite o nome do responsável pelo ativo: ")
    status = pedir_status("Digite o status do ativo: ")

    if tipo is Notebook:
        so, tela = cadastro_notebook()
        ativo = Notebook(id_do_ativo, nome_ativo, setor, responsavel, status, so, tela)

    elif tipo is Roteador:
        portas, velocidade = cadastro_roteador()
        ativo = Roteador(id_do_ativo, nome_ativo, setor, responsavel, status, portas, velocidade)

    elif tipo is Servidor:
        ram, armazenamento = cadastro_servidor()
        ativo = Servidor(id_do_ativo, nome_ativo, setor, responsavel, status, ram, armazenamento)

    elif tipo is Impressora:
        cor, tecnologia = cadastro_impressora()
        ativo = Impressora(id_do_ativo, nome_ativo, setor, responsavel, status, cor, tecnologia)

    registrar_ativo_no_inventario(repositorio, ativos, ativo)
    print("Ativo cadastrado com sucesso!")
    print(ativo.exibir_detalhes())
    return ativo


def editar_ativo(repositorio, ativos):

    ativo_encontrado = perguntar_ativo(ativos, "Digite o ID do ativo: ")
    if ativo_encontrado is None:
        return

    print("\n=== Dados atuais do ativo ===\n")
    print(
        f"ID: {ativo_encontrado.id}\n"
        f"Nome: {ativo_encontrado.nome}\n"
        f"Responsável: {ativo_encontrado.responsavel}\n"
        f"Tipo: {type(ativo_encontrado).__name__}\n"
        f"Setor: {ativo_encontrado.setor.name}\n"
        f"Status: {ativo_encontrado.status.name}"
    )

    while True:
        print("\n=== Menu de edição ===\n")
        print(
            "1 - Editar responsável\n"
            "2 - Editar status\n"
            "3 - Editar setor\n"
            "4 - Editar detalhes específicos\n"
            "5 - Editar tipo\n"
            "6 - Voltar"
        )

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            novo_responsavel = pedir_info("Digite o novo nome do responsável pelo ativo: ")
            ativo_encontrado.responsavel = novo_responsavel
            print("Responsável atualizado com sucesso.")
            print(f"Novo responsável: {novo_responsavel}.")

        elif opcao == "2":
            novo_status = pedir_status("Digite o novo status do ativo: ")
            ativo_encontrado.status = novo_status
            print("Status do ativo atualizado com sucesso.")
            print(f"Status atual: {novo_status.name}.")

        elif opcao == "3":
            novo_setor = pedir_setor("Digite o novo setor do ativo: ")
            ativo_encontrado.setor = novo_setor
            print("Setor do ativo atualizado com sucesso.")
            print(f"Setor atual: {novo_setor.name}.")

        elif opcao == "4":

            if isinstance(ativo_encontrado, Notebook):
                ativo_encontrado.sistema_operacional = pedir_info("Novo SO: ")
                ativo_encontrado.tela = pedir_float("Nova tela: ")

            elif isinstance(ativo_encontrado, Roteador):
                ativo_encontrado.portas = pedir_int("Nova quantidade de portas: ")
                ativo_encontrado.velocidade = pedir_int("Nova velocidade em MB: ")

            elif isinstance(ativo_encontrado, Servidor):
                ativo_encontrado.ram = pedir_int("Digite a quantidade de RAM do Servidor em GB: ")
                ativo_encontrado.armazenamento = pedir_float(
                    "Digite a quantidade de armazenamento do Servidor em T: "
                )

            elif isinstance(ativo_encontrado, Impressora):
                ativo_encontrado.cor = pedir_cor()
                ativo_encontrado.tecnologia = pedir_tecnologia()

            print("Detalhes específicos atualizados com sucesso!")
            print("Ativo atualizado:")
            print(ativo_encontrado.exibir_detalhes())

        elif opcao == "5":

            novo_tipo = pedir_tipo("Qual o novo tipo do ativo? ")

            if novo_tipo is Notebook:
                so, tela = cadastro_notebook()
                novo_ativo = Notebook(
                    ativo_encontrado.id,
                    ativo_encontrado.nome,
                    ativo_encontrado.setor,
                    ativo_encontrado.responsavel,
                    ativo_encontrado.status,
                    so,
                    tela,
                )
            elif novo_tipo is Roteador:
                portas, velocidade = cadastro_roteador()
                novo_ativo = Roteador(
                    ativo_encontrado.id,
                    ativo_encontrado.nome,
                    ativo_encontrado.setor,
                    ativo_encontrado.responsavel,
                    ativo_encontrado.status,
                    portas,
                    velocidade,
                )
            elif novo_tipo is Servidor:
                ram, armazenamento = cadastro_servidor()
                novo_ativo = Servidor(
                    ativo_encontrado.id,
                    ativo_encontrado.nome,
                    ativo_encontrado.setor,
                    ativo_encontrado.responsavel,
                    ativo_encontrado.status,
                    ram,
                    armazenamento,
                )
            elif novo_tipo is Impressora:
                cor, tecnologia = cadastro_impressora()
                novo_ativo = Impressora(
                    ativo_encontrado.id,
                    ativo_encontrado.nome,
                    ativo_encontrado.setor,
                    ativo_encontrado.responsavel,
                    ativo_encontrado.status,
                    cor,
                    tecnologia,
                )

            ativo_encontrado = novo_ativo
            print("Tipo do ativo atualizado com sucesso!")
            print(f"Tipo atual: {type(novo_ativo).__name__}.")

        elif opcao == "6":
            atualizar_ativo_no_inventario(repositorio, ativos, ativo_encontrado)
            print("Voltando...")
            break

        else:
            print("Opção inválida.")


def excluir_ativo(repositorio, ativos):
    ativo = perguntar_ativo(ativos, "Digite o ID do ativo: ")
    if ativo is None:
        return

    if not confirmar_exclusao(ativo):
        print("Exclusão cancelada.")
        return

    remover_ativo_do_inventario(repositorio, ativos, ativo.id)
    print("Ativo excluído com sucesso!")


def confirmar_exclusao(ativo):

    print(f'Tem certeza que deseja excluir o ativo "{ativo.nome}" (ID {ativo.id})?')
    resposta = input('Digite "sim" para excluir ou tecle enter para voltar: ').strip().lower()

    if resposta == "sim":
        return True
    else:
        return False


def perguntar_ativo(ativos, mensagem):

    if not ativos:
        print("Nenhum ativo cadastrado.")
        return None

    id_ativo = pedir_int(mensagem)

    try:
        return obter_ativo(ativos, id_ativo)
    except DadoInvalidoError as erro:
        print(erro)
        return None


def escolher_ativo_com_vulnerabilidades(ativos):
    ativo_encontrado = perguntar_ativo(ativos, "Digite o ID do ativo: ")
    if ativo_encontrado is None:
        return None
    elif not ativo_encontrado.vulnerabilidades:
        print("Nenhuma vulnerabilidade vinculada a este ativo.")
        return None
    else:
        return ativo_encontrado


def mostrar_lista_de_ativos(ativos):
    for ativo in listar_ativos_ordenados(ativos, por_nome):
        mostrar_cabecalho_do_ativo(ativo)


def mostrar_cabecalho_do_ativo(ativo):
    print(f"{ativo.id} - {ativo.nome} ({type(ativo).__name__})")
