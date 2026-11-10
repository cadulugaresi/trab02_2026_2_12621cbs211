import os
import sqlite3
from inventario.dominio.vulnerabilidade import Vulnerabilidade
from inventario.dominio.enums import StatusDaVuln
from inventario.dominio.excecoes import PersistenciaError
from inventario.dominio.ativo import MAPA_DE_TIPOS

ARQUIVO_BANCO_DE_DADOS = "inventario.db"
ESQUEMA_SQL = os.path.join(os.path.dirname(__file__), "esquema.sql")
TABELAS_DOS_TIPOS = {
    "Notebook": ("notebooks", ("tela", "sistema_operacional")),
    "Servidor": ("servidores", ("ram", "armazenamento")),
    "Roteador": ("roteadores", ("portas", "velocidade")),
    "Impressora": ("impressoras", ("tecnologia", "cor")),
}


class RepositorioSQLite:
    def __init__(self, caminho_banco_de_dados=ARQUIVO_BANCO_DE_DADOS):
        self.conexao = sqlite3.connect(caminho_banco_de_dados)
        self.executar("PRAGMA foreign_keys = ON")
        try:
            with open(ESQUEMA_SQL, encoding="utf-8") as arquivo:
                self.conexao.executescript(arquivo.read())
        except sqlite3.Error:
            raise PersistenciaError(
                "Erro de Persistência: o banco de dados está corrompido ou inacessível."
            )

    def executar(self, sql, valores=()):
        try:
            return self.conexao.execute(sql, valores)
        except sqlite3.Error:
            raise PersistenciaError("Erro de Persistência: falha ao acessar o banco de dados.")

    def carregar_ativos(self):
        ativos = {}

        for tipo in TABELAS_DOS_TIPOS.keys():
            tabela, colunas_do_tipo = TABELAS_DOS_TIPOS[tipo]

            registros = self.executar(
                """SELECT ativos.id, ativos.nome,
                ativos.setor, ativos.responsavel,
                ativos.status, """
                f"""{', '.join(colunas_do_tipo)}
                FROM ativos JOIN {tabela} ON
                {tabela}.id_ativo = ativos.id"""
            ).fetchall()

            for registro in registros:
                dados_do_ativo = {
                    "id": registro[0],
                    "nome": registro[1],
                    "setor": registro[2],
                    "responsavel": registro[3],
                    "status": registro[4],
                }

                posicao = 5
                for coluna in colunas_do_tipo:
                    dados_do_ativo[coluna] = registro[posicao]
                    posicao = posicao + 1

                ativo = MAPA_DE_TIPOS[tipo].de_dicionario(dados_do_ativo)
                ativos[ativo.id] = ativo

                todos_os_vinculos = self.executar(
                    """SELECT id_vulnerabilidade, status_tratamento
                    FROM vinculos WHERE id_ativo = ?""",
                    (ativo.id,),
                ).fetchall()

                for registro_vinculo in todos_os_vinculos:
                    id_vulnerabilidade, status_tratamento = registro_vinculo
                    ativo.vulnerabilidades[id_vulnerabilidade] = StatusDaVuln(status_tratamento)

                todas_as_dependencias = self.executar(
                    """SELECT id_ativo_do_qual_depende, fracao
                    FROM dependencias WHERE id_ativo_que_depende = ?""",
                    (ativo.id,),
                ).fetchall()

                for registro_dependencia in todas_as_dependencias:
                    id_ativo_do_qual_depende, fracao = registro_dependencia
                    ativo.dependencias[id_ativo_do_qual_depende] = fracao

        return ativos

    def carregar_catalogo(self):
        todas_as_vulnerabilidades = self.executar("""SELECT id_vulnerabilidade,
            nome_vulnerabilidade,
            cvss FROM vulnerabilidades""").fetchall()

        catalogo = {}

        for registro in todas_as_vulnerabilidades:
            id_vulnerabilidade, nome_vulnerabilidade, cvss = registro
            vulnerabilidade = Vulnerabilidade(id_vulnerabilidade, nome_vulnerabilidade, cvss)
            catalogo[id_vulnerabilidade] = vulnerabilidade

        return catalogo

    def inserir_dados_do_tipo(self, dados_do_ativo):
        tabela, colunas_do_tipo = TABELAS_DOS_TIPOS[dados_do_ativo["tipo"]]

        valores_para_inserir = [dados_do_ativo["id"]]
        marcadores = ["?"]

        for coluna in colunas_do_tipo:
            valores_para_inserir.append(dados_do_ativo[coluna])
            marcadores.append("?")

        self.executar(
            f"INSERT INTO {tabela} (id_ativo, {', '.join(colunas_do_tipo)}) "
            f"VALUES ({', '.join(marcadores)})",
            valores_para_inserir,
        )

    def adicionar_ativo(self, ativo):

        dados_do_ativo = ativo.para_dicionario()

        with self.conexao:
            self.executar(
                """INSERT INTO ativos
                (id, nome, tipo, setor, responsavel, status)
                VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    dados_do_ativo["id"],
                    dados_do_ativo["nome"],
                    dados_do_ativo["tipo"],
                    dados_do_ativo["setor"],
                    dados_do_ativo["responsavel"],
                    dados_do_ativo["status"],
                ),
            )

            self.inserir_dados_do_tipo(dados_do_ativo)

    def atualizar_ativo(self, ativo):

        dados_do_ativo = ativo.para_dicionario()

        with self.conexao:
            self.executar(
                """UPDATE ativos
                SET nome = ?, tipo = ?, setor = ?,
                responsavel = ?, status = ?
                WHERE id = ?""",
                (
                    dados_do_ativo["nome"],
                    dados_do_ativo["tipo"],
                    dados_do_ativo["setor"],
                    dados_do_ativo["responsavel"],
                    dados_do_ativo["status"],
                    dados_do_ativo["id"],
                ),
            )

            for tabela, colunas_do_tipo in TABELAS_DOS_TIPOS.values():
                self.executar(
                    f"DELETE FROM {tabela} WHERE id_ativo = ?",
                    (dados_do_ativo["id"],),
                )

            self.inserir_dados_do_tipo(dados_do_ativo)

    def remover_ativo(self, id_ativo):
        with self.conexao:
            self.executar(
                """DELETE FROM ativos
                WHERE id = ?""",
                (id_ativo,),
            )

    def adicionar_vulnerabilidade(self, vulnerabilidade):
        with self.conexao:
            self.executar(
                """INSERT INTO vulnerabilidades
                (id_vulnerabilidade, nome_vulnerabilidade, cvss)
                VALUES (?, ?, ?)""",
                (
                    vulnerabilidade.id_vulnerabilidade,
                    vulnerabilidade.nome_vulnerabilidade,
                    vulnerabilidade.cvss,
                ),
            )

    def atualizar_vulnerabilidade(self, vulnerabilidade):
        with self.conexao:
            self.executar(
                """UPDATE vulnerabilidades
                SET nome_vulnerabilidade = ?, cvss = ?
                WHERE id_vulnerabilidade = ?""",
                (
                    vulnerabilidade.nome_vulnerabilidade,
                    vulnerabilidade.cvss,
                    vulnerabilidade.id_vulnerabilidade,
                ),
            )

    def remover_vulnerabilidade(self, id_vulnerabilidade):
        with self.conexao:
            self.executar(
                """DELETE FROM vulnerabilidades
                WHERE id_vulnerabilidade = ?""",
                (id_vulnerabilidade,),
            )

    def vincular(self, id_ativo, id_vulnerabilidade, status_tratamento):
        with self.conexao:
            self.executar(
                """INSERT INTO vinculos
                (id_ativo, id_vulnerabilidade,
                status_tratamento)
                VALUES (?, ?, ?)""",
                (id_ativo, id_vulnerabilidade, status_tratamento.value),
            )

    def atualizar_status_vinculo(self, id_ativo, id_vulnerabilidade, status_tratamento):
        with self.conexao:
            self.executar(
                """UPDATE vinculos
                SET status_tratamento = ?
                WHERE id_ativo = ? AND id_vulnerabilidade = ?""",
                (status_tratamento.value, id_ativo, id_vulnerabilidade),
            )

    def desvincular(self, id_ativo, id_vulnerabilidade):
        with self.conexao:
            self.executar(
                """DELETE FROM vinculos
                WHERE id_ativo = ? AND id_vulnerabilidade = ?""",
                (id_ativo, id_vulnerabilidade),
            )

    def adicionar_dependencia(self, id_ativo_que_depende, id_ativo_do_qual_depende, fracao):
        with self.conexao:
            self.executar(
                """INSERT INTO dependencias
                (id_ativo_que_depende,
                id_ativo_do_qual_depende, fracao)
                VALUES (?, ?, ?)""",
                (id_ativo_que_depende, id_ativo_do_qual_depende, fracao),
            )

    def remover_dependencia(self, id_ativo_que_depende, id_ativo_do_qual_depende):
        with self.conexao:
            self.executar(
                """DELETE FROM dependencias
                WHERE id_ativo_que_depende = ? AND
                id_ativo_do_qual_depende = ?""",
                (id_ativo_que_depende, id_ativo_do_qual_depende),
            )

    def atualizar_dependencia(
        self,
        id_ativo_que_depende,
        id_ativo_do_qual_depende_antigo,
        id_ativo_do_qual_depende_novo,
        fracao_nova,
    ):
        with self.conexao:
            self.executar(
                """UPDATE dependencias
                SET id_ativo_do_qual_depende = ?, fracao = ?
                WHERE id_ativo_que_depende = ?
                AND id_ativo_do_qual_depende = ?""",
                (
                    id_ativo_do_qual_depende_novo,
                    fracao_nova,
                    id_ativo_que_depende,
                    id_ativo_do_qual_depende_antigo,
                ),
            )
