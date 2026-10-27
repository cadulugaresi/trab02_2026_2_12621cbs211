from inventario.entradas import pedir_cvss, pedir_info
from inventario.excecoes import DadoInvalidoError
from inventario.modelos.vulnerabilidade import Vulnerabilidade


def proximo_id(dicionario):

    maior_id = 0

    for id_existente in dicionario:
        if id_existente > maior_id:
            maior_id = id_existente

    return maior_id + 1


def cadastrar_vulnerabilidade(catalogo):
    nome = pedir_info("Digite o nome da vulnerabilidade: ")
    cvss = pedir_cvss("Digite a nota CVSS da vulnerabilidade (0.1 a 10): ")
    id_vulnerabilidade = proximo_id(catalogo)

    vulnerabilidade = Vulnerabilidade(id_vulnerabilidade, nome, cvss)

    mostrar_vulnerabilidade(vulnerabilidade)

    return vulnerabilidade


def mostrar_vulnerabilidade(vulnerabilidade, status_tratamento=None):

    print(f"""
    ID: {vulnerabilidade.id_vulnerabilidade}
    Vulnerabilidade: {vulnerabilidade.nome_vulnerabilidade}
    CVSS: {vulnerabilidade.cvss}
    Nível: {vulnerabilidade.nivel().name.lower()}""")

    if status_tratamento is not None:
        print(f"    Status neste ativo: {status_tratamento.name.lower()}")


def vincular_vulnerabilidade(ativo, id_vulnerabilidade, status_tratamento, catalogo):
    if id_vulnerabilidade in catalogo:

        if id_vulnerabilidade in ativo.vulnerabilidades:
            raise DadoInvalidoError("Esta vulnerabilidade já está vinculada a este ativo.")

        ativo.vulnerabilidades[id_vulnerabilidade] = status_tratamento

    else:
        raise DadoInvalidoError("Vulnerabilidade não encontrada no catálogo.")

def mostrar_vulnerabilidades_do_ativo(ativo, catalogo):
    for id_vulnerabilidade, status_tratamento in ativo.vulnerabilidades.items():
        vulnerabilidade = catalogo[id_vulnerabilidade]
        mostrar_vulnerabilidade(vulnerabilidade, status_tratamento)

def atualizar_status_vulnerabilidade(ativo_encontrado, id_vulnerabilidade, novo_status):
    if id_vulnerabilidade not in ativo_encontrado.vulnerabilidades:
        print('Este ativo não possui nenhuma vulnerabilidade com este ID vinculada a ele.')

    ativo_encontrado.vulnerabilidades[id_vulnerabilidade] = novo_status