from funcoes_s1 import *

ativos=carregar_dados()

while True:

    print('MENU')
    print('1 - Cadastrar ativo')
    print('2 - Listar ativos')
    print('3 - Excluir ativo')
    print('4 - Editar vulnerabilidades')
    print('5 - Editar ativo')
    print('6 - Sair')

    try:
        opcao = input('Escolha uma opção: ').strip()
  
    except (EOFError, KeyboardInterrupt):
        print('Programa encerrado pelo usuário.')
        break

    except ValueError:
        print('Escolha uma opção válida.')
        continue

    if opcao == '1':
        novo_ativo = cadastrar_ativo(ativos)
        ativos[novo_ativo.id] = novo_ativo
        salvar_dados(ativos)

    elif opcao == '2':

        todos_um = input('Deseja listar todos os ativos ou apenas um específico? (todos/um): ').strip()

        if todos_um == 'todos':
            if ativos:
                print('Listando ativos por ID, nome e responsável...')
                for ativo in ativos.values():
                    print(
                        f'''ID: {ativo.id}
                        Nome: {ativo.nome}
                        Categoria: {ativo.categoria.name}
                        Responsável: {ativo.responsavel}
                        Status: {ativo.status.name}'''
                    )
            else:
                print('Nenhum ativo cadastrado.')

        elif todos_um == 'um':
            id_ativo = pedir_id('Digite o ID do ativo que deseja listar: ')
            ativo_encontrado = encontrar_ativo_por_id(id_ativo, ativos)
            if ativo_encontrado:
                print(
                    f'''ID: {ativo_encontrado.id}
                    Nome: {ativo_encontrado.nome}
                    Categoria: {ativo_encontrado.categoria.name}
                    Responsável: {ativo_encontrado.responsavel}
                    Status: {ativo_encontrado.status.name}'''
                )

            else:
                print('Ativo não encontrado.')

        else:
            print('Opção inválida. Tente novamente.')

    elif opcao == '3':
        excluir_ativo(ativos)

    elif opcao == '4':

        while True:
            print('Menu de vulnerabilidades:')
            print('1 - Listar vulnerabilidades')
            print('2 - Adicionar vulnerabilidade')
            print('3 - Remover vulnerabilidade')
            print('4 - Voltar ao menu principal')

            try:
                opcao_vulnerabilidade = input('Escolha uma opção: ').strip()

            except (EOFError, KeyboardInterrupt):
                print('Programa encerrado pelo usuário.')
                break

            except ValueError:
                print('Escolha uma opção válida.')
                continue

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
                                    print(
                                        f'''  Vulnerabilidade: {vulnerabilidade.nome_vulnerabilidade}
                                        Nível: {vulnerabilidade.nivel.name.lower()}
                                        Status: {vulnerabilidade.status_tratamento.name.lower()}'''
                                    )

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
                                print(
                                    f'''Vulnerabilidade: {vulnerabilidade.nome_vulnerabilidade}
                                    Nível: {vulnerabilidade.nivel.name.lower()}
                                    Status: {vulnerabilidade.status_tratamento.name.lower()}'''
                                )
                        
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
                        status_tratamento = status_vulnerabilidade()
                        ativo_encontrado.vulnerabilidades.append(
                            Vulnerabilidade(nome_da_vulnerabilidade, nivel, status_tratamento)
                        )

                        salvar_dados(ativos)

                        print(f'''Informações adicionadas com sucesso! \n
                              Vulnerabilidade: "{nome_da_vulnerabilidade}" \n
                              Nível: "{nivel.name.lower()}" \n
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
                            print(f'''{vulnerabilidade.nome_vulnerabilidade} \n
                            (nível {vulnerabilidade.nivel.name.lower()}) \n
                            (status {vulnerabilidade.status_tratamento.name.lower()}''')

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