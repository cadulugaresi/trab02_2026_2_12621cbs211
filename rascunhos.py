from enum import Enum
from funcoes_t2 import *

class StatusDoAtivo(Enum):
    ATIVO = 1
    INATIVO = 2
    EM_MANUTENCAO = 3

class NivelDaVulnerabilidade(Enum):
    BAIXO = 1
    MEDIO = 2
    ALTO = 3

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

def pedir_tipo(mensagem):

    tipo = None

    while tipo is None:

        try:
            print('Tipos de ativo:')
            for numero, nome in OPCOES_MENU.items():
                print(f'{numero} - {nome}')

            tipo_digitado = input(mensagem).strip()
            tipo = validar_tipo(tipo_digitado)

        except DadoInvalidoError as erro:
            print(erro)

    return tipo

def validar_tipo(tipo_digitado):

    if tipo_digitado == '1':
        return Notebook
    
    elif tipo_digitado == '2':
        return Servidor
    
    elif tipo_digitado == '3':
        return Roteador
    
    elif tipo_digitado == '4':
        return Impressora
    
    else:
        raise DadoInvalidoError('Tipo inválido. Tente novamente.')

def cadastro_notebook():

    so = pedir_info('Digite o sistema operacional do ativo: ')
    tela = pedir_float('Digite o tamanho da tela em polegadas: ')

    return so, tela    

def cadastro_roteador():

    portas = pedir_int('Digite a quantidade de portas do roteador: ')
    velocidade = pedir_int('Digite a velocidade do roteador em MB: ')

    return portas, velocidade

def cadastro_servidor():

    ram = pedir_int('Digite a quantidade de RAM do Servidor em GB: ')
    armazenamento = pedir_float('Digite a quantidade de armazenamento do Servidor em T: ')

    return ram, armazenamento

def validar_cor(opcao):

    if opcao == '1':
        return Cor.COLORIDA
    elif opcao == '2':
        return Cor.PRETA_E_BRANCA
    
    else:
        raise DadoInvalidoError('Cor inválida. Tente novamente.')

def pedir_cor():

    cor = None
    while cor is None:

        try:
            print('''
            Qual é a cor do cartucho da impressora?

            1 - Colorido
            2 - Preto e branco
            ''')
            opcao_cor = input('Escolha: ').strip()
            cor = validar_cor(opcao_cor)

        except DadoInvalidoError as erro:
            print(erro)

    return cor

def validar_tecnologia(opcao_tec):

    if opcao_tec == '1':
        return Tecnologia.TINTA
    elif opcao_tec == '2':
        return Tecnologia.LASER
    else:
        raise DadoInvalidoError('Tecnologia inválida. Tente novamente.')

def pedir_tecnologia():

    tecnologia = None
    while tecnologia is None:

        try:
            print('''
            Tecnologias de impressão:
            
            1 - Tinta
            2 - Laser
            ''')
            opcao_tec = input('Qual é a tecnologia da impressão? ')
            tecnologia = validar_tecnologia(opcao_tec)

        except DadoInvalidoError as erro:
            print(erro)

    return tecnologia

def cadastro_impressora():
    cor = pedir_cor()
    tecnologia = pedir_tecnologia()
    return cor, tecnologia

def cadastrar_ativo(ativos):

    tipo = pedir_tipo('Digite o tipo do ativo: ')
    ID_do_ativo = pedir_id_disponivel(ativos)
    nome_ativo = pedir_info('Digite o nome do ativo: ')
    setor = pedir_setor('Digite o setor do ativo: ')
    responsavel = pedir_info('Digite o nome do responsável pelo ativo: ')
    status = pedir_status('Digite o status do ativo: ')

    if tipo is Notebook:
        so, tela = cadastro_notebook()
        ativo = Notebook(ID_do_ativo, nome_ativo, setor, responsavel, status, so, tela)

    elif tipo is Roteador:
        portas, velocidade = cadastro_roteador()
        ativo = Roteador(ID_do_ativo, nome_ativo, setor, responsavel, status, portas, velocidade)

    elif tipo is Servidor:
        ram, armazenamento = cadastro_servidor()
        ativo = Servidor(ID_do_ativo, nome_ativo, setor, responsavel, status, ram, armazenamento)
    
    elif tipo is Impressora:
        cor, tecnologia = cadastro_impressora()
        ativo = Impressora(ID_do_ativo, nome_ativo, setor, responsavel, status, cor, tecnologia)

    print('Ativo cadastrado com sucesso!')
    print(ativo.exibir_detalhes())
    return ativo

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