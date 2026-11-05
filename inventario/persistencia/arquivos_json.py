import json
import os

from inventario.dominio.enums import StatusDaVuln
from inventario.dominio.ativo import MAPA_DE_TIPOS
from inventario.dominio.vulnerabilidade import Vulnerabilidade
from inventario.dominio.excecoes import PersistenciaError

ARQUIVO_DADOS = "ativos.json"
ARQUIVO_CATALOGO = "vulnerabilidades.json"


def salvar_dados(ativos):

    lista_para_salvar = []

    for ativo in ativos.values():
        lista_para_salvar.append(ativo.para_dicionario())

    salvar_seguro(ARQUIVO_DADOS, lista_para_salvar)


def salvar_catalogo(catalogo):

    catalogo_para_salvar = []

    for vulnerabilidade in catalogo.values():
        catalogo_para_salvar.append(vulnerabilidade.para_dicionario())

    salvar_seguro(ARQUIVO_CATALOGO, catalogo_para_salvar)


def salvar_seguro(caminho, dados):

    arquivo_temporario = caminho + ".tmp"

    try:
        with open(arquivo_temporario, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)

        os.replace(arquivo_temporario, caminho)

    except PermissionError:
        raise PersistenciaError(
            "Erro de Persistência: Sem permissão para gravar no arquivo no computador."
        )
    except IOError:
        raise PersistenciaError("Erro de Persistência ao salvar os dados no arquivo.")


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
        raise PersistenciaError(
            "Erro de Persistência: O arquivo de dados está corrompido ou com formato inválido."
        )


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
        raise PersistenciaError(
            "Erro de Persistência: O catálogo de vulnerabilidades está corrompido ou com formato inválido."
        )
