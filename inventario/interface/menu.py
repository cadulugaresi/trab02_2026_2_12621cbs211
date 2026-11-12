from inventario.dominio.excecoes import DadoInvalidoError, PersistenciaError
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
    mostrar_cabecalho_do_ativo,
    mostrar_lista_de_ativos,
    perguntar_ativo,
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
from inventario.interface.riscos import analisar_risco
from inventario.servicos.ativos import (
    encontrar_ativo_por_id,
    encontrar_ativos_por_nome,
    encontrar_ativos_por_status,
    encontrar_ativos_por_tipo,
)
from inventario.servicos.vulnerabilidades import (
    atualizar_status_vulnerabilidade,
    desvincular_vulnerabilidade,
    excluir_vulnerabilidade_do_catalogo,
)

from inventario.interface.dependencias import (
    mostrar_dependencias,
    atualizar_dependencia_menu,
    cadastrar_dependencia_menu,
    excluir_dependencia_menu,
)

from inventario.servicos.ordenacao import (
    listar_ativos_ordenados,
    CRITERIOS_DE_ORDENACAO,
    por_nome,
)


def menu_principal(repositorio, ativos, catalogo):
    while True:

        try:

            print("\n=== Menu principal ===\n")
            print(
                "1 - Cadastrar ativo\n"
                "2 - Listar ativo\n"
                "3 - Excluir ativo\n"
                "4 - Menu de vulnerabilidades\n"
                "5 - Editar ativo\n"
                "6 - Menu de dependências\n"
                "7 - Análise de risco\n"
                "8 - Sair"
            )

            opcao = input("Escolha uma opção: ").strip()

            if opcao == "1":
                cadastrar_ativo(repositorio, ativos)

            elif opcao == "2":
                menu_listagem(ativos)

            elif opcao == "3":
                excluir_ativo(repositorio, ativos)

            elif opcao == "4":
                menu_vulnerabilidades(repositorio, ativos, catalogo)

            elif opcao == "5":
                editar_ativo(repositorio, ativos)

            elif opcao == "6":
                if len(ativos) < 2:
                    print(
                        "É preciso ter pelo menos dois ativos cadastrados para acessar o menu de dependências."
                    )
                else:
                    menu_dependencias(repositorio, ativos)

            elif opcao == "7":
                analisar_risco(ativos, catalogo)

            elif opcao == "8":
                print("Saindo do programa...")
                break

            else:
                print("Opção inválida. Tente novamente.")

        except (EOFError, KeyboardInterrupt):
            print("Programa encerrado pelo usuário.")
            break

        except PersistenciaError as erro:
            print(erro)


def menu_vulnerabilidades(repositorio, ativos, catalogo):
    while True:
        print("\n=== Menu de vulnerabilidades ===\n")
        print(
            "1 - Cadastrar vulnerabilidade\n"
            "2 - Listar catálogo de vulnerabilidades\n"
            "3 - Vincular vulnerabilidade a um ativo\n"
            "4 - Listar vulnerabilidades de um ativo\n"
            "5 - Atualizar status da vulnerabilidade em um ativo\n"
            "6 - Desvincular vulnerabilidade de um ativo\n"
            "7 - Excluir vulnerabilidade do catálogo\n"
            "8 - Editar vulnerabilidade no catálogo\n"
            "9 - Voltar ao menu principal"
        )

        opcao_vulnerabilidade = input("Escolha uma opção: ").strip()

        if opcao_vulnerabilidade == "1":
            nova_vulnerabilidade = cadastrar_vulnerabilidade(repositorio, catalogo)
            resposta = (
                input(
                    "Deseja vincular a um ativo agora? (Tecle 'sim'para confirmar ou enter para seguir sem vincular): "
                )
                .strip()
                .lower()
            )
            if resposta in ("sim", "s"):
                vincular_a_um_ativo(repositorio, nova_vulnerabilidade, ativos, catalogo)
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
                vincular_a_um_ativo(repositorio, vulnerabilidade_encontrada, ativos, catalogo)

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
                        repositorio, ativos, ativo_encontrado.id, id_vulnerabilidade, novo_status
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
                    desvincular_vulnerabilidade(
                        repositorio, ativos, ativo_encontrado.id, id_vulnerabilidade
                    )
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
                        repositorio, catalogo, ativos, vulnerabilidade_a_excluir.id_vulnerabilidade
                    )
                    print(
                        f'Vulnerabilidade "{vulnerabilidade_a_excluir.nome_vulnerabilidade}" excluída com sucesso!'
                    )
                else:
                    print("Exclusão cancelada.")

        elif opcao_vulnerabilidade == "8":
            vulnerabilidade = encontrar_vulnerabilidade(catalogo)

            if vulnerabilidade:
                editar_vulnerabilidade(repositorio, vulnerabilidade, catalogo)

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
                opcoes = "/".join(CRITERIOS_DE_ORDENACAO)

                criterio_escolhido = ""
                while criterio_escolhido not in CRITERIOS_DE_ORDENACAO:
                    criterio_escolhido = input(f"Ordenar por ({opcoes}): ").strip().lower()

                estrategia = CRITERIOS_DE_ORDENACAO[criterio_escolhido]

                print("Listando todos os ativos...")
                for ativo in listar_ativos_ordenados(ativos, estrategia):
                    print(ativo.exibir_detalhes())

        elif todos_ou_um == "filtrar":

            if not ativos:
                print("Nenhum ativo cadastrado.")
                continue

            print("\n1 - Tipo\n2 - Status")

            filtro = input("Deseja filtrar por TIPO ou STATUS do ativo?").strip()

            if filtro == "1":
                tipo = pedir_tipo("Qual tipo de ativos deseja listar? ")
                encontrados = encontrar_ativos_por_tipo(ativos, tipo)

            elif filtro == "2":
                status = pedir_status("Qual status de ativos deseja listar? ")
                encontrados = encontrar_ativos_por_status(ativos, status)

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
                    encontrados = encontrar_ativos_por_nome(ativos, nome)

                    if encontrados:
                        for ativo in encontrados:
                            print(ativo.exibir_detalhes())
                    else:
                        print("Nenhum ativo encontrado.")
                elif nome_ou_id == "id":

                    id_ativo = pedir_int("Digite o ID do ativo que deseja listar: ")
                    ativo_encontrado = encontrar_ativo_por_id(ativos, id_ativo)

                    if ativo_encontrado:
                        print(ativo_encontrado.exibir_detalhes())
                    else:
                        print("Nenhum ativo encontrado.")
                else:
                    print('Opção inválida. Digite "nome" ou "id".')

        else:
            print('Opção inválida. Digite "todos" ou "um".')


def menu_dependencias(repositorio, ativos):
    while True:
        print("\n=== Menu de dependências ===\n")
        print(
            "1 - Adicionar dependência\n"
            "2 - Atualizar dependência\n"
            "3 - Remover dependência\n"
            "4 - Listar dependências\n"
            "5 - Voltar ao menu principal"
        )

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_dependencia_menu(repositorio, ativos)

        elif opcao == "2":
            atualizar_dependencia_menu(repositorio, ativos)

        elif opcao == "3":
            excluir_dependencia_menu(repositorio, ativos)

        elif opcao == "4":
            todos_ou_um = ""
            while todos_ou_um not in ("todos", "um"):
                print("Deseja listar as dependências de todos os ativos ou de apenas um?")
                todos_ou_um = input("(todos/um): ").strip().lower()

                if todos_ou_um == "todos":
                    ativos_com_dependencias = []

                    for ativo in listar_ativos_ordenados(ativos, por_nome):
                        if ativo.dependencias:
                            ativos_com_dependencias.append(ativo)

                    if not ativos_com_dependencias:
                        print("Nenhum ativo possui dependências cadastradas.")

                    for ativo in ativos_com_dependencias:
                        mostrar_cabecalho_do_ativo(ativo)
                        mostrar_dependencias(ativo, ativos)

                elif todos_ou_um == "um":
                    mostrar_lista_de_ativos(ativos)

                    ativo_escolhido = perguntar_ativo(
                        ativos, "ID do ativo cujas dependências deseja listar: "
                    )

                    if ativo_escolhido is not None:
                        mostrar_cabecalho_do_ativo(ativo_escolhido)
                        mostrar_dependencias(ativo_escolhido, ativos)

                else:
                    print('Opção inválida. Digite "todos" ou "um".')

        elif opcao == "5":
            print("Voltando ao menu principal...")
            break

        else:
            print("Opção inválida. Tente novamente.")
