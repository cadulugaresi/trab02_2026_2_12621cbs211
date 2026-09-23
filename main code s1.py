from funcoes_s1 import *

ativos = carregar_dados()

while True:

    try:

        print('MENU')
        print('1 - Cadastrar ativo')
        print('2 - Listar ativos')
        print('3 - Excluir ativo')
        print('4 - Editar vulnerabilidades')
        print('5 - Editar ativo')
        print('6 - Sair')

        opcao = input('Escolha uma opção: ').strip()

        if opcao == '1':
            novo_ativo = cadastrar_ativo(ativos)
            ativos[novo_ativo.id] = novo_ativo
            salvar_dados(ativos)

        elif opcao == '2':

            todos_um = ''

            while todos_um not in ('todos', 'um'):
                todos_um = input('Deseja listar todos os ativos ou apenas um específico? (todos/um): ').strip().lower()

                if todos_um == 'todos':
                    if ativos:
                        print('Listando ativos por ID, nome e responsável...')
                        for ativo in ativos.values():
                            mostrar_ativo(ativo)
                    else:
                        print('Nenhum ativo cadastrado.')

                elif todos_um == 'um':

                    nome_ou_id = ''

                    while nome_ou_id not in ('nome', 'id'):
                        nome_ou_id = input('Deseja buscar ativo por NOME ou ID? (nome/id) ').strip().lower()

                        if nome_ou_id == 'nome':

                            nome = pedir_info('Digite o nome do ativo que deseja listar: ')
                            encontrados = encontrar_ativo_por_nome(nome, ativos)

                            if encontrados:
                                for ativo in encontrados:
                                    mostrar_ativo(ativo)
                            else:
                                print('Nenhum ativo encontrado.')
                        elif nome_ou_id == 'id':

                            id_ativo = pedir_id('Digite o ID do ativo que deseja listar: ')
                            ativo_encontrado = encontrar_ativo_por_id(id_ativo, ativos)

                            if ativo_encontrado:
                                mostrar_ativo(ativo_encontrado)
                            else:
                                print('Nenhum ativo encontrado.')
                        else:
                            print('Opção inválida. Digite "nome" ou "id".')

                else:
                    print('Opção inválida. Digite "todos" ou "um".')
                    
        elif opcao == '3':
            excluir_ativo(ativos)

        elif opcao == '4':

            while True:
                print('Menu de vulnerabilidades:')
                print('1 - Listar vulnerabilidades')
                print('2 - Adicionar vulnerabilidade')
                print('3 - Remover vulnerabilidade')
                print('4 - Voltar ao menu principal')

                opcao_vulnerabilidade = input('Escolha uma opção: ').strip()

                if opcao_vulnerabilidade == '1':
                    print('Listando vulnerabilidades...')

                    todas_um = input('Deseja listar todas as vulnerabilidades ou apenas as de um ativo específico? (todas/um): ').strip()

                    if todas_um == 'todas':

                        if ativos:
                            print('Listando todas as vulnerabilidades...')
                            encontrou_alguma = False

                            for ativo in ativos.values():
                                if ativo.vulnerabilidades:
                                    encontrou_alguma = True
                                    print(f"Ativo: {ativo.nome}")

                                    for vulnerabilidade in ativo.vulnerabilidades:
                                        mostrar_vulnerabilidade(vulnerabilidade)

                            if not encontrou_alguma:
                                print('Nenhuma vulnerabilidade cadastrada nos ativos.')

                        else:
                            print('Nenhum ativo cadastrado.')

                    elif todas_um == 'um':

                        id_ativo_vulneravel = pedir_id('Digite o ID do ativo que deseja listar as vulnerabilidades: ')
                        ativo_encontrado = encontrar_ativo_por_id(id_ativo_vulneravel, ativos)

                        if ativo_encontrado:

                            if not ativo_encontrado.vulnerabilidades:
                                print('Este ativo não possui vulnerabilidades cadastradas.')

                            else:
                                print('Vulnerabilidades cadastradas:')
                                for vulnerabilidade in ativo_encontrado.vulnerabilidades:
                                    mostrar_vulnerabilidade(vulnerabilidade)

                        else:
                            print('Ativo não encontrado.')

                    else:
                        print('Opção inválida. Tente novamente.')

                elif opcao_vulnerabilidade == '2':
                    print('Adicionando vulnerabilidade...')

                    id_ativo_add_vuln = pedir_id('Digite o ID do ativo que deseja adicionar a vulnerabilidade: ')
                    ativo_encontrado = encontrar_ativo_por_id(id_ativo_add_vuln, ativos)

                    if ativo_encontrado:
                        nome_da_vulnerabilidade = input('Digite a vulnerabilidade que deseja adicionar: ').strip()

                        if not nome_da_vulnerabilidade:
                            print('Vulnerabilidade não pode ser vazia. Tente novamente.')

                        else:

                            nivel = nivel_vulnerabilidade()
                            tipo = pedir_info('Digite o tipo da vulnerabilidade: ')
                            status_tratamento = status_vulnerabilidade()
                            ativo_encontrado.vulnerabilidades.append(
                                Vulnerabilidade(nome_da_vulnerabilidade, tipo, nivel, status_tratamento)
                            )

                            salvar_dados(ativos)

                            print(f'''Informações adicionadas com sucesso!
                                Vulnerabilidade: "{nome_da_vulnerabilidade}"
                                Tipo: "{tipo}"
                                Nível: "{nivel.name.lower()}"
                                Status: "{status_tratamento.name.lower()}" ''')

                    else:
                        print('Ativo não encontrado.')

                elif opcao_vulnerabilidade == '3':
                    print('Removendo vulnerabilidade...')

                    id_ativo_del_vuln = pedir_id('Digite o ID do ativo que deseja remover a vulnerabilidade: ')
                    ativo_encontrado = encontrar_ativo_por_id(id_ativo_del_vuln, ativos)

                    if ativo_encontrado:

                        if not ativo_encontrado.vulnerabilidades:
                            print('Este ativo não possui vulnerabilidades cadastradas.')

                        else:
                            print('Vulnerabilidades cadastradas:')
                            for vulnerabilidade in ativo_encontrado.vulnerabilidades:
                                mostrar_vulnerabilidade(vulnerabilidade)

                            nome_a_remover = input('Digite o nome da vulnerabilidade que deseja remover: ').strip()

                            vulnerabilidade_encontrada = None

                            for vulnerabilidade in ativo_encontrado.vulnerabilidades:
                                if vulnerabilidade.nome_vulnerabilidade == nome_a_remover:
                                    vulnerabilidade_encontrada = vulnerabilidade

                            if vulnerabilidade_encontrada:
                                ativo_encontrado.vulnerabilidades.remove(vulnerabilidade_encontrada)
                                salvar_dados(ativos)
                                print(f'Vulnerabilidade "{nome_a_remover}" removida do ativo {ativo_encontrado.nome} com sucesso!')
                            else:
                                print('Vulnerabilidade não encontrada. Tente novamente.')
                    else:
                        print('Ativo não encontrado.')

                elif opcao_vulnerabilidade == '4':
                    print('Voltando ao menu principal...')
                    break

        elif opcao == '5':
            editar_ativo(ativos)
            salvar_dados(ativos)

        elif opcao == '6':
            print('Saindo do programa...')
            break

        else:
            print('Opção inválida. Tente novamente.')

    except (EOFError, KeyboardInterrupt):
        print('Programa encerrado pelo usuário.')
        break