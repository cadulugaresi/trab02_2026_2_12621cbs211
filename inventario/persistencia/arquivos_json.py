import json

from inventario.dominio.enums import StatusDaVuln
from inventario.dominio.ativo import MAPA_DE_TIPOS
from inventario.dominio.vulnerabilidade import Vulnerabilidade

ARQUIVO_DADOS = "ativos.json"
ARQUIVO_CATALOGO = "vulnerabilidades.json"


def salvar_catalogo(catalogo):

    catalogo_para_salvar = []

    for vulnerabilidade in catalogo.values():
        catalogo_para_salvar.append(vulnerabilidade.para_dicionario())

    try:
        with open(ARQUIVO_CATALOGO, "w", encoding="utf-8") as arquivo:
            json.dump(catalogo_para_salvar, arquivo, indent=4, ensure_ascii=False)
    except PermissionError:
        print("Erro de Persistência: Sem permissão para gravar no arquivo no computador.")
    except IOError:
        print("Erro de Persistência ao salvar os dados no arquivo.")


def carregar_catalogo():

    try:
        with open(ARQUIVO_CATALOGO, "r", encoding="utf-8") as arquivo:
            dados_brutos = json.load(arquivo)
            catalogo = {}

            for dicionario_vulnerabilidade in dados_brutos:
                vulnerabilidade = Vulnerabilidade.de_dicionario(dicionario_vulnerabilidade)
                catalogo[vulnerabilidade.id_vulnerabilidade] = vulnerabilidade

            return catalogo

    except FileNotFoundError:
        return {}

    except json.JSONDecodeError:
        print("Aviso: ocorreu um erro no arquivo de dados. Criando um novo arquivo...")
        return {}


def salvar_dados(ativos):

    lista_para_salvar = []

    for ativo in ativos.values():
        lista_para_salvar.append(ativo.para_dicionario())

    try:
        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
            json.dump(lista_para_salvar, arquivo, indent=4, ensure_ascii=False)
    except PermissionError:
        print("Erro de Persistência: Sem permissão para gravar no arquivo no computador.")
    except IOError:
        print("Erro de Persistência ao salvar os dados no arquivo.")


def carregar_dados():

    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
            dados_brutos = json.load(arquivo)
            ativos_carregados = {}

            for ativo_dicionario in dados_brutos:
                tipo_string = ativo_dicionario["tipo"]
                classe = MAPA_DE_TIPOS[tipo_string]
                novo_ativo = classe.de_dicionario(ativo_dicionario)

                for vinculo in ativo_dicionario["vulnerabilidades"]:
                    id_vulnerabilidade = vinculo["id_vulnerabilidade"]
                    status_tratamento = StatusDaVuln(vinculo["status_tratamento"])
                    novo_ativo.vulnerabilidades[id_vulnerabilidade] = status_tratamento

                ativos_carregados[novo_ativo.id] = novo_ativo

            return ativos_carregados

    except FileNotFoundError:
        return {}

    except json.JSONDecodeError:
        print("Aviso: ocorreu um erro no arquivo de dados. Criando um novo arquivo...")
        return {}
