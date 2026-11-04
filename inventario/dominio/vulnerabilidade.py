from inventario.dominio.enums import NivelDaVulnerabilidade


class Vulnerabilidade:
    def __init__(self, id_vulnerabilidade, nome_vulnerabilidade, cvss):
        self.id_vulnerabilidade = id_vulnerabilidade
        self.nome_vulnerabilidade = nome_vulnerabilidade
        self.cvss = cvss

    def nivel(self):
        if self.cvss > 8.9:
            return NivelDaVulnerabilidade.CRITICO
        elif self.cvss > 6.9:
            return NivelDaVulnerabilidade.ALTO
        elif self.cvss > 3.9:
            return NivelDaVulnerabilidade.MEDIO
        else:
            return NivelDaVulnerabilidade.BAIXO

    def para_dicionario(self):
        return {
            "id_vulnerabilidade": self.id_vulnerabilidade,
            "nome_vulnerabilidade": self.nome_vulnerabilidade,
            "cvss": self.cvss,
        }

    @classmethod
    def de_dicionario(cls, dicionario_vulnerabilidade):
        return cls(
            dicionario_vulnerabilidade["id_vulnerabilidade"],
            dicionario_vulnerabilidade["nome_vulnerabilidade"],
            dicionario_vulnerabilidade["cvss"],
        )
