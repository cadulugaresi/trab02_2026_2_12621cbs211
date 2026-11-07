from inventario.dominio.excecoes import DadoInvalidoError
from inventario.dominio.validacoes import validar_soma_fracao
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

    soma_atual = 0
    for fracao_existente in ativo_que_depende.dependencias.values():
        soma_atual = soma_atual + fracao_existente

    validar_soma_fracao(soma_atual, fracao)

    ativo_que_depende.dependencias[id_ativo_do_qual_depende] = fracao
    repositorio.adicionar_dependencia(id_ativo_que_depende, id_ativo_do_qual_depende, fracao)
