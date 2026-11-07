import json
import os

from inventario.dominio.enums import StatusDaVuln
from inventario.dominio.ativo import MAPA_DE_TIPOS
from inventario.dominio.vulnerabilidade import Vulnerabilidade
from inventario.dominio.excecoes import PersistenciaError
from inventario.persistencia.repositorio import Repositorio

ARQUIVO_ATIVOS = "ativos.json"
ARQUIVO_CATALOGO = "vulnerabilidades.json"


def salvar_ativos(ativos):

    lista_para_salvar = []

    for ativo in ativos.values():
        lista_para_salvar.append(ativo.para_dicionario())

    salvar_seguro(ARQUIVO_ATIVOS, lista_para_salvar)


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


def carregar_ativos():

    try:
        with open(ARQUIVO_ATIVOS, "r", encoding="utf-8") as arquivo:
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

                for dependencia in ativo_dicionario.get("dependencias", []):
                    id_ativo_do_qual_depende = dependencia["id_ativo_do_qual_depende"]
                    fracao = dependencia["fracao"]
                    novo_ativo.dependencias[id_ativo_do_qual_depende] = fracao

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


def copiar_ativo_sem_vinculos(ativo):
    classe = type(ativo)
    return classe.de_dicionario(ativo.para_dicionario())


def copiar_vulnerabilidade(vulnerabilidade):
    return Vulnerabilidade.de_dicionario(vulnerabilidade.para_dicionario())


class RepositorioJSON(Repositorio):

    def __init__(self):
        self.ativos_guardados = None
        self.catalogo_guardado = None

    def obter_ativos_guardados(self):
        if self.ativos_guardados is None:
            self.ativos_guardados = carregar_ativos()
        return self.ativos_guardados

    def obter_catalogo_guardado(self):
        if self.catalogo_guardado is None:
            self.catalogo_guardado = carregar_catalogo()
        return self.catalogo_guardado

    def carregar_ativos(self):
        self.ativos_guardados = carregar_ativos()
        return carregar_ativos()

    def carregar_catalogo(self):
        self.catalogo_guardado = carregar_catalogo()
        return carregar_catalogo()

    def adicionar_ativo(self, ativo):
        ativos = self.obter_ativos_guardados()
        ativos[ativo.id] = copiar_ativo_sem_vinculos(ativo)
        salvar_ativos(ativos)

    def atualizar_ativo(self, ativo):
        ativos = self.obter_ativos_guardados()
        ativo_atualizado = copiar_ativo_sem_vinculos(ativo)
        ativo_atualizado.vulnerabilidades = ativos[ativo.id].vulnerabilidades
        ativo_atualizado.dependencias = ativos[ativo.id].dependencias
        ativos[ativo.id] = ativo_atualizado
        salvar_ativos(ativos)

    def remover_ativo(self, id_ativo):
        ativos = self.obter_ativos_guardados()
        ativos.pop(id_ativo, None)

        for ativo in ativos.values():
            ativo.dependencias.pop(id_ativo, None)

        salvar_ativos(ativos)

    def adicionar_vulnerabilidade(self, vulnerabilidade):
        catalogo = self.obter_catalogo_guardado()
        catalogo[vulnerabilidade.id_vulnerabilidade] = copiar_vulnerabilidade(vulnerabilidade)
        salvar_catalogo(catalogo)

    def atualizar_vulnerabilidade(self, vulnerabilidade):
        catalogo = self.obter_catalogo_guardado()
        catalogo[vulnerabilidade.id_vulnerabilidade] = copiar_vulnerabilidade(vulnerabilidade)
        salvar_catalogo(catalogo)

    def remover_vulnerabilidade(self, id_vulnerabilidade):
        ativos = self.obter_ativos_guardados()
        catalogo = self.obter_catalogo_guardado()

        for ativo in ativos.values():
            ativo.vulnerabilidades.pop(id_vulnerabilidade, None)
        catalogo.pop(id_vulnerabilidade, None)

        salvar_ativos(ativos)
        salvar_catalogo(catalogo)

    def vincular(self, id_ativo, id_vulnerabilidade, status):
        ativos = self.obter_ativos_guardados()
        ativos[id_ativo].vulnerabilidades[id_vulnerabilidade] = status
        salvar_ativos(ativos)

    def atualizar_status_vinculo(self, id_ativo, id_vulnerabilidade, status):
        ativos = self.obter_ativos_guardados()
        ativos[id_ativo].vulnerabilidades[id_vulnerabilidade] = status
        salvar_ativos(ativos)

    def desvincular(self, id_ativo, id_vulnerabilidade):
        ativos = self.obter_ativos_guardados()
        ativos[id_ativo].vulnerabilidades.pop(id_vulnerabilidade, None)
        salvar_ativos(ativos)

    def adicionar_dependencia(self, id_ativo_que_depende, id_ativo_do_qual_depende, fracao):
        ativos = self.obter_ativos_guardados()
        ativos[id_ativo_que_depende].dependencias[id_ativo_do_qual_depende] = fracao
        salvar_ativos(ativos)

    def remover_dependencia(self, id_ativo_que_depende, id_ativo_do_qual_depende):
        ativos = self.obter_ativos_guardados()
        ativos[id_ativo_que_depende].dependencias.pop(id_ativo_do_qual_depende, None)
        salvar_ativos(ativos)
