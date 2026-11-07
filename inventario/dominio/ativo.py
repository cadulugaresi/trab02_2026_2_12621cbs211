from inventario.dominio.enums import Cor, Setor, StatusDoAtivo, Tecnologia


class Ativo:

    def __init__(self, id, nome, setor, responsavel, status):
        self.id = id
        self.nome = nome
        self.setor = setor
        self.responsavel = responsavel
        self.status = status
        self.vulnerabilidades = {}
        self.dependencias = {}

    def exibir_detalhes(self):
        return f"""
            ID: {self.id}
            Nome: {self.nome}
            Tipo: {type(self).__name__}
            Setor: {self.setor.name}
            Responsável: {self.responsavel}
            Status: {self.status.name}
            """

    def para_dicionario(self):
        lista_de_vulns = []

        for id_vulnerabilidade, status in self.vulnerabilidades.items():
            lista_de_vulns.append(
                {"id_vulnerabilidade": id_vulnerabilidade, "status_tratamento": status.value}
            )

        lista_de_dependencias = []

        for id_ativo_do_qual_depende, fracao in self.dependencias.items():
            lista_de_dependencias.append({"id_ativo_do_qual_depende": id_ativo_do_qual_depende, "fracao": fracao})

        return {
            "id": self.id,
            "nome": self.nome,
            "tipo": type(self).__name__,
            "setor": self.setor.value,
            "responsavel": self.responsavel,
            "status": self.status.value,
            "vulnerabilidades": lista_de_vulns,
            "dependencias": lista_de_dependencias,
        }


class Notebook(Ativo):
    def __init__(self, id, nome, setor, responsavel, status, sistema_operacional, tela):
        super().__init__(id, nome, setor, responsavel, status)
        self.sistema_operacional = sistema_operacional
        self.tela = tela

    def exibir_detalhes(self):
        detalhes_base = super().exibir_detalhes()
        return f"""
            {detalhes_base}
            Sistema operacional: {self.sistema_operacional}
            Tamanho da tela: {self.tela} polegadas
            """

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
        )


class Roteador(Ativo):
    def __init__(self, id, nome, setor, responsavel, status, portas, velocidade):
        super().__init__(id, nome, setor, responsavel, status)
        self.portas = portas
        self.velocidade = velocidade

    def exibir_detalhes(self):
        detalhes_base = super().exibir_detalhes()
        return f"""
            {detalhes_base}
            Qtde de portas: {self.portas}
            Velocidade: {self.velocidade}MB
            """

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
        )


class Servidor(Ativo):
    def __init__(self, id, nome, setor, responsavel, status, ram, armazenamento):
        super().__init__(id, nome, setor, responsavel, status)
        self.ram = ram
        self.armazenamento = armazenamento

    def exibir_detalhes(self):
        detalhes_base = super().exibir_detalhes()
        return f"""
            {detalhes_base}
            Memória RAM: {self.ram}GB
            Qtde armazenamento: {self.armazenamento}T
            """

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
        )


class Impressora(Ativo):
    def __init__(self, id, nome, setor, responsavel, status, cor, tecnologia):
        super().__init__(id, nome, setor, responsavel, status)
        self.cor = cor
        self.tecnologia = tecnologia

    def exibir_detalhes(self):
        detalhes_base = super().exibir_detalhes()
        return f"""
            {detalhes_base}
            Cor: {self.cor.name}
            Tecnologia: {self.tecnologia.name}
            """

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
        )


MAPA_DE_TIPOS = {
    "Notebook": Notebook,
    "Servidor": Servidor,
    "Roteador": Roteador,
    "Impressora": Impressora,
}
