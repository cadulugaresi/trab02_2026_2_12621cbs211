from funcoes_t2 import *

ativos = carregar_dados()
catalogo = carregar_catalogo()

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
            novo_ativo = cadastrar_ativo(ativos)
            ativos[novo_ativo.id] = novo_ativo
            salvar_dados(ativos)

        elif opcao == "2":

            todos_um = ""

            while todos_um not in ("todos", "um", "filtrar"):
                print("Deseja listar todos os ativos, filtrar ou mostrar apenas um?")
                todos_um = input("todos/filtrar/um): ").strip().lower()

                if todos_um == "todos":
                    if ativos:
                        print("Listando todos os ativos...")
                        for ativo in ativos.values():
                            print(ativo.exibir_detalhes())
                    else:
                        print("Nenhum ativo cadastrado.")

                elif todos_um == "filtrar":

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

                elif todos_um == "um":

                    nome_ou_id = ""

                    while nome_ou_id not in ("nome", "id"):
                        nome_ou_id = (
                            input("Deseja buscar ativo por NOME ou ID? (nome/id) ").strip().lower()
                        )

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

        elif opcao == "3":
            excluir_ativo(ativos)

        elif opcao == "4":

            while True:
                print('''MENU DE VULNERABILIDADES

                        1 - Cadastrar vulnerabilidade
                        2 - Listar catálogo de vulnerabilidades
                        3 - Vincular vulnerabilidade a um ativo
                        4 - Listar vulnerabilidades de um ativo
                        5 - Atualizar status da vulnerabilidade em um ativo
                        6 - Desvincular vulnerabilidade de um ativo
                        7 - Excluir vulnerabilidade do catálogo
                        8 - Editar vulnerabilidade no catálogo
                        9 - Voltar ao menu principal''')

                opcao_vulnerabilidade = input("Escolha uma opção: ").strip()

                if opcao_vulnerabilidade == '1':
                    nova_vulnerabilidade = cadastrar_vulnerabilidade(catalogo)
                    catalogo[nova_vulnerabilidade.id_vulnerabilidade] = nova_vulnerabilidade
                    salvar_catalogo(catalogo)

                elif opcao_vulnerabilidade == '2':
                    if not catalogo:
                        print("Nenhuma vulnerabilidade cadastrada no catálogo.")
                    else:
                        print("Listando catálogo de vulnerabilidades...")
                        for vulnerabilidade in catalogo.values():
                            mostrar_vulnerabilidade(vulnerabilidade)

                elif opcao_vulnerabilidade == '3':
                    if not catalogo:
                        print("Nenhuma vulnerabilidade cadastrada no catálogo.")
                    elif not ativos:
                        print("Nenhum ativo cadastrado.")
                    else:
                        for vulnerabilidade in catalogo.values():
                            mostrar_vulnerabilidade(vulnerabilidade)

                        id_vulnerabilidade = pedir_int("Digite o ID da vulnerabilidade: ")

                        if id_vulnerabilidade not in catalogo:
                            print('Vulnerabilidade não encontrada no catálogo. Tente novamente.')

                        else:
                            id_ativo = pedir_int("Digite o ID do ativo ao qual deseja vincular essa vulnerabilidade: ")
                            ativo_encontrado = encontrar_ativo_por_id(id_ativo, ativos)

                            if ativo_encontrado is None:
                                print("Ativo não encontrado.")

                            else:
                                status_tratamento = pedir_status_vulnerabilidade("Digite o status: ")

                                try:
                                    vincular_vulnerabilidade(ativo_encontrado, id_vulnerabilidade, status_tratamento, catalogo)
                                    salvar_dados(ativos)
                                    print("Vulnerabilidade vinculada com sucesso!")

                                except DadoInvalidoError as erro:
                                    print(erro)

                elif opcao_vulnerabilidade in ('4','5','6','7','8'):
                    print('Em construção...')

                elif opcao_vulnerabilidade == '9':
                    print("Voltando ao menu principal...")
                    break
                
                else:
                    print('Opção inválida. Tente novamente.')

        elif opcao == "5":
            editar_ativo(ativos)
            salvar_dados(ativos)

        elif opcao == "6":
            print("Saindo do programa...")
            break

        else:
            print("Opção inválida. Tente novamente.")

    except (EOFError, KeyboardInterrupt):
        print("Programa encerrado pelo usuário.")
        break
