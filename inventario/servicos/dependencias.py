from inventario.dominio.excecoes import DadoInvalidoError
from inventario.dominio.validacoes import (
    validar_soma_fracao,
    validar_fracao,
)
from inventario.servicos.ativos import obter_ativo


def cadastrar_dependencia(
    repositorio, ativos, id_ativo_que_depende, id_ativo_do_qual_depende, fracao
):
    if id_ativo_que_depende == id_ativo_do_qual_depende:
        raise DadoInvalidoError("Um ativo não pode depender dele próprio.")

    ativo_que_depende = obter_ativo(ativos, id_ativo_que_depende)
    obter_ativo(ativos, id_ativo_do_qual_depende)

    if id_ativo_do_qual_depende in ativo_que_depende.dependencias:
        raise DadoInvalidoError("Este ativo já possui essa dependência.")

    soma_atual = somar_fracoes(ativo_que_depende.dependencias)
    validar_fracao(fracao)
    validar_soma_fracao(soma_atual, fracao)

    ativo_que_depende.dependencias[id_ativo_do_qual_depende] = fracao
    repositorio.adicionar_dependencia(id_ativo_que_depende, id_ativo_do_qual_depende, fracao)


def remover_dependencia(repositorio, ativos, id_ativo_que_depende, id_ativo_do_qual_depende):
    ativo_que_depende = obter_ativo(ativos, id_ativo_que_depende)
    obter_ativo(ativos, id_ativo_do_qual_depende)

    if id_ativo_do_qual_depende not in ativo_que_depende.dependencias:
        raise DadoInvalidoError("Este ativo não possui essa dependência.")

    del ativo_que_depende.dependencias[id_ativo_do_qual_depende]
    repositorio.remover_dependencia(id_ativo_que_depende, id_ativo_do_qual_depende)


def atualizar_dependencia(
    repositorio,
    ativos,
    id_ativo_que_depende,
    id_ativo_do_qual_depende_antigo,
    id_ativo_do_qual_depende_novo,
    fracao_nova,
):
    if id_ativo_do_qual_depende_novo == id_ativo_que_depende:
        raise DadoInvalidoError("Um ativo não pode depender dele próprio.")

    ativo_que_depende = obter_ativo(ativos, id_ativo_que_depende)
    obter_ativo(ativos, id_ativo_do_qual_depende_novo)

    if id_ativo_do_qual_depende_antigo not in ativo_que_depende.dependencias:
        raise DadoInvalidoError("Este ativo não possui essa dependência.")

    # Se o usuário quis trocar uma dependência por outra
    # já cadastrada no mesmo ativo:
    trocou_de_ativo = id_ativo_do_qual_depende_novo != id_ativo_do_qual_depende_antigo
    if trocou_de_ativo and id_ativo_do_qual_depende_novo in ativo_que_depende.dependencias:
        raise DadoInvalidoError(
            f"Este ativo já depende do ativo {id_ativo_do_qual_depende_novo}. Edite essa dependência em vez disso."
        )

    fracao_antiga = ativo_que_depende.dependencias[id_ativo_do_qual_depende_antigo]
    soma_sem_a_antiga = somar_fracoes(ativo_que_depende.dependencias) - fracao_antiga
    validar_fracao(fracao_nova)
    validar_soma_fracao(soma_sem_a_antiga, fracao_nova)

    del ativo_que_depende.dependencias[id_ativo_do_qual_depende_antigo]
    ativo_que_depende.dependencias[id_ativo_do_qual_depende_novo] = fracao_nova
    repositorio.atualizar_dependencia(
        id_ativo_que_depende,
        id_ativo_do_qual_depende_antigo,
        id_ativo_do_qual_depende_novo,
        fracao_nova,
    )


def somar_fracoes(dependencias):
    soma = 0
    for fracao in dependencias.values():
        soma = soma + fracao
    return round(soma, 6)
