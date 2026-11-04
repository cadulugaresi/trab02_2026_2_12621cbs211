from inventario.entradas import (
    pedir_cor,
    pedir_float,
    pedir_info,
    pedir_int,
    pedir_setor,
    pedir_status,
    pedir_tecnologia,
    pedir_tipo,
)
from inventario.excecoes import DadoInvalidoError
from inventario.modelos.ativo import Impressora, Notebook, Roteador, Servidor
from inventario.persistencia import salvar_dados


def pedir_id_disponivel(ativos):

    while True:

        ID_do_ativo = pedir_int("Digite o ID do ativo: ")
        if encontrar_ativo_por_id(ID_do_ativo, ativos) is None:
            return ID_do_ativo

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


def cadastrar_ativo(ativos):

    tipo = pedir_tipo("Digite o tipo do ativo: ")
    ID_do_ativo = pedir_id_disponivel(ativos)
    nome_ativo = pedir_info("Digite o nome do ativo: ")
    setor = pedir_setor("Digite o setor do ativo: ")
    responsavel = pedir_info("Digite o nome do responsável pelo ativo: ")
    status = pedir_status("Digite o status do ativo: ")

    if tipo is Notebook:
        so, tela = cadastro_notebook()
        ativo = Notebook(ID_do_ativo, nome_ativo, setor, responsavel, status, so, tela)

    elif tipo is Roteador:
        portas, velocidade = cadastro_roteador()
        ativo = Roteador(ID_do_ativo, nome_ativo, setor, responsavel, status, portas, velocidade)

    elif tipo is Servidor:
        ram, armazenamento = cadastro_servidor()
        ativo = Servidor(ID_do_ativo, nome_ativo, setor, responsavel, status, ram, armazenamento)

    elif tipo is Impressora:
        cor, tecnologia = cadastro_impressora()
        ativo = Impressora(ID_do_ativo, nome_ativo, setor, responsavel, status, cor, tecnologia)

    registrar_ativo(ativos, ativo)  # entrega o ativo pronto pra regra
    print("Ativo cadastrado com sucesso!")
    print(ativo.exibir_detalhes())
    return ativo


def registrar_ativo(ativos, ativo):
    if ativo.id in ativos:  # regra: o ID não pode repetir
        raise DadoInvalidoError("Já existe um ativo cadastrado com este ID.")

    ativos[ativo.id] = ativo  # guarda no inventário
    salvar_dados(ativos)  # cozinha guarda na despensa


def encontrar_ativo_por_id(ID, ativos):
    return ativos.get(ID)


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


def editar_ativo(ativos):

    id_ativo = pedir_int("Digite o ID do ativo que deseja editar: ")

    ativo_encontrado = encontrar_ativo_por_id(id_ativo, ativos)

    if not ativo_encontrado:
        print("Nenhum ativo com este ID cadastrado.")
        return

    print(f"""Dados atuais do ativo:
    ID: {ativo_encontrado.id}
    Nome: {ativo_encontrado.nome}
    Responsável: {ativo_encontrado.responsavel}
    Tipo: {type(ativo_encontrado).__name__}
    Setor: {ativo_encontrado.setor.name}
    Status: {ativo_encontrado.status.name}
    """)

    while True:
        print("""
        MENU DE EDIÇÃO
        1 - Editar responsável
        2 - Editar status
        3 - Editar setor
        4 - Editar detalhes específicos
        5 - Editar tipo
        6 - Voltar""")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            novo_responsavel = pedir_info("Digite o novo nome do responsável pelo ativo: ")
            ativo_encontrado.responsavel = novo_responsavel
            print(f"""
                Responsável atualizado com sucesso.
                Novo responsável: {novo_responsavel}.
                """)

        elif opcao == "2":
            novo_status = pedir_status("Digite o novo status do ativo: ")
            ativo_encontrado.status = novo_status
            print(f"""
                Status do ativo atualizado com sucesso.
                Status atual: {novo_status.name}.
                """)

        elif opcao == "3":
            novo_setor = pedir_setor("Digite o novo setor do ativo: ")
            ativo_encontrado.setor = novo_setor
            print(f"""
                Setor do ativo atualizado com sucesso.
                Setor atual: {novo_setor.name}.
                """)

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

            print(f"""
            Detalhes específicos atualizados com sucesso!
            Ativo atualizado:
            {ativo_encontrado.exibir_detalhes()}
            """)

        elif opcao == "5":

            novo_tipo = pedir_tipo("Qual o novo tipo do ativo? ")

            if novo_tipo is Notebook:
                so, tela = cadastro_notebook()
                novo_ativo = Notebook(
                    id_ativo,
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
                    id_ativo,
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
                    id_ativo,
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
                    id_ativo,
                    ativo_encontrado.nome,
                    ativo_encontrado.setor,
                    ativo_encontrado.responsavel,
                    ativo_encontrado.status,
                    cor,
                    tecnologia,
                )

            novo_ativo.vulnerabilidades = ativo_encontrado.vulnerabilidades
            ativos[id_ativo] = novo_ativo
            ativo_encontrado = novo_ativo
            print(f"""
                Tipo do ativo atualizado com sucesso!
                Tipo atual: {type(novo_ativo).__name__}.
                """)

        elif opcao == "6":
            print("Voltando...")
            break

        else:
            print("Opção inválida.")


def excluir_ativo(ativos):
    if ativos:
        id_a_excluir = pedir_int("Digite o ID do ativo que deseja excluir: ")
        ativo_encontrado = encontrar_ativo_por_id(id_a_excluir, ativos)

        if ativo_encontrado:

            if confirmar_exclusao(ativo_encontrado):
                del ativos[ativo_encontrado.id]
                salvar_dados(ativos)
                print("Ativo excluído com sucesso!")
            else:
                print("Exclusão cancelada.")

        else:
            print("Ativo não encontrado.")

    else:
        print("Nenhum ativo cadastrado.")


def confirmar_exclusao(ativo):

    print(f'Tem certeza que deseja excluir o ativo "{ativo.nome}" (ID {ativo.id})?')
    resposta = input('Digite "sim" para excluir ou tecle enter para voltar: ').strip().lower()

    if resposta == "sim":
        return True
    else:
        return False


def encontrar_ativo(ativos):

    if not ativos:
        print("Nenhum ativo cadastrado.")
        return None

    id_ativo = pedir_int("Digite o ID do ativo: ")
    ativo_encontrado = encontrar_ativo_por_id(id_ativo, ativos)

    if not ativo_encontrado:
        print("Ativo não encontrado.")
        return None

    return ativo_encontrado


def escolher_ativo_com_vulnerabilidades(ativos):
    ativo_encontrado = encontrar_ativo(ativos)
    if ativo_encontrado is None:
        return None
    elif not ativo_encontrado.vulnerabilidades:
        print("Nenhuma vulnerabilidade vinculada a este ativo.")
        return None
    else:
        return ativo_encontrado
