from enum import Enum

class StatusDoAtivo(Enum):
    ATIVO = 1
    INATIVO = 2
    EM_MANUTENCAO = 3

class NivelDaVulnerabilidade(Enum):
    BAIXO = 1
    MEDIO = 2
    ALTO = 3

class Categorias(Enum):
    NOTEBOOK = 1
    SERVIDOR = 2
    ROTEADOR = 3
    IMPRESSORA = 4

class StatusDaVuln(Enum):
    ABERTA = 1
    EM_TRATAMENTO = 2
    CORRIGIDA = 3
    ACEITA = 4

class Setor(Enum):
    TI = 1
    FINANCEIRO = 2
    MARKETING = 3
    RH = 4
    JURIDICO = 5

class Cor(Enum):
    COLORIDA = 1
    PRETA_E_BRANCA = 2

class Tecnologia(Enum):
    TINTA = 1
    LASER = 2

class Ativo:

    def __init__(self, id, nome, setor, responsavel, status):
        self.id = id
        self.nome = nome
        self.setor = setor
        self.responsavel = responsavel
        self.status = status
        self.vulnerabilidades = []

    def exibir_detalhes(self):
        return f'''
            ID: {self.id}
            Nome: {self.nome}
            Tipo: {type(self).__name__}
            Setor: {self.setor.name}
            Responsável: {self.responsavel}
            Status: {self.status.name}
            '''

    def para_dicionario(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'tipo': type(self).__name__,
            'setor': self.setor.value,
            'responsavel': self.responsavel,
            'status': self.status.value,
            'vulnerabilidades': [
                vulnerabilidade.para_dicionario() for vulnerabilidade in self.vulnerabilidades
            ]
        }

class Notebook(Ativo):
    def __init__ (self, id, nome, setor, responsavel, status, sistema_operacional, tela):
        super().__init__(id, nome, setor, responsavel, status)
        self.sistema_operacional = sistema_operacional
        self.tela = tela

    def exibir_detalhes(self):
        detalhes_base = super().exibir_detalhes()
        return f'''
            {detalhes_base}
            Sistema operacional: {self.sistema_operacional}
            Tamanho da tela: {self.tela} polegadas
            '''

    def para_dicionario(self):
        dicionario_base = super().para_dicionario()
        dicionario_base['sistema_operacional'] = self.sistema_operacional
        dicionario_base['tela'] = self.tela
        return dicionario_base

    @classmethod
    def de_dicionario(cls, dicionario_do_ativo):
        return cls(
            dicionario_do_ativo['id'],
            dicionario_do_ativo['nome'],
            Setor(dicionario_do_ativo['setor']),
            dicionario_do_ativo['responsavel'],
            StatusDoAtivo(dicionario_do_ativo['status']),
            dicionario_do_ativo['sistema_operacional'],
            dicionario_do_ativo['tela']
        )

class Roteador(Ativo):
    def __init__(self, id, nome, setor, responsavel, status, portas, velocidade):
        super().__init__(id, nome, setor, responsavel, status)
        self.portas = portas
        self.velocidade = velocidade

    def exibir_detalhes(self):
        detalhes_base = super().exibir_detalhes()
        return f'''
            {detalhes_base}
            Qtde de portas: {self.portas}
            Velocidade: {self.velocidade}MB
            '''

    def para_dicionario(self):
        dicionario_base = super().para_dicionario()
        dicionario_base['portas'] = self.portas
        dicionario_base['velocidade'] = self.velocidade
        return dicionario_base

    @classmethod
    def de_dicionario(cls, dicionario_do_ativo):
        return cls(
            dicionario_do_ativo['id'],
            dicionario_do_ativo['nome'],
            Setor(dicionario_do_ativo['setor']),
            dicionario_do_ativo['responsavel'],
            StatusDoAtivo(dicionario_do_ativo['status']),
            dicionario_do_ativo['portas'],
            dicionario_do_ativo['velocidade']
        )


class Servidor(Ativo):
    def __init__(self, id, nome, setor, responsavel, status, ram, armazenamento):
        super().__init__(id, nome, setor, responsavel, status)
        self.ram = ram
        self.armazenamento = armazenamento

    def exibir_detalhes(self):
        detalhes_base = super().exibir_detalhes()
        return f'''
            {detalhes_base}
            Memória RAM: {self.ram}GB
            Qtde armazenamento: {self.armazenamento}T
            '''

    def para_dicionario(self):
        dicionario_base = super().para_dicionario()
        dicionario_base['ram'] = self.ram
        dicionario_base['armazenamento'] = self.armazenamento
        return dicionario_base

    @classmethod
    def de_dicionario(cls, dicionario_do_ativo):
        return cls(
            dicionario_do_ativo['id'],
            dicionario_do_ativo['nome'],
            Setor(dicionario_do_ativo['setor']),
            dicionario_do_ativo['responsavel'],
            StatusDoAtivo(dicionario_do_ativo['status']),
            dicionario_do_ativo['ram'],
            dicionario_do_ativo['armazenamento']
        )

class Impressora(Ativo):
    def __init__(self, id, nome, setor, responsavel, status, cor, tecnologia):
        super().__init__(id, nome, setor, responsavel, status)
        self.cor = cor
        self.tecnologia = tecnologia

    def exibir_detalhes(self):
        detalhes_base = super().exibir_detalhes()
        return f'''
            {detalhes_base}
            Cor: {self.cor.name}
            Tecnologia: {self.tecnologia.name}
            '''

    def para_dicionario(self):
        dicionario_base = super().para_dicionario()
        dicionario_base['cor'] = self.cor.value
        dicionario_base['tecnologia'] = self.tecnologia.value
        return dicionario_base

    @classmethod
    def de_dicionario(cls, dicionario_do_ativo):
        return cls(
            dicionario_do_ativo['id'],
            dicionario_do_ativo['nome'],
            Setor(dicionario_do_ativo['setor']),
            dicionario_do_ativo['responsavel'],
            StatusDoAtivo(dicionario_do_ativo['status']),
            Cor(dicionario_do_ativo['cor']),
            Tecnologia(dicionario_do_ativo['tecnologia'])
        )

MAPA_DE_TIPOS = {
    'Notebook': Notebook,
    'Servidor': Servidor,
    'Roteador': Roteador,
    'Impressora': Impressora
    }

OPCOES_MENU = {
    '1': 'Notebook',
    '2': 'Servidor',
    '3': 'Roteador',
    '4': 'Impressora'
}

def listar_ativos_por_tipo(ativos):
    tipo_digitado = input('Qual tipo? ').strip()
    
    encontrados = filtrar_ativos_por_tipo(tipo_digitado, ativos)
    
    if not encontrados:
        print('Nenhum ativo cadastrado com esse tipo.')
        return
    
    for ativo in encontrados:
        print(ativo.exibir_detalhes())

def filtrar_ativos_por_tipo(tipo_digitado, ativos):
    if not tipo_digitado:
        return []
    
    classes_encontradas = []
    for nome_tipo, classe in MAPA_DE_TIPOS.items():
        if tipo_digitado.lower() in nome_tipo.lower():
            classes_encontradas.append(classe)
    
    if not classes_encontradas:
        return []
    
    encontrados = []
    for ativo in ativos.values():
        for classe in classes_encontradas:
            if isinstance(ativo, classe):
                encontrados.append(ativo)
                break
    
    return encontrados

#Testes:
if __name__ == '__main__':
    ativos = [
        Notebook(1, "Dell", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, "Linux", 15.6),
        Roteador(2, "TP-Link", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, 4, 1000),
        Servidor(3, "Dell PowerEdge", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, 32, 4),
        Impressora(4, "HP", Setor.TI, "Cadu", StatusDoAtivo.ATIVO, Cor.COLORIDA, Tecnologia.LASER),
    ]

    #Teste de listagem de todos os ativos:
    for ativo in ativos:
        print(ativo.exibir_detalhes())
        print('---')

    # Teste de serialização
    print("Testando para_dicionario:")
    for ativo in ativos:
        print(ativo.para_dicionario())
        print('---')

    # Teste de desserialização:
    print("Testando de_dicionario:")
    for ativo in ativos:
        dicionario = ativo.para_dicionario()
        classe = MAPA_DE_TIPOS[dicionario['tipo']]
        ativo_reconstruido = classe.de_dicionario(dicionario)
        print(ativo_reconstruido.exibir_detalhes())
        print('---')

    # Teste de listagem por tipo:
    ativos_dict = {ativo.id: ativo for ativo in ativos}
    print("Testando listar_ativos_por_tipo:")
    listar_ativos_por_tipo(ativos_dict)