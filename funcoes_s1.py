import json
from enum import Enum

ARQUIVO_DADOS = 'ativos.json'

class Vulnerabilidade:
    def __init__(self, nome_vulnerabilidade, tipo, nivel, status_tratamento):
        self.nome_vulnerabilidade = nome_vulnerabilidade
        self.tipo = tipo
        self.nivel = nivel
        self.status_tratamento = status_tratamento

    def para_dicionario(self):
        return {
            'nome da vulnerabilidade': self.nome_vulnerabilidade,
            'tipo': self.tipo,
            'nivel': self.nivel.value,
            'status_tratamento': self.status_tratamento.value
        }

class Ativo:

    def __init__(self, id, nome, categoria, setor, responsavel, status):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.setor = setor
        self.responsavel = responsavel
        self.status = status
        self.vulnerabilidades = []

    def para_dicionario(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'categoria': self.categoria.value,
            'setor': self.setor.value,
            'responsavel': self.responsavel,
            'status': self.status.value,
            'vulnerabilidades': [
                vulnerabilidade.para_dicionario() for vulnerabilidade in self.vulnerabilidades
            ]
        }

class DadoInvalidoError(Exception):
    pass

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

def validar_nome_responsavel(nome):
        
    if not nome:
        raise DadoInvalidoError('Este campo não pode ser vazio.')
    if nome.isnumeric():
        raise DadoInvalidoError('Este campo não pode ser composto apenas por números.')

def pedir_info(mensagem):

    info = None
    while info is None:

        info=input(mensagem).strip()

        try:
            validar_nome_responsavel(info)
            return info
        except DadoInvalidoError as erro:
            print(erro)
            info = None

def pedir_status(mensagem):

    status = None

    while status is None:

        try:
            print(f'''
            Status:

            ATIVO - 1
            INATIVO - 2
            EM_MANUTENCAO - 3
            ''')

            status_digitado = input(mensagem).strip()
            status = validar_status(status_digitado)

        except DadoInvalidoError as erro:
            print(erro)

    return status

def validar_status(status_digitado):

    if status_digitado == '1':
        return StatusDoAtivo.ATIVO
    
    elif status_digitado == '2':
        return StatusDoAtivo.INATIVO
    
    elif status_digitado == '3':
        return StatusDoAtivo.EM_MANUTENCAO
    
    else:
        raise DadoInvalidoError('Status inválido. Tente novamente.')

def pedir_setor(mensagem):

    setor = None

    while setor is None:

        try:
            print(f'''
            Setor:

            TI - 1
            FINANCEIRO - 2
            MARKETING - 3
            RH - 4
            JURIDICO - 5
            ''')

            setor_digitado = input(mensagem).strip()
            setor = validar_setor(setor_digitado)

        except DadoInvalidoError as erro:
            print(erro)

    return setor

def validar_setor(setor_digitado):

    if setor_digitado == '1':
        return Setor.TI
    
    elif setor_digitado == '2':
        return Setor.FINANCEIRO
    
    elif setor_digitado == '3':
        return Setor.MARKETING
    
    elif setor_digitado == '4':
        return Setor.RH
    
    elif setor_digitado == '5':
        return Setor.JURIDICO
    
    else:
        raise DadoInvalidoError('Setor inválido. Tente novamente.')

def pedir_id(mensagem):

    while True:
        try:
            id_texto=input(mensagem).strip()

            if not id_texto:
                raise DadoInvalidoError('Este campo não pode ser vazio. Tente novamente.')

            if int(id_texto) <= 0:
                raise DadoInvalidoError('O ID não pode ser nulo ou negativo. Tente novamente.')

            return int(id_texto)

        except ValueError:
            print('Digite um número válido')

        except DadoInvalidoError as erro:
            print(erro)

def pedir_id_disponivel(ativos):

    while True:

        ID_do_ativo = pedir_id('Digite o ID do ativo: ')
        if encontrar_ativo_por_id(ID_do_ativo, ativos) is None:
            return ID_do_ativo
        
        print('Já existe um ativo cadastrado com este ID. Tente outro.')

def pedir_categoria(mensagem):

    categoria = None

    while categoria is None:

        try: 
            print(f'''
            Categorias:

            NOTEBOOK - 1
            SERVIDOR - 2
            ROTEADOR - 3
            IMPRESSORA - 4
            ''')

            categoria_digitada = input(mensagem).strip()
            categoria = validar_categoria(categoria_digitada)

        except DadoInvalidoError as erro:
            print(erro)

    return categoria

def validar_categoria(categoria_digitada):

    if categoria_digitada == '1':
        return Categorias.NOTEBOOK
        
    elif categoria_digitada == '2':
        return Categorias.SERVIDOR

    elif categoria_digitada == '3':
        return Categorias.ROTEADOR

    elif categoria_digitada == '4':
        return Categorias.IMPRESSORA

    else:
        raise DadoInvalidoError('Dado inválido. Tente novamente.')

def cadastrar_ativo(ativos):

    ID_do_ativo = pedir_id_disponivel(ativos)
    nome_ativo = pedir_info('Digite o nome do ativo: ')
    categoria = pedir_categoria('Digite a categoria do ativo: ')
    setor = pedir_setor('Digite o setor do ativo: ')
    responsavel = pedir_info('Digite o nome do responsável pelo ativo: ')
    status = pedir_status('Digite o status do ativo: ')

    print(f'''Ativo cadastrado com sucesso!
    Ativo cadastrado:ID {ID_do_ativo}
    Nome {nome_ativo}
    Categoria {categoria.name}
    Setor {setor.name}
    Responsável {responsavel}
    Status {status.name}
    ''')

    return Ativo(ID_do_ativo, nome_ativo, categoria, setor, responsavel, status)

def encontrar_ativo_por_id(ID, ativos):
    return ativos.get(ID)

def encontrar_ativo_por_nome(nome, ativos):

    encontrados = []

    for ativo in ativos.values():
        if nome.lower() in ativo.nome.lower():
            encontrados.append(ativo)

    return encontrados

def mostrar_ativo(ativo):
    print(f'''
    ID: {ativo.id}
    Nome: {ativo.nome}
    Categoria: {ativo.categoria.name}
    Setor: {ativo.setor.name}
    Responsável: {ativo.responsavel}
    Status: {ativo.status.name}
    ''')

def mostrar_vulnerabilidade(vulnerabilidade):

    print(f'''
    Vulnerabilidade: {vulnerabilidade.nome_vulnerabilidade}
    Tipo: {vulnerabilidade.tipo}
    Nível: {vulnerabilidade.nivel.name.lower()}
    Status: {vulnerabilidade.status_tratamento.name.lower()}
    ''')

def editar_ativo(ativos):

    id_ativo = pedir_id('Digite o ID do ativo que deseja editar: ')

    ativo_encontrado = encontrar_ativo_por_id(id_ativo, ativos)

    if not ativo_encontrado:
        print('Nenhum ativo com este ID cadastrado.')
        return

    print(f'''Dados atuais do ativo:
    ID: {ativo_encontrado.id}
    Nome: {ativo_encontrado.nome}
    Responsável: {ativo_encontrado.responsavel}
    Categoria: {ativo_encontrado.categoria.name}
    Setor: {ativo_encontrado.setor.name}
    Status: {ativo_encontrado.status.name}
    ''')

    while True:
        print(f'''
        MENU DE EDIÇÃO
        1 - Editar responsável
        2 - Editar status
        3 - Editar setor
        4 - Editar categoria
        5 - Voltar''')

        opcao = input('Escolha uma opção: ').strip()

        if opcao == '1':
            novo_responsavel = pedir_info('Digite o novo nome do responsável pelo ativo: ')
            ativo_encontrado.responsavel = novo_responsavel
            print(f'Responsável atualizado com sucesso. Novo responsável: {novo_responsavel}')

        elif opcao == '2':
            novo_status=pedir_status('Digite o novo status do ativo: ')
            ativo_encontrado.status = novo_status
            print(f'Status do ativo atualizado com sucesso. Status atual: {novo_status.name}.')

        elif opcao == '3':
            novo_setor=pedir_setor('Digite o novo setor do ativo: ')
            ativo_encontrado.setor = novo_setor
            print(f'Setor do ativo atualizado com sucesso. Setor atual: {novo_setor.name}.')

        elif opcao == '4':
            nova_categ = pedir_categoria('Digite a nova categoria do ativo: ')
            ativo_encontrado.categoria = nova_categ
            print(f'Categoria do ativo atualizada com sucesso. Categoria atual: {nova_categ.name}.')

        elif opcao == '5':
            print('Voltando...')
            break

        else:
            print('Opção inválida.')

def excluir_ativo(ativos):
    if ativos:
        id_a_excluir = pedir_id('Digite o ID do ativo que deseja excluir: ')
        ativo_encontrado = encontrar_ativo_por_id(id_a_excluir, ativos)

        if ativo_encontrado:

            if confirmar_exclusao(ativo_encontrado):
                del ativos[ativo_encontrado.id]
                salvar_dados(ativos)
                print('Ativo excluído com sucesso!')
            else:
                print('Exclusão cancelada.')

        else:
            print('Ativo não encontrado.')

    else:
        print('Nenhum ativo cadastrado.')

def confirmar_exclusao(ativo):

    print(f'Tem certeza que deseja excluir o ativo "{ativo.nome}" (ID {ativo.id})?')
    resposta = input('Digite "sim" para excluir ou tecle enter para voltar: ').strip().lower()

    if resposta == 'sim':
        return True
    else:
        return False

def nivel_vulnerabilidade():

    nivel = None
    while nivel is None:
        print(f'''BAIXO - 1 \n MEDIO - 2 \n ALTO - 3''')

        nivel_digitado = input('Digite o nível da vulnerabilidade: ').strip()

        if nivel_digitado == '1':
            nivel = NivelDaVulnerabilidade.BAIXO
        elif nivel_digitado == '2':
            nivel = NivelDaVulnerabilidade.MEDIO
        elif nivel_digitado == '3':
            nivel = NivelDaVulnerabilidade.ALTO
        else:
            print('Nível inválido. Tente novamente.')
            continue

    return nivel

def status_vulnerabilidade():

    status_tratamento = None
    while status_tratamento is None:
        print(f'''ABERTA - 1 \n EM TRATAMENTO - 2 \n CORRIGIDA - 3 \n ACEITA - 4''')

        status_digitado = input('Digite o status atual da vulnerabilidade: ').strip()

        if status_digitado == '1':
            status_tratamento = StatusDaVuln.ABERTA
        elif status_digitado == '2':
            status_tratamento = StatusDaVuln.EM_TRATAMENTO
        elif status_digitado == '3':
            status_tratamento = StatusDaVuln.CORRIGIDA
        elif status_digitado == '4':
            status_tratamento = StatusDaVuln.ACEITA

        else:
            print('Status inválido. Tente novamente.')
            continue

    return status_tratamento

def salvar_dados(ativos):

    lista_para_salvar = []

    for ativo in ativos.values():
        lista_para_salvar.append(ativo.para_dicionario())

    try:
        with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as arquivo:
            json.dump(lista_para_salvar, arquivo, indent=4, ensure_ascii=False)
    except PermissionError:
        print('Erro de Persistência: Sem permissão para gravar no arquivo no computador.')
    except IOError:
        print('Erro de Persistência ao salvar os dados no arquivo.')

def carregar_dados():

    try:
        with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as arquivo:
            dados_brutos = json.load(arquivo)

            ativos_carregados = {}

            for ativo_dicionario in dados_brutos:

                vulnerabilidades_carregadas = []

                for vulnerabilidade_dicionario in ativo_dicionario['vulnerabilidades']:
                    nova_vulnerabilidade = Vulnerabilidade(
                        vulnerabilidade_dicionario['nome da vulnerabilidade'],
                        vulnerabilidade_dicionario['tipo'],
                        NivelDaVulnerabilidade(vulnerabilidade_dicionario['nivel']),
                        StatusDaVuln(vulnerabilidade_dicionario['status_tratamento'])
                    )
                    vulnerabilidades_carregadas.append(nova_vulnerabilidade)

                novo_ativo = Ativo(
                    ativo_dicionario['id'],
                    ativo_dicionario['nome'],
                    Categorias(ativo_dicionario['categoria']),
                    Setor(ativo_dicionario['setor']),
                    ativo_dicionario['responsavel'],
                    StatusDoAtivo(ativo_dicionario['status'])
                )

                novo_ativo.vulnerabilidades = vulnerabilidades_carregadas

                ativos_carregados[novo_ativo.id] = novo_ativo

            return ativos_carregados

    except FileNotFoundError:
        return {}

    except json.JSONDecodeError:
        print('Aviso: ocorreu um erro no arquivo de dados. Criando um novo arquivo...')
        return {}