from inventario.dominio.excecoes import DadoInvalidoError
from inventario.interface.ativos import perguntar_ativo
from inventario.interface.entradas import pedir_float, pedir_int
from inventario.servicos.dependencias import (
    cadastrar_dependencia,
    remover_dependencia,
    somar_fracoes,
)


def mostrar_dependencias(ativo, ativos):
    if not ativo.dependencias:
        print("Este ativo não depende de nenhum outro ativo.")
        return

    for id_ativo_do_qual_depende, fracao in ativo.dependencias.items():
        ativo_do_qual_depende = ativos[id_ativo_do_qual_depende]
        print(f"""
    ID: {id_ativo_do_qual_depende}
    Ativo: {ativo_do_qual_depende.nome}
    Tipo: {type(ativo_do_qual_depende).__name__}
    Fração herdada: {fracao}""")

    soma = somar_fracoes(ativo.dependencias)
    print(f"""
    Soma das frações: {soma}. Ainda cabem {round(1 - soma, 6)}.""")


def cadastrar_dependencia_menu(repositorio, ativos):

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


def deletar_dependencia_menu(repositorio, ativos):

    ativo_que_depende = perguntar_ativo(
        ativos, "ID do ativo do qual deseja remover uma dependência: "
    )

    if ativo_que_depende is None:
        return

    if not ativo_que_depende.dependencias:
        print("Este ativo não possui dependências cadastradas.")
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
