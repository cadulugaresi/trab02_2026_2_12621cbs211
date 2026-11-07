import os
import sqlite3
from inventario.persistencia.repositorio import Repositorio
from inventario.dominio.vulnerabilidade import Vulnerabilidade
from inventario.dominio.enums import StatusDaVuln
from inventario.dominio.ativo import MAPA_DE_TIPOS

ARQUIVO_BANCO_DE_DADOS = "inventario.db"
ESQUEMA_SQL = os.path.join(os.path.dirname(__file__), "esquema.sql")
TABELAS_DOS_TIPOS = {
    "Notebook": ("notebooks", ("tela", "sistema_operacional")),
    "Servidor": ("servidores", ("ram", "armazenamento")),
    "Roteador": ("roteadores", ("portas", "velocidade")),
    "Impressora": ("impressoras", ("tecnologia", "cor")),
}


class RepositorioSQLite(Repositorio):
    def __init__(self, caminho_banco_de_dados=ARQUIVO_BANCO_DE_DADOS):
        self.conexao = sqlite3.connect(caminho_banco_de_dados)
        self.conexao.execute("PRAGMA foreign_keys = ON")

        with open(ESQUEMA_SQL, encoding="utf-8") as arquivo:
            self.conexao.executescript(arquivo.read())

    def carregar_ativos(self):
        ativos = {}

        for tipo in TABELAS_DOS_TIPOS.keys():
            tabela, colunas_do_tipo = TABELAS_DOS_TIPOS[tipo]

            registros = self.conexao.execute(
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

                todos_os_vinculos = self.conexao.execute(
                    """SELECT id_vulnerabilidade, status_tratamento
                    FROM vinculos WHERE id_ativo = ?""",
                    (ativo.id,),
                ).fetchall()

                for registro_vinculo in todos_os_vinculos:
                    id_vulnerabilidade, status_tratamento = registro_vinculo
                    ativo.vulnerabilidades[id_vulnerabilidade] = StatusDaVuln(status_tratamento)

        return ativos

    def carregar_catalogo(self):
        todas_as_vulnerabilidades = self.conexao.execute("""SELECT id_vulnerabilidade,
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

        self.conexao.execute(
            f"INSERT INTO {tabela} (id_ativo, {', '.join(colunas_do_tipo)}) "
            f"VALUES ({', '.join(marcadores)})",
            valores_para_inserir,
        )

    def adicionar_ativo(self, ativo):

        dados_do_ativo = ativo.para_dicionario()

        with self.conexao:
            self.conexao.execute(
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
            self.conexao.execute(
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
                self.conexao.execute(
                    f"DELETE FROM {tabela} WHERE id_ativo = ?",
                    (dados_do_ativo["id"],),
                )

            self.inserir_dados_do_tipo(dados_do_ativo)

    def remover_ativo(self, id_ativo):
        with self.conexao:
            self.conexao.execute(
                """DELETE FROM ativos
                WHERE id = ?""",
                (id_ativo,),
            )

    def adicionar_vulnerabilidade(self, vulnerabilidade):
        with self.conexao:
            self.conexao.execute(
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
            self.conexao.execute(
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
            self.conexao.execute(
                """DELETE FROM vulnerabilidades
                WHERE id_vulnerabilidade = ?""",
                (id_vulnerabilidade,),
            )

    def vincular(self, id_ativo, id_vulnerabilidade, status_tratamento):
        with self.conexao:
            self.conexao.execute(
                """INSERT INTO vinculos
                (id_ativo, id_vulnerabilidade,
                status_tratamento)
                VALUES (?, ?, ?)""",
                (id_ativo, id_vulnerabilidade, status_tratamento.value),
            )

    def atualizar_status_vinculo(self, id_ativo, id_vulnerabilidade, status_tratamento):
        with self.conexao:
            self.conexao.execute(
                """UPDATE vinculos
                SET status_tratamento = ?
                WHERE id_ativo = ? AND id_vulnerabilidade = ?""",
                (status_tratamento.value, id_ativo, id_vulnerabilidade),
            )

    def desvincular(self, id_ativo, id_vulnerabilidade):
        with self.conexao:
            self.conexao.execute(
                """DELETE FROM vinculos
                WHERE id_ativo = ? AND id_vulnerabilidade = ?""",
                (id_ativo, id_vulnerabilidade),
            )
