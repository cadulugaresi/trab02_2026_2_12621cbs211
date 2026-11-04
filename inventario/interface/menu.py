from inventario.dominio.excecoes import DadoInvalidoError
from inventario.interface.entradas import (
    pedir_info,
    pedir_int,
    pedir_status,
    pedir_status_vulnerabilidade,
    pedir_tipo,
)

from inventario.interface.ativos import (
    cadastrar_ativo,
    editar_ativo,
    escolher_ativo_com_vulnerabilidades,
    excluir_ativo,
)
from inventario.interface.vulnerabilidades import (
    cadastrar_vulnerabilidade,
    confirmar_exclusao_vuln,
    editar_vulnerabilidade,
    encontrar_vulnerabilidade,
    mostrar_vulnerabilidade,
    mostrar_vulnerabilidades_do_ativo,
    vincular_a_um_ativo,
)
from inventario.servicos.ativos import (
    encontrar_ativo_por_id,
    encontrar_ativo_por_nome,
    encontrar_ativos_por_status,
    listar_ativos_por_tipo,
)
from inventario.servicos.vulnerabilidades import (
    atualizar_status_vulnerabilidade,
    desvincular_vulnerabilidade,
    excluir_vulnerabilidade_do_catalogo,
)


def menu_principal(ativos, catalogo):
    while True:

        try:

            print("""
            MENU

            1 - Cadastrar ativo
            2 - Listar ativo
            3 - Excluir ativo
            4 - Menu de vulnerabilidades
            5 - Editar ativo
            6 - Sair
            """)

            opcao = input("Escolha uma opção: ").strip()

            if opcao == "1":
                cadastrar_ativo(ativos)

            elif opcao == "2":
                menu_listagem(ativos)

            elif opcao == "3":
                excluir_ativo(ativos)

            elif opcao == "4":
                menu_vulnerabilidades(ativos, catalogo)

            elif opcao == "5":
                editar_ativo(ativos)

            elif opcao == "6":
                print("Saindo do programa...")
                break

            else:
                print("Opção inválida. Tente novamente.")

        except (EOFError, KeyboardInterrupt):
            print("Programa encerrado pelo usuário.")
            break


def menu_vulnerabilidades(ativos, catalogo):
    while True:
        print("""MENU DE VULNERABILIDADES

                1 - Cadastrar vulnerabilidade
                2 - Listar catálogo de vulnerabilidades
                3 - Vincular vulnerabilidade a um ativo
                4 - Listar vulnerabilidades de um ativo
                5 - Atualizar status da vulnerabilidade em um ativo
                6 - Desvincular vulnerabilidade de um ativo
                7 - Excluir vulnerabilidade do catálogo
                8 - Editar vulnerabilidade no catálogo
                9 - Voltar ao menu principal""")

        opcao_vulnerabilidade = input("Escolha uma opção: ").strip()

        if opcao_vulnerabilidade == "1":
            nova_vulnerabilidade = cadastrar_vulnerabilidade(catalogo)
            resposta = (
                input(
                    "Deseja vincular a um ativo agora? (Tecle 'sim'para confirmar ou enter para seguir sem vincular): "
                )
                .strip()
                .lower()
            )
            if resposta in ("sim", "s"):
                vincular_a_um_ativo(nova_vulnerabilidade, ativos, catalogo)
            else:
                print("Nova vulnerabilidade criada com sucesso!\nNão vinculada a nenhum ativo.")

        elif opcao_vulnerabilidade == "2":
            if not catalogo:
                print("Nenhuma vulnerabilidade cadastrada no catálogo.")
            else:
                print("Listando catálogo de vulnerabilidades...")
                for vulnerabilidade in catalogo.values():
                    mostrar_vulnerabilidade(vulnerabilidade)

        elif opcao_vulnerabilidade == "3":
            vulnerabilidade_encontrada = encontrar_vulnerabilidade(catalogo)

            if vulnerabilidade_encontrada:
                vincular_a_um_ativo(vulnerabilidade_encontrada, ativos, catalogo)

        elif opcao_vulnerabilidade == "4":
            ativo_encontrado = escolher_ativo_com_vulnerabilidades(ativos)
            if ativo_encontrado:
                mostrar_vulnerabilidades_do_ativo(ativo_encontrado, catalogo)

        elif opcao_vulnerabilidade == "5":
            ativo_encontrado = escolher_ativo_com_vulnerabilidades(ativos)

            if ativo_encontrado:
                mostrar_vulnerabilidades_do_ativo(ativo_encontrado, catalogo)
                id_vulnerabilidade = pedir_int(
                    "Digite o ID da vulnerabilidade cujo status deseja editar: "
                )
                novo_status = pedir_status_vulnerabilidade("Novo status: ")

                try:
                    atualizar_status_vulnerabilidade(
                        ativos, ativo_encontrado.id, id_vulnerabilidade, novo_status
                    )
                    print(f"Status atualizado com sucesso! Novo status: {novo_status.name.lower()}")
                except DadoInvalidoError as erro:
                    print(erro)

        elif opcao_vulnerabilidade == "6":
            ativo_encontrado = escolher_ativo_com_vulnerabilidades(ativos)

            if ativo_encontrado:
                mostrar_vulnerabilidades_do_ativo(ativo_encontrado, catalogo)
                id_vulnerabilidade = pedir_int(
                    "Digite o ID da vulnerabilidade que deseja desvincular do ativo: "
                )

                try:
                    desvincular_vulnerabilidade(ativos, ativo_encontrado.id, id_vulnerabilidade)
                    print("Vulnerabilidade desvinculada com sucesso!")
                except DadoInvalidoError as erro:
                    print(erro)

        elif opcao_vulnerabilidade == "7":
            print("Excluindo vulnerabilidade...")
            vulnerabilidade_a_excluir = encontrar_vulnerabilidade(catalogo)

            if vulnerabilidade_a_excluir:
                confirmou = confirmar_exclusao_vuln(vulnerabilidade_a_excluir)

                if confirmou:
                    excluir_vulnerabilidade_do_catalogo(
                        catalogo, ativos, vulnerabilidade_a_excluir.id_vulnerabilidade
                    )
                    print(
                        f'Vulnerabilidade "{vulnerabilidade_a_excluir.nome_vulnerabilidade}" excluída com sucesso!'
                    )
                else:
                    print("Exclusão cancelada.")

        elif opcao_vulnerabilidade == "8":
            vulnerabilidade = encontrar_vulnerabilidade(catalogo)

            if vulnerabilidade:
                editar_vulnerabilidade(vulnerabilidade, catalogo)

        elif opcao_vulnerabilidade == "9":
            print("Voltando ao menu principal...")
            break

        else:
            print("Opção inválida. Tente novamente.")


def menu_listagem(ativos):
    todos_ou_um = ""
    while todos_ou_um not in ("todos", "um", "filtrar"):
        print("Deseja listar todos os ativos, filtrar ou mostrar apenas um?")
        todos_ou_um = input("todos/filtrar/um): ").strip().lower()

        if todos_ou_um == "todos":
            if ativos:
                print("Listando todos os ativos...")
                for ativo in ativos.values():
                    print(ativo.exibir_detalhes())
            else:
                print("Nenhum ativo cadastrado.")

        elif todos_ou_um == "filtrar":

            if not ativos:
                print("Nenhum ativo cadastrado.")
                continue

            print("""
            1 - Tipo
            2 - Status
            """)

            filtro = input("Deseja filtrar por TIPO ou STATUS do ativo?").strip()

            if filtro == "1":
                tipo = pedir_tipo("Qual tipo de ativos deseja listar? ")
                encontrados = listar_ativos_por_tipo(tipo, ativos)

            elif filtro == "2":
                status = pedir_status("Qual status de ativos deseja listar? ")
                encontrados = encontrar_ativos_por_status(status, ativos)

            else:
                print("Opção inválida.")
                continue

            if encontrados:
                for ativo in encontrados:
                    print(ativo.exibir_detalhes())

            else:
                print("Nenhum ativo encontrado com este filtro.")

        elif todos_ou_um == "um":

            nome_ou_id = ""

            while nome_ou_id not in ("nome", "id"):
                nome_ou_id = input("Deseja buscar ativo por NOME ou ID? (nome/id) ").strip().lower()

                if nome_ou_id == "nome":

                    nome = pedir_info("Digite o nome do ativo que deseja listar: ")
                    encontrados = encontrar_ativo_por_nome(nome, ativos)

                    if encontrados:
                        for ativo in encontrados:
                            print(ativo.exibir_detalhes())
                    else:
                        print("Nenhum ativo encontrado.")
                elif nome_ou_id == "id":

                    id_ativo = pedir_int("Digite o ID do ativo que deseja listar: ")
                    ativo_encontrado = encontrar_ativo_por_id(id_ativo, ativos)

                    if ativo_encontrado:
                        print(ativo_encontrado.exibir_detalhes())
                    else:
                        print("Nenhum ativo encontrado.")
                else:
                    print('Opção inválida. Digite "nome" ou "id".')

        else:
            print('Opção inválida. Digite "todos" ou "um".')
