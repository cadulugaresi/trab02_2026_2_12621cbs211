from inventario.dominio.enums import Cor, Setor, StatusDoAtivo, Tecnologia


class Ativo:
    FATOR_EXPOSICAO_PADRAO = 1.0

    def __init__(self, id, nome, setor, responsavel, status, fator_exposicao=None):
        self.id = id
        self.nome = nome
        self.setor = setor
        self.responsavel = responsavel
        self.status = status
        self.vulnerabilidades = {}
        self.dependencias = {}
        if fator_exposicao is None:
            self.fator_exposicao = self.FATOR_EXPOSICAO_PADRAO
        else:
            self.fator_exposicao = fator_exposicao

    def exibir_detalhes(self):
        return (
            f"\nID: {self.id}\n"
            f"Nome: {self.nome}\n"
            f"Tipo: {type(self).__name__}\n"
            f"Setor: {self.setor.name}\n"
            f"Responsável: {self.responsavel}\n"
            f"Status: {self.status.name}\n"
            f"Fator de exposição: {self.fator_exposicao}"
        )

    def para_dicionario(self):
        lista_de_vulns = []

        for id_vulnerabilidade, status in self.vulnerabilidades.items():
            lista_de_vulns.append(
                {"id_vulnerabilidade": id_vulnerabilidade, "status_tratamento": status.value}
            )

        lista_de_dependencias = []

        for id_ativo_do_qual_depende, fracao in self.dependencias.items():
            lista_de_dependencias.append(
                {"id_ativo_do_qual_depende": id_ativo_do_qual_depende, "fracao": fracao}
            )

        return {
            "id": self.id,
            "nome": self.nome,
            "tipo": type(self).__name__,
            "setor": self.setor.value,
            "responsavel": self.responsavel,
            "status": self.status.value,
            "vulnerabilidades": lista_de_vulns,
            "dependencias": lista_de_dependencias,
            "fator_exposicao": self.fator_exposicao,
        }


class Notebook(Ativo):
    FATOR_EXPOSICAO_PADRAO = 1.2

    def __init__(
        self, id, nome, setor, responsavel, status, sistema_operacional, tela, fator_exposicao=None
    ):
        super().__init__(id, nome, setor, responsavel, status, fator_exposicao)
        self.sistema_operacional = sistema_operacional
        self.tela = tela

    def exibir_detalhes(self):
        detalhes_base = super().exibir_detalhes()
        return (
            f"{detalhes_base}\n"
            f"Sistema operacional: {self.sistema_operacional}\n"
            f"Tamanho da tela: {self.tela} polegadas"
        )

    def para_dicionario(self):
        dicionario_base = super().para_dicionario()
        dicionario_base["sistema_operacional"] = self.sistema_operacional
        dicionario_base["tela"] = self.tela
        return dicionario_base

    @classmethod
    def de_dicionario(cls, dicionario_do_ativo):
        return cls(
            dicionario_do_ativo["id"],
            dicionario_do_ativo["nome"],
            Setor(dicionario_do_ativo["setor"]),
            dicionario_do_ativo["responsavel"],
            StatusDoAtivo(dicionario_do_ativo["status"]),
            dicionario_do_ativo["sistema_operacional"],
            dicionario_do_ativo["tela"],
            dicionario_do_ativo.get("fator_exposicao"),
        )


class Roteador(Ativo):
    FATOR_EXPOSICAO_PADRAO = 1.5

    def __init__(
        self, id, nome, setor, responsavel, status, portas, velocidade, fator_exposicao=None
    ):
        super().__init__(id, nome, setor, responsavel, status, fator_exposicao)
        self.portas = portas
        self.velocidade = velocidade

    def exibir_detalhes(self):
        detalhes_base = super().exibir_detalhes()
        return (
            f"{detalhes_base}\n"
            f"Qtde de portas: {self.portas}\n"
            f"Velocidade: {self.velocidade}MB"
        )

    def para_dicionario(self):
        dicionario_base = super().para_dicionario()
        dicionario_base["portas"] = self.portas
        dicionario_base["velocidade"] = self.velocidade
        return dicionario_base

    @classmethod
    def de_dicionario(cls, dicionario_do_ativo):
        return cls(
            dicionario_do_ativo["id"],
            dicionario_do_ativo["nome"],
            Setor(dicionario_do_ativo["setor"]),
            dicionario_do_ativo["responsavel"],
            StatusDoAtivo(dicionario_do_ativo["status"]),
            dicionario_do_ativo["portas"],
            dicionario_do_ativo["velocidade"],
            dicionario_do_ativo.get("fator_exposicao"),
        )


class Servidor(Ativo):
    FATOR_EXPOSICAO_PADRAO = 1.3

    def __init__(
        self, id, nome, setor, responsavel, status, ram, armazenamento, fator_exposicao=None
    ):
        super().__init__(id, nome, setor, responsavel, status, fator_exposicao)
        self.ram = ram
        self.armazenamento = armazenamento

    def exibir_detalhes(self):
        detalhes_base = super().exibir_detalhes()
        return (
            f"{detalhes_base}\n"
            f"Memória RAM: {self.ram}GB\n"
            f"Qtde armazenamento: {self.armazenamento}T"
        )

    def para_dicionario(self):
        dicionario_base = super().para_dicionario()
        dicionario_base["ram"] = self.ram
        dicionario_base["armazenamento"] = self.armazenamento
        return dicionario_base

    @classmethod
    def de_dicionario(cls, dicionario_do_ativo):
        return cls(
            dicionario_do_ativo["id"],
            dicionario_do_ativo["nome"],
            Setor(dicionario_do_ativo["setor"]),
            dicionario_do_ativo["responsavel"],
            StatusDoAtivo(dicionario_do_ativo["status"]),
            dicionario_do_ativo["ram"],
            dicionario_do_ativo["armazenamento"],
            dicionario_do_ativo.get("fator_exposicao"),
        )


class Impressora(Ativo):
    FATOR_EXPOSICAO_PADRAO = 0.9

    def __init__(self, id, nome, setor, responsavel, status, cor, tecnologia, fator_exposicao=None):
        super().__init__(id, nome, setor, responsavel, status, fator_exposicao)
        self.cor = cor
        self.tecnologia = tecnologia

    def exibir_detalhes(self):
        detalhes_base = super().exibir_detalhes()
        return f"{detalhes_base}\n" f"Cor: {self.cor.name}\n" f"Tecnologia: {self.tecnologia.name}"

    def para_dicionario(self):
        dicionario_base = super().para_dicionario()
        dicionario_base["cor"] = self.cor.value
        dicionario_base["tecnologia"] = self.tecnologia.value
        return dicionario_base

    @classmethod
    def de_dicionario(cls, dicionario_do_ativo):
        return cls(
            dicionario_do_ativo["id"],
            dicionario_do_ativo["nome"],
            Setor(dicionario_do_ativo["setor"]),
            dicionario_do_ativo["responsavel"],
            StatusDoAtivo(dicionario_do_ativo["status"]),
            Cor(dicionario_do_ativo["cor"]),
            Tecnologia(dicionario_do_ativo["tecnologia"]),
            dicionario_do_ativo.get("fator_exposicao"),
        )


MAPA_DE_TIPOS = {
    "Notebook": Notebook,
    "Servidor": Servidor,
    "Roteador": Roteador,
    "Impressora": Impressora,
}
