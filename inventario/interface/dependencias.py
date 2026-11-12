from inventario.dominio.excecoes import DadoInvalidoError
from inventario.interface.ativos import mostrar_lista_de_ativos, perguntar_ativo
from inventario.interface.entradas import pedir_float, pedir_int
from inventario.servicos.dependencias import (
    cadastrar_dependencia,
    remover_dependencia,
    somar_fracoes,
    atualizar_dependencia,
)


def mostrar_dependencias(ativo, ativos):
    if not ativo.dependencias:
        print("Este ativo não depende de nenhum outro ativo.")
        return

    for id_ativo_do_qual_depende, fracao in ativo.dependencias.items():
        ativo_do_qual_depende = ativos[id_ativo_do_qual_depende]
        print(
            f"\nID: {id_ativo_do_qual_depende}\n"
            f"Ativo: {ativo_do_qual_depende.nome}\n"
            f"Tipo: {type(ativo_do_qual_depende).__name__}\n"
            f"Fração herdada: {fracao}"
        )

    soma = somar_fracoes(ativo.dependencias)
    print(f"\nSoma das frações: {soma}. Ainda cabem {round(1 - soma, 6)}.")


def escolher_ativo_com_dependencias(ativos, mensagem):
    mostrar_lista_de_ativos(ativos)

    ativo_encontrado = perguntar_ativo(ativos, mensagem)

    if ativo_encontrado is None:
        return None
    elif not ativo_encontrado.dependencias:
        print("Este ativo não possui dependências cadastradas.")
        return None
    else:
        return ativo_encontrado


def cadastrar_dependencia_menu(repositorio, ativos):
    mostrar_lista_de_ativos(ativos)

    ativo_que_depende = perguntar_ativo(
        ativos, "ID do ativo ao qual deseja adicionar uma dependência: "
    )

    if ativo_que_depende is None:
        return

    try:
        mostrar_dependencias(ativo_que_depende, ativos)

        id_ativo_do_qual_depende = pedir_int("ID do ativo do qual ele depende: ")
        fracao = pedir_float("Fração do risco herdada (exemplo: 0,3): ")

        cadastrar_dependencia(
            repositorio, ativos, ativo_que_depende.id, id_ativo_do_qual_depende, fracao
        )
        print("Dependência cadastrada com sucesso.")

    except DadoInvalidoError as erro:
        print(erro)


def excluir_dependencia_menu(repositorio, ativos):

    ativo_que_depende = escolher_ativo_com_dependencias(
        ativos, "ID do ativo cuja dependência deseja remover: "
    )

    if ativo_que_depende is None:
        return

    try:
        mostrar_dependencias(ativo_que_depende, ativos)

        id_ativo_do_qual_depende = pedir_int(
            "Digite o ID do ativo (dependência) que deseja remover: "
        )

        remover_dependencia(repositorio, ativos, ativo_que_depende.id, id_ativo_do_qual_depende)

        print("Dependência removida com sucesso.")

    except DadoInvalidoError as erro:
        print(erro)


def atualizar_dependencia_menu(repositorio, ativos):
    ativo_que_depende = escolher_ativo_com_dependencias(
        ativos, "ID do ativo cujas dependências deseja atualizar: "
    )

    if ativo_que_depende is None:
        return

    try:
        mostrar_dependencias(ativo_que_depende, ativos)

        id_ativo_do_qual_depende_antigo = pedir_int(
            "Digite o ID do ativo (dependência) que deseja atualizar: "
        )

        if id_ativo_do_qual_depende_antigo not in ativo_que_depende.dependencias:
            print("Este ativo não possui essa dependência.")
            return

        fracao_atual = ativo_que_depende.dependencias[id_ativo_do_qual_depende_antigo]

        texto_id_novo = input(
            "Novo ID do ativo do qual depende (tecle Enter para manter): "
        ).strip()

        if texto_id_novo == "":
            id_ativo_do_qual_depende_novo = id_ativo_do_qual_depende_antigo
        else:
            id_ativo_do_qual_depende_novo = int(texto_id_novo)

        texto_fracao_nova = (
            input("Nova fração (tecle Enter para manter): ").strip().replace(",", ".")
        )

        if texto_fracao_nova == "":
            fracao_nova = fracao_atual
        else:
            fracao_nova = float(texto_fracao_nova)

        atualizar_dependencia(
            repositorio,
            ativos,
            ativo_que_depende.id,
            id_ativo_do_qual_depende_antigo,
            id_ativo_do_qual_depende_novo,
            fracao_nova,
        )

        print("Dependência atualizada com sucesso.")

    except DadoInvalidoError as erro:
        print(erro)

    except ValueError:
        print("Digite um número válido.")
